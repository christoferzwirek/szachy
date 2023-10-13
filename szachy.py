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
user=input("podaj nazwę użytkownika ")#AinsOowl
#ile_gier=input("podaj ile gier ")

games=client.games.export_by_player(user,max=3,perf_type='rapid')#
games1 = list(games)
game_id = games1[0]['id']
pgn=client.games.export(game_id,as_pgn=True)

# Ścieżka do pliku wykonywalnego Stockfisha
stockfish_path = "stockfish/stockfish-windows-x86-64.exe"
# Utwórz obiekt silnika szachowego
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

import io

# Pozycja, którą chcesz zanalizować
game= chess.pgn.read_game(io.StringIO(pgn))

# Inicjalizuj planszę
board = game.board()
result=[]
# Iteruj przez ruchy gry i analizuj każdą pozycję
for ply,move in enumerate(game.mainline_moves()):
    board.push(move)

    if ply ==20:
        break
    analysis = engine.analyse(board, chess.engine.Limit(time=0.5))
    #result.append(analysis.score)
    # Wyświetl lub zapisz wyniki analizy dla każdego ruchu
    print(f"Move: {move}, Evaluation: {analysis['score']}")  # Limit czasowy analizy (np. 0.1 sekundy)
    
#best_move = info.get("pv", [])[0]
#print("Najlepszy ruch:", best_move)
#print("Ocena pozycji:", info["score"])

# Zamknij silnik szachowy po zakończeniu
engine.quit()

"""
for słownik in games1:
    for klucz, wartość in słownik.items():
        if(klucz=='speed'):
            print(f"\ntępo: {wartość}")
        if(klucz=='moves'):
            print(f"ruchy: {wartość}")
"""        