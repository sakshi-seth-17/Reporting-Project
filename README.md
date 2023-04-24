 # Daily Reporting App
                                                            
This application is built using Python's streamlit package to show observations captured by RPIs on a day to day basis. It shows information about temperature, humidity and brightness in the form of graph and Images in the form of grid in a time range of 12AM-6AM, 6AM-12PM, 12PM-6PM and 6PM-12AM.

---

### Flow of the application:
<img src="https://github.com/sakshi-seth-17/Reporting-Project/blob/main/Sensor-Daily-Report.jpg" alt="Alt text" title="Optional title">

### Instructions
1. Clone this repository. \
`git clone https://github.com/sakshi-seth-17/Reporting-Project.git`

2. Make neccessary changes required in the app.py wrt specific path. \

3. Travel to the parent project directory and install the required python packages. \
`Create virtual environment – python3 -m venv venv` \
`source venv/bin/activate` \
`pip3 install -r requirement.txt` \
`To check if application is working fine run – streamlit run app.py` \
`use the link from the cmd and check on browser` \

### Create service file to make the app run indefinitely
`sudo nano /lib/systemd/system/dailyreport.service` \
Paste below lines inside the file by making necessary changes \
[Unit] \
Description=Daily Report Service \
After=multi-user.target 


[Service] \
User=webserver \
Type=idle \
ExecStart=/var/www/aspendb/probesearch/Reporting-Project/venv/bin/streamlit run /var/www/aspendb/probesearch/Reporting-Project/app.py \
Restart=on-failure 


[Install] \
WantedBy=multi-user.target 

`sudo chmod 644 /lib/systemd/system/dailyreport.service` \
`sudo systemctl enable dailyreport.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start dailyreport.service` \
`sudo systemctl status dailyreport.service` \

---
### Location details of the components:
•	Application code path (on webserver - webserver@128.192.158.63): /var/www/aspendb/probesearch/Reporting-Project
•	Active RPI details can be found https://console.firebase.google.com/u/2/project/rpi-dataset/firestore/data/~2FRPI-details~2Fblackbox
•	Centralized Local database (on webserver - webserver@128.192.158.63) path: /var/www/aspendb/probesearch/SensorsData

---
### Technical details:
•	The application is built using Python’s Streamlit package.
•	The application can be accessed using link - http://128.192.158.63:8501/
•	It runs on port – 8501.

---
### How to register a new RPI to this application?
•	Add the query in the config file by referring to the older query to get data from the database. Note: The name of columns should be same as mentioned in the older query.

---
### Folder Structure
- venv/
- static/
- app.py
- config.json
- userdefined.py
- requirement.txt
	
