__author__ = 'Levi'

from flask import Flask, render_template, request, send_from_directory, g, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_oidc import OpenIDConnect
import data_stores as data
import os
import time
import test_class as tc
import auth_secrets as aus
import Web_classes as wc
import primary_results as testdata
from okta import UsersClient


app = Flask(__name__)
Bootstrap(app)
oidc, okta_client = aus.run_config(app)

players = ['Levi', 'Lex', 'Eric']
gplay = tc.League()
gplay.build_players(players, 20)
gplay.build_candidates(data.candidates, data.stock_price_modifiers)
gplay.build_states()
gplay.update_state_data("Iowa", testdata.iowa)



@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(str(oidc.user_getfield("sub")))
    else:
        g.user = None


@app.route('/favicon.ico')
def favicon():
    print(os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=['GET', 'POST'])
@oidc.require_login
def hello():
    user_ip = request.remote_addr
    with open('Server_Log_File.log', 'w') as logfile:
            logfile.write("Got connection from user at IP address: " + user_ip + " at time: " +
                          time.strftime("%c") + "\n")


    print(g.user)
    print(g.user.profile.firstName)
    game_people = []
    for player in gplay.player_names:
        game_people.append(gplay.players[player].get_web_class())

    game_candidates = []
    for candidate in gplay.candidate_names:
        game_candidates.append(gplay.candidates[candidate].get_web_class())

    upcoming_primaries = [wc.Primary_Table('Febuary 2nd, 2018', 'Iowa', '30')]


    # TODO maybe we should get candidate info from json? Is there added value from getting it from the class?
    return render_template('index.html', upcoming_primaries = upcoming_primaries, people=game_people,
                           candidates=game_candidates)


@app.route('/home', methods=['GET', 'POST'])
@oidc.require_login
def index():
    a = request.remote_addr
    with open('Server_Log_File.log', 'a') as logfile:
            logfile.write("Got connection from user at IP address: " + a + " at time: " +
                          time.strftime("%c") + " username created: " + " animal chosen: "  + "\n")
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    user_ip = request.remote_addr
    with open('Server_Log_File.log', 'w') as logfile:
        logfile.write("Got connection from user at IP address: " + user_ip + " at time: " +
                      time.strftime("%c") + "\n")
    return render_template('login.html')


@app.route("/logout")
def logout():
    a=1
    oidc.logout()
    return redirect(url_for(".hello"))


@app.route('/userprofile', methods=['GET', 'POST'])
@oidc.require_login
def userprofile():
    a = request.remote_addr
    with open('Server_Log_File.log', 'a') as logfile:
            logfile.write("Got connection from user at IP address: " + a + " at time: " +
                          time.strftime("%c") + " username created: " + " animal chosen: "  + "\n")

    # We are going to hard code this in as lex - we need to add a login function
    # TODO add login - remove hardcoding

    # TODO - I shouldn't need to do this everytime
    players = ['Levi', 'Lex', 'Eric']
    gplay = tc.League()
    gplay.build_players(players, 20)
    gplay.build_candidates(data.candidates, data.stock_price_modifiers)
    gplay.build_states()
    gplay.update_state_data("Iowa", testdata.iowa)

    user = gplay.players['Lex'].get_web_class()

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
