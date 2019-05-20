#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Created by Roberto Cella
# For any question mail me at rob.uniuc@gmail.com

"""


                               .:lddddddoc'.                  
                            .;d0NWWNNNNWWWKx:.                
                           .oKWWKkocc:clxKWWXx;               
                          .dXWNk:,:lool:,;xXWWO'              
                          ;0MNk;'lKNWWWXd',dNMKc.             
                          ;0MNd,.;oooooo:.'oXMKl.             
                          'kWWKo.        .cOWM0;. .           
                      .;,..:ONWXx;.     ,dXWWKl..,o:          
                      ;kOl..,dKWWKo.  .c0WWXx;..:OXo.         
                      ,kNXd,..'lk0x,. .dKOo,...l0WXl.         
                      .lXMWKx:'.....   .....:oONWNx,          
                      .;0MMMMNKkdo:.  .:odx0NWMMMKc.          
                 ,dkkkk0NMMMMMMMMM0:..,0MMMMMMMMMN0kkkkd:.    
                 ;ONMMMMMMMMMMMMMMK:..,0MMMMMMMMMMMMMMW0c.    
                  'l0NWMMMMMMMMMMM0:..,OWMMMMMMMMMMMW0o,.     
                    .;loodONMMMMWKd'. .,:cld0NNKkdol:.        
                         .;0WNXXKxc,'''.''':xX0c.             
                          .xXO:'..';looddoclkXO'              
                           ;k0l.          .:OOl.              
                            ;x0d.        .l00l.               
                             ,O0c.       ;O0c.                
                             .kKl.      .:0k'                 
                             .o0k:......;dKx.                 
                              .lkOkxxkxkOko,                  
                               .';cloooc:'.                   


         DEVELOPED BY ROBERTO CELLA FOR AZIENDA AGRICOLA TRENTINA

"""

import os, sys, csv, datetime, plotly
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
from time import sleep
from os import system, name
from pynput.keyboard import Key, Controller


class For_my:

    @classmethod
    def main(cls) -> None:
        dirname = os.path.dirname(os.path.abspath(__file__))
        path = Path(os.path.join(dirname, "data.csv"))
        sys.tracebacklimit = 0
        keyboard = Controller()
        Tools.logo()
        Tools.remove_blanks()
        sleep(2)
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
        while True:
            choice: str = input()
            if choice == "1":  # imposta uscite, litri lavorati e introiti
                with path.open("a") as op:
                    writer = csv.writer(op)
                    writer.writerow([f"{datetime.datetime.now():%d-%m-%Y}", input(
                        "Quanto hai speso questa settimana? "), input(
                        "Quanti litri di latte hai lavorato? "), input(
                        "Quanto hai guadagnato questa settimana? ")
                    ])
            elif choice == "2":  # calcola le spese totali
                print(f"\nLe spese totali sono state di {Tools.summer(1)}€.\n")
            elif choice == "3":  # calcola il latte usato in totale
                print(f"\nHai usato un totale di {Tools.summer(2)} litri.\n")
            elif choice == "4":  # calcola le entrate nette
                gain: float = Tools.summer(3) - Tools.summer(1) - \
                    Tools.summer(2) * 0.4
                print(f"\nHai guadagnato un netto di {Tools.prettify(gain)}€\n")
            elif choice == "5":  # genera il grafico
                df = pd.read_csv(path)

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
                }, auto_open=True, filename='grafico.html')
                sleep(2)
            elif choice == "0":  # chiusura
                keyboard.press(Key.alt)
                keyboard.press(Key.f4)
                keyboard.release(Key.f4)
                keyboard.release(Key.alt)
            else:
                print("Inserisci il numero corrispondente all'azione desiderata.\n")
#            loop = input(  # ripeti ciclo
#                "\nDesideri continuare a usare l'applicazione?\n(Premi \"s\" per continuare)\n")
#            if loop == "s" or loop == "S":
#                continue
#            else:
#                break


class Tools:

    # takes an index and sums every number at that index in a csv file
    @staticmethod
    def summer(index: int) -> int:
        dirname = os.path.dirname(os.path.abspath(__file__))
        path: Path = Path(os.path.join(dirname, "data.csv"))
        tot: int = 0
        with open(path, "r", newline="") as op:
            reader = csv.reader(op, delimiter=",")
            data = [line[index] for line in reader if line[index].isdigit()]
            for value in data:
                tot += int(value)
            return tot

    # Takes an index and sums all the numbers at that index in a csv file
    @staticmethod
    def prettify(num: float) -> str:
        strnum: list = str(num).split(".")
        bef: str = strnum[0]
        if len(strnum) <= 1:
            return f"{bef}.00"
        else:
            aft: str = strnum[1]
            if len(aft) > 1:
                return f"{bef}.{aft[:2]}"
            elif len(aft) == 1:
                return f"{bef}.{aft[:1]}0"
            else:
                return f"{bef}.00"

    # removes every blank line in excess from the .csv file
    @staticmethod
    def remove_blanks() -> None:
        dirname: str = os.path.dirname(os.path.abspath(__file__))
        path: Path = Path(os.path.join(dirname, "data.csv"))
        with open(path, "r") as op:
            lines: list = op.readlines()  # read lines in memory
        with open(path, "w") as op:  # re-write everything from the beginning
            for line in lines:
                if line != "\n":
                    op.write(line)
                else:
                    continue

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

    # Prints the logo
    @staticmethod
    def logo() -> None:
        print("""


                               .:lddddddoc'.                  
                            .;d0NWWNNNNWWWKx:.                
                           .oKWWKkocc:clxKWWXx;               
                          .dXWNk:,:lool:,;xXWWO'              
                          ;0MNk;'lKNWWWXd',dNMKc.             
                          ;0MNd,.;oooooo:.'oXMKl.             
                          'kWWKo.        .cOWM0;. .           
                      .;,..:ONWXx;.     ,dXWWKl..,o:          
                      ;kOl..,dKWWKo.  .c0WWXx;..:OXo.         
                      ,kNXd,..'lk0x,. .dKOo,...l0WXl.         
                      .lXMWKx:'.....   .....:oONWNx,          
                      .;0MMMMNKkdo:.  .:odx0NWMMMKc.          
                 ,dkkkk0NMMMMMMMMM0:..,0MMMMMMMMMN0kkkkd:.    
                 ;ONMMMMMMMMMMMMMMK:..,0MMMMMMMMMMMMMMW0c.    
                  'l0NWMMMMMMMMMMM0:..,OWMMMMMMMMMMMW0o,.     
                    .;loodONMMMMWKd'. .,:cld0NNKkdol:.        
                         .;0WNXXKxc,'''.''':xX0c.             
                          .xXO:'..';looddoclkXO'              
                           ;k0l.          .:OOl.              
                            ;x0d.        .l00l.               
                             ,O0c.       ;O0c.                
                             .kKl.      .:0k'                 
                             .o0k:......;dKx.                 
                              .lkOkxxkxkOko,                  
                               .';cloooc:'.                   

               
               """)


For_my().main()
