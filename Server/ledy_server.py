import requests
import socket
import threading
import json
import time
import os

BASE_URL = 'https://127.0.0.1:2999/'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6060
ADDR = (HOST, PORT)
HEADER = 64
FORMAT = 'utf-8'
EXIT_MSG = "Az!DaKYJ,2LvN=]s{R@];4))#Aj-hub<tuP4D+^S8RN,Yb+r_+"
SUMMONER_NAME = "GrelsoN21"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def save_json_file(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def reed_file(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data


def send_msg(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def request_game_data(recived_url):
    try:
       return json.loads(requests.get(BASE_URL + recived_url, verify=False).text)
    except:
        return {}

def on_connection(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        try:
            detect_score_change(request_game_data("liveclientdata/playerscores?summonerName=GrelsoN21"), "scores", conn, addr)
            detect_score_change(request_game_data("liveclientdata/activeplayer"), "activeplayer", conn, addr)
            detect_score_change(request_game_data("liveclientdata/playerlist"), "playerlist", conn, addr)
        except:
            pass
        
        try:
            send_msg("ping_message", conn)
        except:
            connected = False
    print(f"[DISCONNECTED] {addr} disconnected")
    os.remove(os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_scores.json")
    os.remove(os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_activeplayer.json")
    os.remove(os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_playerlist.json")
    

def detect_score_change(game_data, data_type, conn, addr):
    if data_type == "scores":
        
        game_data_file_path = os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_scores.json"

        if os.path.isfile(game_data_file_path):
            old_game_data = reed_file(game_data_file_path)
            if old_game_data != {}:
                if game_data["assists"] > old_game_data["assists"]:
                    send_msg("new assist", conn)
                if game_data["creepScore"] > old_game_data["creepScore"]:
                    send_msg("new creep score", conn)
                if game_data["deaths"] > old_game_data["deaths"]:
                    send_msg("new death", conn)
                if game_data["kills"] > old_game_data["kills"]:
                    send_msg("new kill", conn)
                if game_data["wardScore"] - old_game_data["wardScore"] > 0.2:
                    send_msg("new wardScore", conn)
                
        save_json_file(game_data_file_path, game_data)

    elif data_type == "activeplayer":
        game_data_file_path = os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_activeplayer.json"

        if os.path.isfile(game_data_file_path):
            old_game_data = reed_file(game_data_file_path)
            if old_game_data != {}:
                if game_data["currentGold"] < old_game_data["currentGold"]:
                    send_msg("new purchase", conn)
                if game_data["level"] > old_game_data["level"]:
                    send_msg("level up", conn)
                
        save_json_file(game_data_file_path, game_data)
    
    elif data_type == "playerlist":
        game_data_file_path = os.getcwd() + "\\" + str(addr[0]) + "_" + str(addr[1]) + "_playerlist.json"

        if os.path.isfile(game_data_file_path):
            old_game_data = reed_file(game_data_file_path)
            if old_game_data != {}:
                for summoner in game_data:
                    if summoner["summonerName"] == SUMMONER_NAME:
                        if summoner["respawnTimer"] != 0:
                            send_msg(str(summoner["respawnTimer"]) + " - respawn timer", conn)
                            time.sleep(summoner["respawnTimer"])


                
        save_json_file(game_data_file_path, game_data)

            


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=on_connection, args=(conn, addr))
        thread.start()
        print(f"\r[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start()