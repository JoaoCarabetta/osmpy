import pytest
from shapely.geometry import Polygon
from osmpy.core import simplify, check_length, get_area, threshold_func, katana, to_geojson, swipe, flatten, to_overpass_coords, _get_queries_names

def test_simplify():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])  # roughly 111 x 111 km square
    simplified = simplify(polygon)
    assert isinstance(simplified, Polygon)

def test_check_length():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    assert check_length(polygon) is True

def test_get_area():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    area = get_area(polygon)
    assert 11000 <= area <= 16298  # considering a roughly 111 x 111 km square

def test_threshold_func():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    assert threshold_func(polygon, 16298) is True  # considering a roughly 111 x 111 km square

def test_katana():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    result = katana(polygon, threshold_func, 15000)
    assert isinstance(result, list)
    assert all(isinstance(r, Polygon) for r in result)

def test_to_geojson():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    result = to_geojson(polygon)
    assert isinstance(result, list)
    assert len(result) == 5  # 5 points in a Square, last one equals to the first

def test_swipe():
    coords = [(-70, 40), (-70, 41), (-69, 41), (-70, 40)]
    result = swipe(coords)
    assert result == [[40, -70], [41, -70], [41, -69], [40, -70]]

def test_flatten():
    coords = [[-70, 40], [-70, 41], [-69, 41], [-69, 40]]
    result = flatten(coords)
    assert result == ['-70', '40', '-70', '41', '-69', '41', '-69', '40']

def test_to_overpass_coords():
    polygon = Polygon([(-70, 40), (-70, 41), (-69, 41), (-69, 40), (-70, 40)])
    result = to_overpass_coords(polygon)
    assert isinstance(result, str)