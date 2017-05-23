#################################################################
##     Electric Usage Conditioner Monitoring - Web Server      ##
#################################################################
import sys
sys.path.insert(0, '../')
from flask import Flask, request, send_from_directory, render_template
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
    return 'Electric Usage Conditioner Monitoring - Web Server'

@app.route('/updatestatus', methods=['POST'])
def UpdateStatus():
    room_id = request.args.get('id', '')
    status = request.args.get('status', '')
    a_status = request.args.get('aircon', '')
    return 'Room {}: Update status -to->{} and AIRCON\"{}\"'.format(room_id, status, a_status)

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
    app.run(debug=True, host='0.0.0.0', port=80)