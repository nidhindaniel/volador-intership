
import json

import numpy as np
import xarray as xr
import rioxarray  # noqa: F401  (registers the .rio accessor)
import geopandas as gpd
from matplotlib import pyplot as plt, colors
from shapely.geometry import box


def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)


def build_aoi(geojson_path, buffer_m):
    """Read the GeoJSON study area (Polygon, or Point which becomes a square of +/- buffer_m metres).

    Returns (aoi_lonlat, aoi_utm): the same polygon in EPSG:4326 and in a metric UTM CRS.
    """
    gdf = gpd.read_file(geojson_path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    utm = gdf.estimate_utm_crs()
    gdf_utm = gdf.to_crs(utm)
    if gdf_utm.geometry.geom_type.eq("Point").all():
        gdf_utm["geometry"] = [box(p.x - buffer_m, p.y - buffer_m, p.x + buffer_m, p.y + buffer_m)
                               for p in gdf_utm.geometry]
    return gdf_utm.to_crs("EPSG:4326"), gdf_utm


def get_scene_real(aoi_lonlat, start, end, max_cloud, tile=None):
    """Find the least cloudy Sentinel-2 L2A scene in a date window (Microsoft Planetary Computer)
    and return the red (B04) and NIR (B08) bands clipped to the AOI as reflectance (0-1)."""
    import pystac_client
    import planetary_computer

    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    items = list(catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=list(aoi_lonlat.total_bounds),
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": max_cloud}},
    ).items())
    if tile:  # use the same satellite tile for date 2 so both rasters share one grid
        items = [i for i in items if i.properties.get("s2:mgrs_tile") == tile]
    if not items:
        raise RuntimeError(f"No Sentinel-2 scene under {max_cloud}% cloud between {start} and {end}. "
                           "Widen the date window or raise max_cloud_percent in config.json.")
    item = min(items, key=lambda i: i.properties["eo:cloud_cover"])
    # Scenes processed with baseline >= 04.00 have a +1000 offset in the digital numbers
    offset = 1000 if float(item.properties.get("s2:processing_baseline", "0")) >= 4.0 else 0

    def read_band(name):
        da = rioxarray.open_rasterio(item.assets[name].href, masked=True).squeeze(drop=True)
        da = da.rio.clip(aoi_lonlat.to_crs(da.rio.crs).geometry, from_disk=True)
        return (da - offset) / 10000

    meta = {"scene_id": item.id, "date": item.datetime.date().isoformat(),
            "cloud_percent": round(item.properties["eo:cloud_cover"], 1),
            "tile": item.properties.get("s2:mgrs_tile")}
    return read_band("B04"), read_band("B08"), meta


def get_scene_synthetic(aoi_utm, loss):
    """Fake red/NIR rasters over the AOI so the notebook can be tested offline."""
    n = 200
    minx, miny, maxx, maxy = aoi_utm.total_bounds
    px = (maxx - minx) / n
    x = minx + (np.arange(n) + 0.5) * px
    y = maxy - (np.arange(n) + 0.5) * px
    yy, xx = np.mgrid[0:n, 0:n]
    veg = 0.35 + 0.15 * np.sin(xx / 25) * np.cos(yy / 35)
    if loss:  # simulated vegetation loss block placed inside the polygon
        p = aoi_utm.geometry.iloc[0].representative_point()
        ci, cj = int((maxy - p.y) / px), int((p.x - minx) / px)
        veg[max(ci - 15, 0):ci + 15, max(cj - 15, 0):cj + 15] = 0.05
    nir = 0.30 + 0.35 * veg
    red = nir * (1 - veg) / (1 + veg)

    def make(a):
        da = xr.DataArray(a, coords={"y": y, "x": x}, dims=("y", "x")).rio.write_crs(aoi_utm.crs)
        return da.rio.clip(aoi_utm.geometry, drop=False)   # blank out pixels outside the polygon, like the real data

    meta = {"scene_id": "synthetic", "date": "synthetic-loss" if loss else "synthetic-base",
            "cloud_percent": 0.0, "tile": None}
    return make(red), make(nir), meta


def ndvi(red, nir):
    return ((nir - red) / (nir + red)).clip(-1, 1)


def to_overlay(da, vmin, vmax, cmap):
    """Reproject a raster to lat/lon and turn it into an RGBA image + bounds for folium."""
    da4326 = da.rio.reproject("EPSG:4326")
    arr = da4326.values
    rgba = plt.get_cmap(cmap)(colors.Normalize(vmin, vmax)(arr))
    rgba[np.isnan(arr)] = 0
    w, s, e, n = da4326.rio.bounds()
    return rgba, [[s, w], [n, e]]
