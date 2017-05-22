#################################################################
##     Electric Usage Conditioner Monitoring - Web Server      ##
#################################################################
from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/')
def Index():
    return 'Electric Usage Conditioner Monitoring - Web Server'

@app.route('/updatestatus', methods=['POST'])
def UpdateStatus():
    room_id = request.args.get('id', '')
    status = request.args.get('status', '')
    return 'Room {}: Update status -to->{}'.format(room_id, status)

#+-----------------------------------------------------+#
#|                  Start-Up Statement                 +#
#+-----------------------------------------------------+#
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)