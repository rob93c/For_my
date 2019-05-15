#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by Roberto Cella
# For any question mail me at rob.uniuc@gmail.com

"""
Scrivere le uscite ogni settimana, con cronologia
Scrivere i litri di latte usati e moltiplicarli * 0.4, aggiungendoli alle spese
Tenere conto dei litri (quanti litri ho usato finora?)
Vedere le entrate al netto delle spese
Grafico:
	x = tempo, y = soldi guadagnati
    x = tempo, y = litri lavorati
	- sovrapposizione dei due grafici
"""
import sys
import csv
import datetime
import plotly
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
from pynput.keyboard import Key, Controller
from summer import summer
from functools import lru_cache


class For_my:

    @lru_cache(maxsize=64)
    def main(self):
        path = Path("data.csv")
        sys.tracebacklimit = 0
        keyboard = Controller()
        while True:
            print("""
Benvenuto in For_my, scegli un'opzione:

1) Registra le uscite settimanali, litri lavorati e introiti
2) Vedi la cronologia delle spese
3) Vedi la cronologia del latte lavorato
4) Vedi le entrate nette
5) Crea il grafico (latte e soldi guadagnati in relazione al tempo)
0) Chiudi il programma
		    """)
            choice = input()
            if choice == "1":  # imposta uscite, litri lavorati e introiti
                with path.open("a") as op:
                    writer = csv.writer(op)
                    writer.writerow([f"{datetime.datetime.now():%d-%m-%Y}", input(
                        "Quanto hai speso questa settimana? "), input(
                        "Quanti litri di latte hai lavorato? "), input(
                        "Quanto hai guadagnato questa settimana? ")
                    ])
            elif choice == "2":  # cronologia spese
                print(f"\nLe spese totali sono state di {summer(1)}€.")
            elif choice == "3":  # cronologia latte
                print(f"\nHai usato un totale di {summer(2)} litri.")
            elif choice == "4":  # entrate
                gain = summer(3) - summer(1) - summer(2) * 0.4
                print(f"\nHai guadagnato un netto di {gain}0€")
            elif choice == "5":  # grafico
                df = pd.read_csv("data.csv")

                trace_high = go.Scatter(
                    x=df.Date,
                    y=df["Guadagno"],
                    name="Soldi guadagnati",
                    line=dict(color='#57E53D'),
                    opacity=0.8)

                trace_low = go.Scatter(
                    x=df.Date,
                    y=df["Latte usato"],
                    name="Litri di latte",
                    line=dict(color='#17BECF'),
                    opacity=0.8)

                plotly.offline.plot({
                    "data": [trace_high, trace_low],
                    "layout": go.Layout(title="Guadagni e litri usati:")
                }, auto_open=True, filename='graph.html')

            elif choice == "0":  # chiusura
                keyboard.press(Key.alt)
                keyboard.press(Key.f4)
                keyboard.release(Key.f4)
                keyboard.release(Key.alt)
            else:
                raise ValueError(
                    "Inserisci il numero corrispondente all'azione desiderata.")
            loop = input(  # ripeti ciclo
                "\nDesideri continuare a usare l'applicazione?\n(Premi \"s\" per continuare)\n")
            if loop == "s" or loop == "S":
                continue
            else:
                break


For_my().main()
