import geojson
import requests
from shapely.geometry import box, Polygon, MultiPolygon, GeometryCollection, shape
from shapely import wkt
from shapely.ops import transform
import shapely
from functools import partial
import pyproj
import time
import json
from retry import retry
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def simplify(s, delta=0.05):
    
    while not check_length(s):
        s = s.simplify(delta, False)
        delta = delta + 0.05

    return s

def check_length(s, threshold=3000):
    
    return len(str(s)) < threshold

def get_area(s):
    s = shape(s)
    proj = partial(
        pyproj.transform, pyproj.Proj(init="epsg:4326"), pyproj.Proj(init="epsg:3857")
    )

    return transform(proj, s).area / 1e6  # km


def threshold_func(g, value):

    return get_area(g) < value


def katana(geometry, threshold_func, threshold_value, count=0):
    """Split a Polygon into two parts across it's shortest dimension"""
    bounds = geometry.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    if threshold_func(geometry, threshold_value) or count == 250:
        # either the polygon is smaller than the threshold, or the maximum
        # number of recursions has been reached
        return [geometry]
    if height >= width:
        # split left to right
        a = box(bounds[0], bounds[1], bounds[2], bounds[1] + height / 2)
        b = box(bounds[0], bounds[1] + height / 2, bounds[2], bounds[3])
    else:
        # split top to bottom
        a = box(bounds[0], bounds[1], bounds[0] + width / 2, bounds[3])
        b = box(bounds[0] + width / 2, bounds[1], bounds[2], bounds[3])
    result = []
    for d in (
        a,
        b,
    ):
        c = geometry.intersection(d)
        if not isinstance(c, GeometryCollection):
            c = [c]
        for e in c:
            if isinstance(e, (Polygon, MultiPolygon)):
                result.extend(katana(e, threshold_func, threshold_value, count + 1))
    if count > 0:
        return result
    # convert multipart into singlepart
    final_result = []
    for g in result:
        if isinstance(g, MultiPolygon):
            final_result.extend(g)
        else:
            final_result.append(g)
    return final_result


def to_geojson(x):

    if isinstance(x, shapely.geometry.multipolygon.MultiPolygon):
        x = max(x, key=lambda a: a.area)

    g = geojson.Feature(geometry=x, properties={}).geometry

    return g["coordinates"][0]


def swipe(x):
    return [[c[1], c[0]] for c in x]


def flatten(l):
    return [str(round(item, 4)) for sublist in l for item in sublist]


def to_overpass_coords(x):

    coords = to_geojson(x)
    coords = swipe(coords)
    coords = flatten(coords)
    coords = " ".join(coords)
    return coords


@retry(tries=5)
def overpass_request(geo):

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = (
        """
    [out:json];
    way["highway"](poly:"%s");
    for (t["highway"])
    {
       make stat highway=_.val,
           count=count(ways),length=sum(length());
       out;
    }"""
        % geo
    )

    response = requests.get(overpass_url, params={"data": overpass_query})
    return [e["tags"] for e in response.json()["elements"]]


def get(geometry, threshold_value=1000000):
    """Get Open Street Maps highways length in meters and object count for a given geometry

    It splits the regions to manage overpass turbo limits.

    For MultiPolygons, only the biggest polygon will be considered.

    Parameters
    ----------
    geometry : shapely.geometry
        A shapely polygon
    threshold_value : int, optional
        Maximum area in sq km to split the polygons, by default 1000000

    Returns
    -------
    pd.DataFrame
        Table indexed by highway with length sum in meters and observation count
    """

    geometries = katana(geometry, threshold_func, threshold_value)

    responses = []
    for geo in geometries:

        geo = to_overpass_coords(geo)
        responses.append(overpass_request(geo))

    data = pd.concat([pd.DataFrame(d) for d in responses])
    data["length"] = data["length"].astype(float)
    data["count"] = data["count"].astype(int)
    data = data.groupby("highway").sum()

    return data
