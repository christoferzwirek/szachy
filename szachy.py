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
import chess.polyglot
import berserk
import pandas as pd
import io
import time



session = berserk.TokenSession("lip_4M09fZ192Ysehbmnhh26")

client = berserk.Client(session=session)

#profiler
def is_move_in_opening_book(board, move, opening_book_path):
    #start2=time.time()
    with chess.polyglot.open_reader(opening_book_path) as reader:
        for entry in reader.find_all(board):
            if entry.move == move:
                #print(entry)
                
                return True
    
    return False


def checkmiss(user):
    
    # Ścieżka do pliku wykonywalnego Stockfisha
    stockfish_path = "stockfish/stockfish-windows-x86-64.exe"
    opening_book_path = "komodo.bin"
    # Utwórz obiekt silnika szachowego
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    
    
    a2 = None 
    games=client.games.export_by_player(user,max=10,perf_type='rapid',opening=True)#
    
    games1 = list(games)
    result=[]
    l=0
    for i in range(len(games1)):
        game_id = games1[i]['id']
        pgn=client.games.export(game_id,as_pgn=True) 
        
        # Pozycja, którą chcesz zanalizować
        game= chess.pgn.read_game(io.StringIO(pgn))
        headers = {key: value.lower() for key, value in game.headers.items()}
        #print(headers)
        game2= chess.pgn.read_game(io.StringIO(pgn))
        headers = {key: value.lower() for key, value in game2.headers.items()}
        preocena=0
        ocena =0
        board2 = game2.board()
        # Inicjalizuj planszę
        board1 = game.board()
        #print("\n")
        # Iteruj przez ruchy gry i analizuj każdą pozycję
        b=0
        
        for ply,move in enumerate(game.mainline_moves()):
            if l==10:
                #pass
                
                print("git",b)
                #break
                
            if move==chess.Move.from_uci("e2e4"):
                b=b+1
            if move==chess.Move.from_uci("e7e5"):
                b=b+1
                
            #print(b,move,ply)
            if b!=2 and ply>1:
                #l=l+1
                #break
                pass
            if ply==2:
                #l=l+1
                pass
            if ply ==23:#kończenie debiutu
               break
            a2_local = a2 
            if is_move_in_opening_book(board1, move, opening_book_path):
                #print(f"{move} is in opeingn book")
                board1.push(move)
                board2.push(move)
            else:
                
                board1.push(move)
                
                #print(move)
                analysis = engine.analyse(board1, chess.engine.Limit(time=0.5)) # Limit czasowy analizy (np. 0.1 sekundy)
                
                #result.append(analysis.score)
                # Wyświetl lub zapisz wyniki analizy dla każdego ruchu
                if headers['White'] == user.lower():
                    info =analysis['score']
                    ocena=info.white()
                elif headers['Black'] == user.lower():
                    info =analysis['score']
                    ocena=info.black()
                else:
                    #print(headers['White'])
                    #print('ja ',user)
                    print(f"{user} is not part of this game or their color is not specified in PGN headers.")
                #print(ocena)
                #print
               
                if isinstance(ocena, chess.engine.Mate) or ocena== chess.engine.MateGiven:
                # Handle mate score, for example, set preocena to a large value
                   preocena = 10000 if ocena.mate() > 0 else -10000
                   #print(ocena.mate())
                   ocena.cp=ocena.mate()
                   
                  # ocena.cp=0
                #print(f"ocena {ocena.cp},pporzednia ocena {preocena}")
                if preocena-ocena.cp>200:
                    #print(f"ocena {ocena.cp},pporzednia ocena {preocena}")
                    #print(preocena-ocena.cp)
                    #print(f"Move: {move}, Evaluation: {analysis['score']}")
                    
                    best_move = a2_local.get("pv", [])[0]

                    #print("Best Move:", best_move)
                    #print(game_id)
                    result.append((board2.fen(),move,best_move))
                a2 = analysis
                #print(a2)
                preocena=ocena.cp
                board2.push(move)
        #best_move = info.get("pv", [])[0]
        #print("Najlepszy ruch:", best_move)
        #print("Ocena pozycji:", info["score"])
        
        # Zamknij silnik szachowy po zakończeniu
    engine.quit()
    return result

from collections import Counter


def most_common_moves(games):
    
    counter = Counter(games)
    most_common = counter.most_common()
    return most_common

if __name__ == '__main__':
    
    #user=input("podaj nazwę użytkownika ").lower()#AinsOowl
    #ile_gier=input("podaj ile gier ")
    user="radek8640"
    start=time.time()
    games=checkmiss(user)
    stop=time.time()
    executio= stop - start
    
    #print(games)


    # Przykładowe użycie:
    # games to lista tupli (pozycja FEN, ruch)
    #games = [(fen1, move1), (fen2, move2), ...]
    most_common = most_common_moves(games)
    #print(most_common)
    # Wyświetl czas wykonania
    print(f"Czas wykonania programu: {executio:.2f} sekundy")
 
    """
    for fen,m in result:
        print(m) 
    """
   