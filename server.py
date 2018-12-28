__author__ = 'Levi'

from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
import data_stores as data
import os
import time
import test_class as tc
import Web_classes as wc

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
    players = ['Levi', 'Lex', 'Eric']
    gplay = tc.League()
    gplay.build_players(players, 20)
    gplay.build_candidates(data.candidates, data.stock_price_modifiers)
    gplay.build_states()

    game_people = []
    for player in gplay.player_names:
        game_people.append(gplay.players[player].get_web_class())
        print(game_people)

    game_candidates = []
    for candidate in gplay.candidate_names:
        game_candidates.append(gplay.candidates[candidate].get_web_class())
        print(game_candidates)

    upcoming_primaries = [wc.Primary_Table('Febuary 2nd, 2018', 'Iowa', '30')]

    # TODO maybe we should get candidate info from json? Is there added value from getting it from the class?
    return render_template('index.html', upcoming_primaries = upcoming_primaries, people=game_people,candidates=game_candidates)


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
