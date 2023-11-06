# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:03:14 2023

@author: radek
"""

'''
#name=None
import sys

from GUI2 import MyWindow
from PyQt5.QtWidgets import QApplication



app = QApplication(sys.argv)
window = MyWindow()
window.show()



# Create a list to store connections

try:
    sys.exit(app.exec_())
except SystemExit:
    from GUI2 import N
    
print(N)
'''
import chess
import chess.pgn
import chess.engine
import berserk
import pandas as pd
import io
import time
session = berserk.TokenSession("lip_4M09fZ192Ysehbmnhh26")

client = berserk.Client(session=session)

response = client.account.get()
print(response['perfs']['bullet']['rating'])
print(response['perfs']['blitz']['rating'])
print(response['perfs']['rapid']['rating'])

"""
for klucz_zew, dict_wew in response.items():
    print(f"Klucz zewnętrzny: {klucz_zew}")

    if isinstance(dict_wew, dict):
        for klucz_wew, wartość_wew in dict_wew.items():
            print(f"{klucz_wew}")
            print(f" {wartość_wew}")
    else:
        print(f"  Wartość: {dict_wew}")

    print()
"""
#print(session)
#a=client.account.get_email()
#print(f"{a}")


# Ścieżka do pliku wykonywalnego Stockfisha
stockfish_path = "stockfish/stockfish-windows-x86-64.exe"
# Utwórz obiekt silnika szachowego
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)


user=input("podaj nazwę użytkownika ").lower()#AinsOowl
#ile_gier=input("podaj ile gier ")
start=time.time()
games=client.games.export_by_player(user,max=25,perf_type='rapid')#
games1 = list(games)
result=[]
for i in range(len(games1)):
    
    game_id = games1[i]['id']
    pgn=client.games.export(game_id,as_pgn=True)



    
    
    # Pozycja, którą chcesz zanalizować
    game= chess.pgn.read_game(io.StringIO(pgn))
    headers = {key: value.lower() for key, value in game.headers.items()}
    
    preocena=0
    ocena =0
    
    # Inicjalizuj planszę
    board = game.board()
    
    # Iteruj przez ruchy gry i analizuj każdą pozycję
    for ply,move in enumerate(game.mainline_moves()):
        board.push(move)
        #print(move)
        #print(procena)
        if ply ==20:
            break
        analysis = engine.analyse(board, chess.engine.Limit(time=0.5)) # Limit czasowy analizy (np. 0.1 sekundy)
        #result.append(analysis.score)
        # Wyświetl lub zapisz wyniki analizy dla każdego ruchu
        if headers['White'] == user:
            info =analysis['score']
            ocena=info.white()
        elif headers['Black'] == user:
            info =analysis['score']
            ocena=info.black()
        else:
            print(f"{user} is not part of this game or their color is not specified in PGN headers.")
        if preocena-ocena.cp>200:
            #print(f"ocena {ocena.cp},pporzednia ocena {preocena}")
            #print(preocena-ocena.cp)
            #print(f"Move: {move}, Evaluation: {analysis['score']}")     
            result.append((board.fen(),move))
        preocena=ocena.cp
    
    #best_move = info.get("pv", [])[0]
    #print("Najlepszy ruch:", best_move)
    #print("Ocena pozycji:", info["score"])
    
    # Zamknij silnik szachowy po zakończeniu


engine.quit()
stop=time.time()
executio= stop - start

# Wyświetl czas wykonania
print(f"Czas wykonania programu: {executio:.2f} sekundy")

"""
for fen,m in result:
    print(m)
for słownik in games1:
    for klucz, wartość in słownik.items():
        if(klucz=='speed'):
            print(f"\ntępo: {wartość}")
        if(klucz=='moves'):
            print(f"ruchy: {wartość}")
"""        