# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:03:14 2023

@author: radek
"""


import berserk

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
a=client.account.get_email()
print(f"{a}")
user=input("podaj nazwę użytkownika ")#AinsOowl
ile_gier=input("podaj ile gier ")
games=client.games.export_by_player(user,max=ile_gier)
games1 = list(games)
game_id = games1[0]['id']
pgn=client.games.export(game_id,as_pgn=True)

for słownik in games1:
    for klucz, wartość in słownik.items():
        if(klucz=='speed'):
            print(f"\ntępo: {wartość}")
        if(klucz=='moves'):
            print(f"ruchy: {wartość}")