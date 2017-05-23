# Electric Usage Conditioner Monitoring 
This project was submitted to Embedded System subject, 2/2016

Department of Computer Engineering, Faculty of Engineering, King
Mongkut's Institute of Technology Ladkrabang

# Getting Started
## Install
### NodeMCU Part
- Download Arduino IDE from [Arduino's Website](https://www.arduino.cc/) and install it
- Add NodeMCU Boards to Arduino IDE [Magesh Jayakumar's Quick Start Guides on Instructables](http://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/)
### WebServer Part
- Download Python 3.6.1  form [Python.org](https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe)
- Download some python package using pip3
```
    $ pip3 install -r WebServer\requirement.txt 
```
**Database**
- Download and Install [PostgreSQL](https://www.postgresql.org/)
    * you can change the command below and update the database information in /WebServer/settings.py
```
    $ psql -U postgres
    $ CREATE DATABASE euc_monitoring;
    $ CREATE USER euc_user WITH PASSWORD 'fhewwwww~~';
    $ GRANT ALL PRIVILEGES ON DATABASE euc_monitoring TO euc_user;
```
## To Run
### NodeMCU Part
- Edit some setting on sketch/sketch.ino

```
    Line 4: YOUR_WIFI_SSID
    Line 5: YOUR_WIFI_PASSWORD
    Line 7: YOUR_SERVER_IPADDRESS
    Line 11: YOUR_SERVER_HOST
```

- (Server's ip address can check by command below)

Linux
```
    $ ifconfig
```
Windows
```
    $ ipconfig
```

- Upload the edited code from sketch/sketch.ino to your nodemcu boards and connect the circuit below
```
    Pin3 ~ Aircon[OUTPUT] (LED)
    Pin4 ~ Aircon[INPUT] (Switch)
    Pin7 ~ Main Switch[OUTPUT] (LED)
    Pin8 ~ Main Switch[INPUT] (Switch)
```

### WebServer Part

Run webserver by the command below

```
    $ python WebServer\app.py
```
