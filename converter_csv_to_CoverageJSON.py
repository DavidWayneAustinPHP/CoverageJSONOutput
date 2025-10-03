import csv
import json

def csv_to_coveragejson(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Extract axes and values
    times = [row['time'] for row in data]
    longitudes = [float(row['longitude']) for row in data]
    latitudes = [float(row['latitude']) for row in data]
    temperatures = [float(row['temperature']) for row in data]

    # Assuming all rows have the same lat/lon (point coverage)
    lon = longitudes[0]
    lat = latitudes[0]

    coveragejson = {
        "type": "Coverage",
        "domain": {
            "type": "Domain",
            "domainType": "PointSeries",
            "axes": {
                "t": {"values": times},
                "x": {"values": [lon]},
                "y": {"values": [lat]}
            },
            "referencing": [
                {
                    "coordinates": ["x", "y"],
                    "system": {
                        "type": "GeographicCRS",
                        "id": "http://www.opengis.net/def/crs/EPSG/0/4326"
                    }
                },
                {
                    "coordinates": ["t"],
                    "system": {
                        "type": "TemporalRS",
                        "calendar": "Gregorian"
                    }
                }
            ]
        },
        "parameters": {
            "temperature": {
                "type": "Parameter",
                "observedProperty": {
                    "label": {"en": "Air Temperature"},
                    "id": "http://vocab.nerc.ac.uk/standard_name/air_temperature"
                },
                "unit": {
                    "label": {"en": "Kelvin"},
                    "symbol": {
                        "value": "K",
                        "type": "http://www.opengis.net/def/uom/UCUM/"
                    }
                }
            }
        },
        "ranges": {
            "temperature": {
                "type": "NdArray",
                "dataType": "float",
                "axisNames": ["t"],
                "shape": [len(times)],
                "values": temperatures
            }
        }
    }

    return coveragejson



# Example usage
coverage = csv_to_coveragejson("input_csv_data.csv")
with open("coverage.json", "w") as f:
    json.dump(coverage, f, indent=2)
