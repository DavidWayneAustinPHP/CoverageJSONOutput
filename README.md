This is a backend service for a weather analytics platform. 
The Python 3.11 application "converter_csv_to_CoverageJSON.py" reads csv file " input_csv_data.csv" containing weather data.
The data read in from the cvs file is then convereted to a ConverageJSON file called "coverage.json"
CoverageJSON is a standard format for representing meteorological data. 

More information can be found in the followng URL: https://covjson.org/.

* To run this application have python version 3.11 installed on the PC
And run the command in a terminal window {Powershell, CMD or Git Bash}
"python .\converter_csv_to_CoverageJSON.py".
The python program will read in the example csv file and create the ConverageJSON file called: "coverage.json"

* To test the ConverageJSON data, copy the JSON code from the file "converage.json" and place in the window of the URL: https://covjson.org/playground/
This website will test the health of the JSON code and report any errors.

A sucessful test of the application can be see in the file: "SuccessFullTest_JSONcode.png"

----------------------------------------------
Additional tuning of the application is needed 
----------------------------------------------
-- Working python code. 
-- All code in one large python function, no use of classes. 
-- No unit tests. 
-- Reasonable readme 
-- Included a PNG of the successful test in covjson playground 
-- Adding more git history
-- Adding validation 
-- Adding setup.py or similar.

-----------------------------------------------
Running Unit Testing of the code
-----------------------------------------------
One of the following unit testing framewaorks needs to be installed when running the Unit Testing python code
-- pip install pytest   {This is a more powerfull test running}
-- pip install unitest
, beforing running the unit test python script: UnitTest_CoverageJSONOutput.py

To run the unit test code can use the following commands
-- pytest UnitTest_CoverageJSONOutput.py
-- python -m unittest UnitTest_CoverageJSONOutput.py
-- python UnitTest_CoverageJSONOutput.py

---------------------------------------------
Results of running the Unit testing code
---------------------------------------------
Ran the unit test with the following command
--  python UnitTest_CoverageJSONOutput.py

, and the following output was produced:
....
-----------------------------------------------
Ran 4 tests in 0.006s

OK

---------------------------------------------------------------------------------------
Added required validation (Error Handling) to the python code to prevent a code fault in the application
---------------------------------------------------------------------------------------
-- added validation code to python file converter_csv_to_CoverageJSON.py
-- this includes ensuring the CSV contains the expected columns: 'time', 'longitude', 'latitude', 'temperature'. 

---------------------------------------------------------------
Created a setup.py file for the installation of the application
----------------------------------------------------------------
-- file created call setup.py and added to application
-- the application can now be installed locally useing the following commands
    -- pip install .
    -- converagejson-convert
-- Add a check to ensure the file "input_csv_data.csv" exists and is readable
-- Ensure the output path is writable where the output file "coverage.json" can be written
