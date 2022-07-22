import socket
import time
import json

TICK_RATE = 0.3
SERVER = "192.168.8.136"
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
EXIT_MSG = "Az!DaKYJ,2LvN=]s{R@];4))#Aj-hub<tuP4D+^S8RN,Yb+r_+"

SUMMONER_NAME = "GrelsoN21"
ALL_GAME_DATA_URL = "liveclientdata/allgamedata"
ACTIVE_PLAYER_URL = "liveclientdata/activeplayer"
SCORES_URL = "liveclientdata/playerscores?summonerName="
REQUEST_QUEE = [ACTIVE_PLAYER_URL, SCORES_URL+SUMMONER_NAME]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def msg_to_json(msg):
    try:
        msg_json = json.loads(msg)
        print("[CONVERTED] Messaeg has been converted to json.")
        return msg_json
    except ValueError:
        print("[ERROR] Error.")
        return ''


def extract_game_data(msg, data_type):
    game_data = msg_to_json(msg)
    try:
        if data_type == REQUEST_QUEE[0]:
            champ_health_percentage = game_data['championStats']['currentHealth']/game_data['championStats']['maxHealth']
            print("Champ health =" + champ_health_percentage + "%")
            print(game_data['currentGold'])
        elif data_type == REQUEST_QUEE[1]:
            print(game_data)
            calculate_score_change(game_data)
            
    except:
        print("[ERROR] Game data reed error.")

def calculate_score_change(scores):
    

def request_data(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("[SEND] Request has ben send")
    
    if msg != EXIT_MSG:
        time.sleep(TICK_RATE)
        recive_data(msg)

def recive_data(data_type):
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)    
        if msg != "" and msg != "{}":
            extract_game_data(msg, data_type)

def start():
    try:
        while True:
            for request in REQUEST_QUEE:
                request_data(request)
    except KeyboardInterrupt:
        request_data(EXIT_MSG)



print("[STARTING] Client is starting....")
start()