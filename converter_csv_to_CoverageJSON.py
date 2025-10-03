
import csv  # Module for reading CSV files
import json  # Module for working with JSON data

def csv_to_coveragejson(csv_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Read rows into dictionaries using column headers
        data = list(reader)  # Convert the reader object to a list of dictionaries

    # Extract individual columns from the CSV data
    times = [row['time'] for row in data]  # List of time values
    longitudes = [float(row['longitude']) for row in data]  # List of longitude values as floats
    latitudes = [float(row['latitude']) for row in data]  # List of latitude values as floats
    temperatures = [float(row['temperature']) for row in data]  # List of temperature values as floats

    # Assume all rows have the same lat/lon (i.e., point coverage)
    lon = longitudes[0]  # Use the first longitude value
    lat = latitudes[0]  # Use the first latitude value

    # Construct the CoverageJSON structure
    coveragejson = {
        "type": "Coverage",
        "domain": {
            "type": "Domain",
            "domainType": "PointSeries",  # Indicates data is a time series at a single point
            "axes": {
                "t": {"values": times},  # Time axis
                "x": {"values": [lon]},  # Longitude axis
                "y": {"values": [lat]}   # Latitude axis
            },
            "referencing": [
                {
                    "coordinates": ["x", "y"],
                    "system": {
                        "type": "GeographicCRS",  # Coordinate Reference System for spatial data
                        "id": "http://www.opengis.net/def/crs/EPSG/0/4326"  # WGS 84
                    }
                },
                {
                    "coordinates": ["t"],
                    "system": {
                        "type": "TemporalRS",  # Temporal Reference System
                        "calendar": "Gregorian"  # Gregorian calendar
                    }
                }
            ]
        },
        "parameters": {
            "temperature": {
                "type": "Parameter",
                "observedProperty": {
                    "label": {"en": "Air Temperature"},  # Human-readable label
                    "id": "http://vocab.nerc.ac.uk/standard_name/air_temperature"  # Standardized identifier
                },
                "unit": {
                    "label": {"en": "Kelvin"},  # Unit label
                    "symbol": {
                        "value": "K",  # Symbol for Kelvin
                        "type": "http://www.opengis.net/def/uom/UCUM/"  # Unit type URI
                    }
                }
            }
        },
        "ranges": {
            "temperature": {
                "type": "NdArray",  # Indicates data is a numerical array
                "dataType": "float",  # Data type of the values
                "axisNames": ["t"],  # Axis along which data is organized
                "shape": [len(times)],  # Shape of the array (length of time series)
                "values": temperatures  # Actual temperature values
            }
        }
    }

    return coveragejson  # Return the constructed CoverageJSON object


# Example usage
coverage = csv_to_coveragejson("input_csv_data.csv")  # Convert CSV to CoverageJSON
with open("coverage.json", "w") as f:
    json.dump(coverage, f, indent=2)  # Write the CoverageJSON to a file with indentation
