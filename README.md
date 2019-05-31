# For_my

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ee4174e8bde54a54b0131f732f0c955e)](https://www.codacy.com/app/rob93c/For_my?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rob93c/For_my&amp;utm_campaign=Badge_Grade)![GitHub top language](https://img.shields.io/github/languages/top/rob93c/RomRoamer.svg) [![PEP8](https://img.shields.io/badge/code%20style-PEP8-important.svg)](https://www.python.org/dev/peps/pep-0008/) [![Build Status](https://travis-ci.com/rob93c/For_my.svg?branch=master)](https://travis-ci.com/rob93c/For_my) ![GitHub release](https://img.shields.io/github/release/rob93c/For_my.svg?color=blueviolet) [![Telegram](https://img.shields.io/badge/write%20me-Telegram-%231974f2.svg)](t.me/rob93c) [![GitHub](https://img.shields.io/github/license/rob93c/For_my.svg?color=%237d8183)](https://opensource.org/licenses/MIT)

A program I developed on my own for [**Azienda Agricola Trentina**](https://www.facebook.com/azagrtrentina) to manage the production of cheese, fully written with *Python 3* and _**PEP8 compliant**_.

It stores data in a `.csv` file and can manage it, generating a chart (using plotly).

![Sample graphic preview](sample/sample.png)

## Installation

- Make sure you have installed [`python`](https://www.python.org/downloads/) and [`pip`](https://pip.pypa.io/en/stable/installing/).
- Install the dependencies using `pip install -r requirements.txt`
- Launch the script in the terminal using `python For_my.py`

### Overview

The program will ask the user to choose what to do:
- 1 ---> Set how much money you spent, how much milk you used and weekly earnings 
- 2 ---> Get the total money spent
- 3 ---> Get the total liters of milk used
- 4 ---> Get the total net income
- 5 ---> Generate the chart showing both incomes and the liters of milk used
- 6 ---> Backup `data.csv` in Dropbox
- 0 ---> Close the program

#### License

See the [**LICENSE**](https://github.com/rob93c/RomRoamer/blob/master/LICENSE.md) file for license rights and limitations (MIT).