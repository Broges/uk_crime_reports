# uk_crime_reports
Download your local crime reports and view aggregated crime data (WIP) in your area

!!VERY WIP!!

Downloads a .txt file in JSON format with local crime data for a given month.
control+f to search for specific roads in the downloaded reports

Setup: 
make sure python3 is installed
--Make sure you are in the correct directory first ..\Crime_project
pip install -r requirements.txt
OR
pip install requests


Running:
run report_generator.py in your IDE, alternatively use a terminal:
cd in to correct folder ( cd ..\Crime_project)
python3 -m report_generator.py
follow instructions on screen
report is downloaded to subfolder 'crime_reports'