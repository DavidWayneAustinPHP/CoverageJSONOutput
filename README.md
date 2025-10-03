This is a backend service for a weather analytics platform. 
The Python 3.11 application "converter_csv_to_CoverageJSON.py" reads csv file " input_csv_data.csv" containing weather data.
The data read in from the cvs file is then convereted to a ConverageJSON file called "coverage.json"
CoverageJSON is a standard format for representing meteorological data. 

More information can be found in the followng URL: https://covjson.org/.

* To run this application have python version 3.11 installed on the PC
And run the command in a terminal window {Powershell, CMD or Git Bash}
python .\converter_csv_to_CoverageJSON.py
The python program will read in the example csv file and create the ConverageJSON file called: coverage.json

* To test the ConverageJSON data, copy the JSON code from the file converage.json and place in the window of the URL: https://covjson.org/playground/
This website will test the health of the JSON code and report any errors.

A sucessful test of the application can be see in the file: "SuccessFullTest_JSONcode.png"
