
import csv
import json

class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)


class CoverageDataExtractor:
    def __init__(self, data):
        self.data = data

    def extract(self):
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


class CoverageJSONWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, coveragejson):
        with open(self.output_path, "w") as f:
            json.dump(coveragejson, f, indent=2)


# Example usage
def main():
    csv_path = "input_csv_data.csv"
    output_path = "coverage.json"

    reader = CSVReader(csv_path)
    data = reader.read_data()

    extractor = CoverageDataExtractor(data)
    extracted_data = extractor.extract()

    builder = CoverageJSONBuilder(extracted_data)
    coveragejson = builder.build()

    writer = CoverageJSONWriter(output_path)
    writer.write(coveragejson)

if __name__ == "__main__":
    main()
