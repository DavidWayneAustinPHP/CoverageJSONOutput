
import csv
import json
from datetime import datetime

def csv_to_coveragejson(csv_file_path):
    # Read CSV data
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Extract domain axes (assuming time and location for this example)
    times = [row['time'] for row in data]
    longitudes = [float(row['longitude']) for row in data]
    latitudes = [float(row['latitude']) for row in data]
    temperature = [float(row['temperature']) for row in data]

    coveragejson = {
        "@context": "https://covjson.org/context.jsonld",
        "type": "Coverage",
        "domain": {
            "type": "Domain",
            "domainType": "Point",
            "axes": {
                "x": {"temperature": longitudes},
                "y": {"temperature": latitudes},
                "t": {"temperature": times}
            },
            "referencing": [
                {"coordinates": ["x", "y"], "system": {"type": "GeographicCRS", "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}},
                {"coordinates": ["t"], "system": {"type": "TemporalRS", "calendar": "Gregorian"}}
            ]
        },
        "parameters": {
            "value": {
                "type": "Parameter",
                "description": {"en": "Sample value"},
                "unit": {"symbol": "unit"}
            }
        },
        "ranges": {
            "value": {
                "type": "NdArray",
                "dataType": "float",
                "axisNames": ["t"],
                "shape": [len(temperature)],
                "temperature": temperature
            }
        }
    }

    return coveragejson

# Example usage
coverage = csv_to_coveragejson("example.csv")
with open("coverage.json", "w") as f:
    json.dump(coverage, f, indent=2)
