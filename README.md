# Reporting-Project
Sensor-Daily-Report
1.	Flow of the application:
 

2.	Location details of the components:
•	Application code path (on webserver - webserver@128.192.158.63): /var/www/aspendb/probesearch/Reporting-Project
•	Active RPI details can be found here
•	Centralized Local database (on webserver - webserver@128.192.158.63) path: /var/www/aspendb/probesearch/SensorsData

3.	Technical details:
•	The application is built using Python’s Streamlit package.
•	The application can be accessed using link - http://128.192.158.63:8501/
•	It runs on port – 8501.
•	To check status or start or stop or restart the service of the application use below command on the webserver:
o	sudo systemctl status dailyreport
o	sudo systemctl start dailyreport
o	sudo systemctl stop dailyreport
o	sudo systemctl restart dailyreport
•	The above service file can be found at: 
o	sudo nano /lib/systemd/system/dailyreport.service

4.	How to register a new RPI to this application?
•	Add the query in the config file by referring to the older query to get data from the database. Note: The name of columns should be same as mentioned in the older query.

5.	Application Summary:
•	This application is built to get daily observations of the sensor data like temperature, humidity, brightness, and images.

6.	GitHub link

7.	Follow below steps to setup this application:
•	Download code from GitHub.
•	Create virtual environment – python3 -m venv venv
•	Next, source venv/bin/activate
•	Next, pip3 install -r requirement.txt
•	To check if application is working fine run – streamlit run app.py

