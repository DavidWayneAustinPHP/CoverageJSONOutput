
import csv
import json
import os

# Class responsible for reading CSV data
class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

            if not data:
                raise ValueError("CSV file is empty or improperly formatted.")

            return data


# Class responsible for extracting relevant data from CSV rows
class CoverageDataExtractor:
    REQUIRED_FIELDS = ['time', 'longitude', 'latitude', 'temperature']

    def __init__(self, data):
        self.data = data

    def validate_row(self, row, index):
        for field in self.REQUIRED_FIELDS:
            if field not in row or row[field].strip() == '':
                raise ValueError(f"Missing or empty field '{field}' in row {index}: {row}")
            if field in ['longitude', 'latitude', 'temperature']:
                try:
                    float(row[field])
                except ValueError:
                    raise ValueError(f"Invalid number format for '{field}' in row {index}: {row[field]}")

    def extract(self):
        for i, row in enumerate(self.data):
            self.validate_row(row, i)

        times = [row['time'] for row in self.data]
        longitudes = [float(row['longitude']) for row in self.data]
        latitudes = [float(row['latitude']) for row in self.data]
        temperatures = [float(row['temperature']) for row in self.data]

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
                    "shape": [len(self.times)],
                    "values": self.temperatures
                }
            }
        }


# Class responsible for writing the CoverageJSON to a file
class CoverageJSONWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, coveragejson):
        try:
            with open(self.output_path, "w") as f:
                json.dump(coveragejson, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to write to {self.output_path}: {e}")


# Main function to orchestrate the conversion process
def main():
    csv_path = "input_csv_data.csv"
    output_path = "coverage.json"

    try:
        reader = CSVReader(csv_path)
        data = reader.read_data()

        extractor = CoverageDataExtractor(data)
        extracted_data = extractor.extract()

        builder = CoverageJSONBuilder(extracted_data)
        coveragejson = builder.build()

        writer = CoverageJSONWriter(output_path)
        writer.write(coveragejson)

        print(f"CoverageJSON successfully written to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()
