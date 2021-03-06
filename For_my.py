#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = '0.5'
__author__ = 'Roberto Cella'

r"""


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

                     _____                            
                    |  ___|__  _ __   _ __ ___  _   _ 
                    | |_ / _ \| '__| | '_ ` _ \| | | |
                    |  _| (_) | |    | | | | | | |_| |
                    |_|  \___/|_|    |_| |_| |_|\__, |
                                                |___/ 


         DEVELOPED BY ROBERTO CELLA FOR AZIENDA AGRICOLA TRENTINA

"""

import os
import sys
import csv
import plotly
import dropbox
import datetime
import pandas as pd
from time import sleep
from pathlib import Path
from os import system, name
import plotly.graph_objs as go
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError

dirname = os.path.dirname(os.path.abspath(__file__))
path = Path(os.path.join(dirname, "data.csv"))


class For_my:

    @classmethod
    def main(cls) -> None:
        sys.tracebacklimit = 0
        Tools.logo()
        sleep(2)
        Tools.clear()
        Tools.menu()
        if not path.exists():  # creates `data.csv` if it doesn't exist
            f = open(path, "w")
            f.write("Date,Spese,Latte usato,Guadagno\n")
            f.close()
            For_my.loop()
        else:
            For_my.loop()

    @staticmethod
    def loop() -> None:
        while True:
            Tools.remove_blanks()
            choice: str = input()
            if choice == "1":  # set money spent, used milk and earnings
                Tools.load_values()
            elif choice == "2":  # get the total money spent
                print(f"\nLe spese totali sono state di {Tools.summer(1)}€.\n")
            elif choice == "3":  # get the total liters of milk used
                print(f"\nHai usato un totale di {Tools.summer(2)} litri.\n")
            elif choice == "4":  # get the total net income
                gain: float = Tools.summer(3) - Tools.summer(1) - \
                        Tools.summer(2) * 0.4
                print(f"\nHai guadagnato un netto di {Tools.prettify(gain)}€.\n")
            elif choice == "5":  # generate the chart
                Tools.create_graph()
            elif choice == "6":  # backup `data.csv` in Dropbox
                Tools.backup()
            elif choice == "0":  # closure
                sys.exit()
            else:
                print("\nInserisci il numero corrispondente all'azione desiderata.\n")
#               again = input(  # repeat cycle
#                    "\nDesideri continuare a usare l'applicazione?\n(Premi \"s\" per continuare)\n")
#                if again == "s" or again == "S":
#                    continue
#                else:
#                    break


class Tools:

    # Creates the chart from `data.csv`
    @staticmethod
    def create_graph() -> None:
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
        }, auto_open=True, filename="grafico.html")

    # Takes an index and sums every number at that index in a csv file
    @staticmethod
    def summer(index: int) -> int:
        tot: int = 0
        with open(path, "r", newline="") as op:
            reader = csv.reader(op, delimiter=",")
            data = [line[index] for line in reader if line[index].isdigit()]
            for value in data:
                tot += int(value)
            return tot

    # Allows the user to insert new data
    @staticmethod
    def load_values() -> None:
        with path.open("a") as op:
            writer = csv.writer(op)
            writer.writerow([f"{datetime.datetime.now():%d-%m-%Y}", input(
                "\nQuanto hai speso questa settimana? "), input(
                "Quanti litri di latte hai lavorato? "), input(
                "Quanto hai guadagnato questa settimana? ")
            ])

    # Takes a float number and returns a string with just 2 decimals
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

    # Removes every blank line in excess from the .csv file
    @staticmethod
    def remove_blanks() -> None:
        with open(path, "r") as op:
            lines: list = op.readlines()  # read lines in memory
        with open(path, "w") as op:       # rewrite everything from the beginning
            for line in lines:
                if line != "\n":
                    op.write(line)
                else:
                    continue

    # Backups `data.csv` to Dropbox, in Dropbox/Applications/Formy/
    @staticmethod
    def backup() -> None:
        TOKEN = "" # Paste your Dropbox token
        LOCALFILE = os.path.join(dirname, "data.csv")
        BACKUPPATH = "/data.csv"
        dbx = dropbox.Dropbox(TOKEN)
        with open(LOCALFILE, "rb") as f:
            # We use WriteMode=overwrite to make sure that the settings in the file
            # are changed on upload
            print(f"""\nCaricamento di {LOCALFILE} in Dropbox...
Troverai il file in Dropbox/Applicazioni/Formy.""")
            try:
                dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode("overwrite"))
                print("Caricamento completato con successo!\n")
            except ApiError as err:
                # This checks for the specific error where a user doesn't 
                # have enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERRORE: Spazio insufficiente.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()

    # Clears terminal's screen
    @staticmethod
    def clear() -> None:
        if Tools.is_win():
            _ = system("cls")
        else:
            _ = system("clear")

    # Check if the OS is Windows
    @staticmethod
    def is_win() -> bool:
        return name == "nt"

    # Prints program's menu
    @staticmethod
    def menu() -> None:
        print("""
Benvenuto in For_my, scegli un'opzione:

1) Registra le uscite settimanali, litri lavorati e introiti
2) Vedi la cronologia delle spese
3) Vedi la cronologia del latte lavorato
4) Vedi le entrate nette
5) Crea il grafico (latte e soldi guadagnati in relazione al tempo)
6) Esegui il backup di data.csv in Dropbox
0) Chiudi il programma
            """)

    # Prints the logo
    @staticmethod
    def logo() -> None:
        print(r"""


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

                     _____                            
                    |  ___|__  _ __   _ __ ___  _   _ 
                    | |_ / _ \| '__| | '_ ` _ \| | | |
                    |  _| (_) | |    | | | | | | |_| |
                    |_|  \___/|_|    |_| |_| |_|\__, |
                                                |___/ 
               
               """)

if __name__ == "__main__":
    For_my().main()
