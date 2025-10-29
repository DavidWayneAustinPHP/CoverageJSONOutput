
import unittest
from unittest.mock import mock_open, patch
import json

# Import your classes here
from converter_csv_to_CoverageJSON import (
    CSVReader,
    CoverageDataExtractor,
    CoverageJSONBuilder,
    CoverageJSONWriter
)

# Sample CSV content for mocking
MOCK_CSV_CONTENT = """time,longitude,latitude,temperature
2023-01-01T00:00:00Z,-3.0,51.0,280.5
2023-01-01T01:00:00Z,-3.0,51.0,281.0
"""

class TestCoverageJSONConversion(unittest.TestCase):

    def test_csv_reader(self):
        # Mock opening the file and reading CSV content
        with patch("builtins.open", mock_open(read_data=MOCK_CSV_CONTENT)):
            reader = CSVReader("input_csv_data.csv")
            data = reader.read_data()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['time'], "2023-01-01T00:00:00Z")

    def test_data_extraction(self):
        # Simulate parsed CSV data
        mock_data = [
            {"time": "2023-01-01T00:00:00Z", "longitude": "-3.0", "latitude": "51.0", "temperature": "280.5"},
            {"time": "2023-01-01T01:00:00Z", "longitude": "-3.0", "latitude": "51.0", "temperature": "281.0"}
        ]
        extractor = CoverageDataExtractor(mock_data)
        extracted = extractor.extract()
        self.assertEqual(extracted["longitude"], -3.0)
        self.assertEqual(extracted["latitude"], 51.0)
        self.assertEqual(extracted["temperatures"], [280.5, 281.0])

    def test_json_builder(self):
        extracted_data = {
            "times": ["2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z"],
            "longitude": -3.0,
            "latitude": 51.0,
            "temperatures": [280.5, 281.0]
        }
        builder = CoverageJSONBuilder(extracted_data)
        coveragejson = builder.build()
        self.assertEqual(coveragejson["type"], "Coverage")
        self.assertEqual(coveragejson["domain"]["axes"]["x"]["values"], [-3.0])
        self.assertEqual(coveragejson["ranges"]["temperature"]["values"], [280.5, 281.0])

    def test_json_writer(self):
        # Create a simple CoverageJSON object
        coveragejson = {"type": "Coverage", "dummy": True}
        with patch("builtins.open", mock_open()) as mocked_file:
            writer = CoverageJSONWriter("output.json")
            writer.write(coveragejson)
            mocked_file().write.assert_called()  # Check that write was called

if __name__ == "__main__":
    unittest.main()

