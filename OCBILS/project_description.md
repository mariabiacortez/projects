Summary of Ocbils project


----


Data Processing
===============

Python requirements:
 - gdal
 - lmpy - https://github.com/lifemapper/lmpy
 - BiotaphyPy - https://github.com/biotaphy/BiotaphyPy

1. Acquire study tree (Smith and Brown 2008)
2. Get accepted taxa names for the tips in the tree (get_accepted_names_for_tree.py)
3. Download data from iDigBio and GBIF
 - iDigBio: https://api.idigbio.org/v2/download/?rq={%22scientificname%22:%20{%22type%22:%20%22exists%22},%22kingdom%22:%20%22Plantae%22,%20%22geopoint%22:%20{%22type%22:%20%22exists%22}}&email={fill in email}
 - GBIF (HTTP POST): https://api.gbif.org/v1/occurrence/download/request
   - POST data
```
{
    "creator": "userName",
    "notificationAddresses": [
        "userEmail@example.org"
    ],
    "sendNotification": true,
    "format": "SIMPLE_CSV",
    "predicate": {
        "type": "and",
        "predicates": [
            {
                "type": "equals",
                "key": "BASIS_OF_RECORD",
                "value": "PRESERVED_SPECIMEN"
            },
            {
                "type": "equals",
                "key": "KINGDOM_KEY",
                "value": "6"
            },
            {
                "type": "equals",
                "key": "HAS_COORDINATE",
                "value": "true"
            },
            {
                "type":"equals",
                "key":"HAS_GEOSPATIAL_ISSUE",
                "value":"false"
            }
        ]
    }
}
```
4. Process iDigBio and GBIF files (process_occurrence_download.py)
5. Fill in missing data from iDigBio and GBIF and get data from POWO (backfill_missing_data.py)
6. Filter data and assemble occurrence CSV (create_occurrence_csv.py)
7. POST using Lifemapper / Biotaphy web UI (http://client.lifemapper.org/biotpahy/)
8. Calculate PAM stats, encode environment layers and create GeoJSON (create_geojson_for_stats_and_env.py)
