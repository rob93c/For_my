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
from time import sleep
from os import system, name
from pynput.keyboard import Key, Controller


class For_my:

    def main(self) -> None:
        # Windows requires a precise file path, i.e.
        # Path("C:\\Users\\user\\Desktop\\For_my\\data.csv")
        path: Path = Path("data.csv") if not Tools.isWin() else Path("\\data.csv")
        sys.tracebacklimit = 0
        keyboard = Controller()
        Tools.logo()
        sleep(2)
        while True:
            Tools.clear()
            print("""
Benvenuto in For_my, scegli un'opzione:

1) Registra le uscite settimanali, litri lavorati e introiti
2) Vedi la cronologia delle spese
3) Vedi la cronologia del latte lavorato
4) Vedi le entrate nette
5) Crea il grafico (latte e soldi guadagnati in relazione al tempo)
0) Chiudi il programma
		    """)
            choice: str = input()
            if choice == "1":  # imposta uscite, litri lavorati e introiti
                with path.open("a") as op:
                    writer = csv.writer(op)
                    writer.writerow([f"{datetime.datetime.now():%d-%m-%Y}", input(
                        "Quanto hai speso questa settimana? "), input(
                        "Quanti litri di latte hai lavorato? "), input(
                        "Quanto hai guadagnato questa settimana? ")
                    ])
            elif choice == "2":  # cronologia spese
                print(f"\nLe spese totali sono state di {Tools.summer(1)}€.")
            elif choice == "3":  # cronologia latte
                print(f"\nHai usato un totale di {Tools.summer(2)} litri.")
            elif choice == "4":  # entrate nette
                gain = Tools.summer(3) - Tools.summer(1) - \
                    Tools.summer(2) * 0.4
                print(f"\nHai guadagnato un netto di {Tools.prettify(gain)}€")
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


class Tools:

    # takes an index and sums every number at that index in a csv file
    @staticmethod
    def summer(index: int) -> int:
        tot: int = 0
        with Path("data.csv").open("r") as op:
            reader = csv.reader(op, delimiter=",")
            data = [line[index] for line in reader if line[index].isdigit()]
            for value in data:
                tot += int(value)
            return tot

    # Windows requires a precise file path, i.e.
    # Path("C:\\Users\\user\\Desktop\\For_my\\data.csv")

    # Takes a float with 13 decimal numbers and returns just the first 2
    @staticmethod
    def prettify(num: float) -> float:
        strnum: str = str(num)
        return float(strnum[:-11])

    # Clears terminal's screen 
    @staticmethod
    def clear() -> None:
        if Tools.isWin(): 
            _ = system("cls")
        else:
            _ = system("clear")

    # Check if the OS is Windows
    @staticmethod
    def isWin() -> bool:
        return name == "nt"

    @staticmethod
    def logo() -> None:
        print("""

                          ---dMMMMMMMMd--.                 
                       .+NMMMMMMMMMMMMMMd                 
                       /MMMMMMMMMMMMMMMMNy-               
                      dNMMMMMMMMMMMMMMMMMMNd              
                      NMMMMMMMMMMMMMMMMMMMMN              
                      NMMMMMMMMMMMMMMMMMMMMN              
                  `d/ NMMMMMo:-----:NMMMMMMMddh`          
                  `MMMdmMMMMMm-`  +MMMMMMMmmMMM`          
                  `MMM+yMMMMMMMy++yMMMMMNso+MMM`          
                  `MMMMMMMMMMMMMMMMMMMMo+ymMMMM`          
                  `MMMMMMMd-dMMMNNMMMd-hmMMMMMM`          
                  `MMMMMMMMMMMMs::sMMMMMMMMMMMM`          
            .ooooooMMMMMMMMMMMMMMMMMMMMMMMMMMMMoooooo.    
            :MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM:    
             `ymMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmy`     
               .ymMMMMMMMMMMMMMMMyyyNMMMMMMMMMMMmy.       
                 :++++MMMMMMMMMMMsssNMMMMMMN++++:         
                      NMMMMMMMMMMMMMMMMMMMMN              
                      hmMMMM:    hhhhmMMMM/               
                       /MMMMy+      +yMMMM/               
                       .:mMMMm      mMMMm:.               
                         dMMMm      mMMMd                 
                         dMMMN//////NMMho                 
                         /sMMMMMMMMMMMM:                  
                          `-dMMMMMMMMd-`                  
               
               """)


For_my().main()
