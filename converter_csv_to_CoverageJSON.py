
import csv
import json

# Class responsible for reading CSV data
class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        # Reads CSV file and returns a list of dictionaries (rows)
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)


# Class responsible for extracting relevant data from CSV rows
class CoverageDataExtractor:
    def __init__(self, data):
        self.data = data

    def extract(self):
        # Extracts time, longitude, latitude, and temperature values
        times = [row['time'] for row in self.data]
        longitudes = [float(row['longitude']) for row in self.data]
        latitudes = [float(row['latitude']) for row in self.data]
        temperatures = [float(row['temperature']) for row in self.data]

        # Assumes all rows have the same lat/lon (point coverage)
        return {
            "times": times,
            "longitude": longitudes[0],
            "latitude": latitudes[0],
            "temperatures": temperatures
        }


# Class responsible for building the CoverageJSON structure
class CoverageJSONBuilder:
    def __init__(self, extracted_data):
        self.times = extracted_data["times"]
        self.lon = extracted_data["longitude"]
        self.lat = extracted_data["latitude"]
        self.temperatures = extracted_data["temperatures"]

    def build(self):
        # Constructs the CoverageJSON dictionary using extracted data
        return {
            "type": "Coverage",
            "domain": {
                "type": "Domain",
                "domainType": "PointSeries",
                "axes": {
                    "t": {"values": self.times},
                    "x": {"values": [self.lon]},
                    "y": {"values": [self.lat]}
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
                        "label": {"": "Kelvin"},
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
                    "shape": [len(self.timestemperatures
                }
            }
        }


# Class responsible for writing the CoverageJSON to a file
class CoverageJSONWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, coveragejson):
        # Writes the CoverageJSON dictionary to a JSON file with indentation
        with open(self.output_path, "w") as f:
            json.dump(coveragejson, f, indent=2)


# Main function to orchestrate the conversion process
def main():
    csv_path = "input_csv_data.csv"       # Input CSV file path
    output_path = "coverage.json"         # Output JSON file path

    # Step 1: Read CSV data
    reader = CSVReader(csv_path)
    data = reader.read_data()

    # Step 2: Extract relevant fields
    extractor = CoverageDataExtractor(data)
    extracted_data = extractor.extract()

    # Step 3: Build CoverageJSON structure
    builder = CoverageJSONBuilder(extracted_data)
    coveragejson = builder.build()

    # Step 4: Write CoverageJSON to file
    writer = CoverageJSONWriter(output_path)
    writer.write(coveragejson)

# Entry point of the script
if __name__ == "__main__":
    main()
