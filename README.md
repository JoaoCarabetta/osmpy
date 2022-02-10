**Powerfull wrapper around OSM Overpass Turbo to query regions of any size and shape**

```bash
pip install osmpy
```

#### List precooked queries
```python
osmpy.list_queries()

            name                                          docstring
0      Amenities           Location of amenities within a boundary 
1  AmentiesCount    Number of amenities per type within a boundary 
2           POIs   Location of Points of Interest within a bound...
3     RoadLength      Length of road by roadtype within a boundary 
```

#### Get all Points of Interest (POIs) within a boundary
```python
import osmpy
from shapely import wkt

boundary = wkt.loads('POLYGON((-46.63 -23.54,-46.6 -23.54,-46.62 -23.55,-46.63 -23.55,-46.63 -23.54))')
osmpy.get('POIs', boundary)

    type          id        lat        lon                                               tags                      poi
0   node   661212030 -23.544739 -46.626160           {'amenity': 'fuel', 'name': 'Posto NGM'}             amenity:fuel
1   node   661212089 -23.547450 -46.626073  {'amenity': 'fuel', 'name': 'Posto Maserati', ...             amenity:fuel
2   node   745733280 -23.541411 -46.613930  {'addr:city': 'São Paulo', 'addr:housenumber':...             amenity:bank
3   node   745733292 -23.542070 -46.614916  {'addr:city': 'São Paulo', 'addr:housenumber':...             amenity:bank
4   node   889763809 -23.542558 -46.620360  {'addr:housenumber': '110/C9', 'addr:street': ...    amenity:social_centre
..   ...         ...        ...        ...                                                ...                      ...
82  node  5663737625 -23.540027 -46.605425  {'access': 'yes', 'addr:city': 'São Paulo', 'a...          amenity:parking
83  node  5990269247 -23.540650 -46.607532  {'addr:city': 'São Paulo', 'addr:housenumber':...        amenity:fast_food
84  node  6621564995 -23.543880 -46.626414  {'access': 'yes', 'addr:city': 'São Paulo', 'a...          amenity:parking
85  node  6625433725 -23.546727 -46.623956  {'access': 'yes', 'addr:city': 'São Paulo', 'a...          amenity:parking
86  node  6625433753 -23.547111 -46.624790  {'access': 'yes', 'addr:city': 'São Paulo', 'a...  amenity:bicycle_parking
```

#### Total road length by road type
```python
osmpy.get('RoadLength', boundary)

               count     length
highway                        
bus_stop           1     82.624
corridor           2    482.195
cycleway           1    134.197
footway          116   5473.419
living_street      3    422.378
path               4    735.539
pedestrian         3     90.327
platform           3    239.206
primary           28   2067.562
primary_link      12   1123.544
```

#### You can use your own query

```python

## Use `{boundary}` as a placeholder.
query = """
    [out:json];
    node["amenity"](poly:"{boundary}");
    out body geom;
    """

osmpy.get(query, boundary)
```

## Create a precooked query

```python
class YourPrecookedQuery(osmpy.queries.QueryType):

    query = """
    <OSM Overpass Turbo Query>
    """

    docstring = """
    <Query description>
    """

    def postprocess(self, df):
        """Post process API result
        """
        return df['tags'].apply(pd.Series).groupby('amenity').sum()

osmpy.get(YourPrecookedQuery, boundary)
```

:point_right: Leave an issue or PR if you want to add a new query to the package

## Credits

Function `katana` from @snorfalorpagus_.
