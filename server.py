__author__ = 'Levi'

from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
import os
import time


app = Flask(__name__)
Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    print(os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=['GET', 'POST'])
def hello():
    user_ip = request.remote_addr
    with open('Server_Log_File.log', 'w') as logfile:
            logfile.write("Got connection from user at IP address: " + user_ip + " at time: " +
                          time.strftime("%c") + "\n")
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def index():
    a = request.remote_addr
    with open('Server_Log_File.log', 'a') as logfile:
            logfile.write("Got connection from user at IP address: " + a + " at time: " +
                          time.strftime("%c") + " username created: " + " animal chosen: "  + "\n")
    return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
