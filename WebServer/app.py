#################################################################
##     Electric Usage Conditioner Monitoring - Web Server      ##
#################################################################
import sys
sys.path.insert(0, '../')
from flask import Flask, request, send_from_directory, render_template, jsonify
from models import *
import psycopg2
import time

app = Flask(__name__, static_folder='statics')


#+-----------------------------------------------------+#
#|                  Static file's URL                  +#
#+-----------------------------------------------------+#

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder + '/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.static_folder + '/css', path)

#+-----------------------------------------------------+#
#|                  Webserver's Views                  +#
#+-----------------------------------------------------+#

@app.route('/')
def Index():
    devices = session.query(Device).all()
    return render_template('index.html', devices=devices)

@app.route('/updatestatus', methods=['POST'])
def UpdateStatus():
    deviceid = request.args.get('id').lower()
    status = request.args.get('status').lower()
    a_status = request.args.get('aircon').lower()
    try:
        device = session.query(Device).get(deviceid)
        s = True if status == 'on' else False
        a = True if a_status == 'on' else False
        device.update(s, a)
        print('Room {}: Update status -to->{} and AIRCON\"{}\"'.format(deviceid, status, a_status))
        return(str(device.last_update))
    except:
        return "Your Device \"{}\" is not registered, please register it add url/register".format(deviceid)

@app.route('/json')
def GetJsonData():
    devices = session.query(Device).all()
    return jsonify({device.id : device.serialize for device in devices})

@app.route('/register', methods=['GET', 'POST'])
def RegisterPage():
    if request.method == 'POST':
        deviceid = request.form.get('deviceid').lower()
        if(deviceid == ""):
            noti = {
                        'type': 'is-danger',
                        'content': 'Please enter device is (You\'re not entered your device id)'
                }
        else:
            try:
                device = session.query(Device).filter_by(id = deviceid).one()
                noti = {
                        'type': 'is-danger',
                        'content': 'The Deivce is \"' + deviceid + '\" is already exist please enter new device id'
                }
            except:
                d = Device(deviceid)
                session.add(d)
                session.commit()
                noti = {
                            'type': 'is-success',
                            'content': 'Your device ID \"' + deviceid + '\" is registered successfully'
                    }
        return render_template('register.html', noti=noti)
    return render_template('register.html')

#+-----------------------------------------------------+#
#|                  Start-Up Statement                 +#
#+-----------------------------------------------------+#
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, )#threaded=True)