import json
import pandas as pd
import os
import csv
from datetime import datetime
import PySimpleGUI as sg

class Helper:
    """Contains useful general functions for read/write to json files and anything else 
    that would clutter up the main application. Static Methods only."""
    def __init__(self):
        pass
    
    @staticmethod
    def timestamp():
        return datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")

    @staticmethod
    def loadJson(jsonFile):
        """Loads json files"""
        with open(jsonFile, "r") as fh:
            return json.load(fh)

    @staticmethod
    def saveJson(dict2save, jsonFile):
        with open(jsonFile, "w") as fh:
            json.dump(dict2save, fh, indent = 2, sort_keys=True)


    @staticmethod
    def generateBaseMap():
        # Takes the clipboard and generates the list
        try:
            if os.path.isfile('BaseMap.csv'):
                df = pd.read_csv('BaseMap.csv',header=0)
            else:
                df = pd.read_clipboard(parse_dates=True)
            subcats = df['Subcategory'].to_list()
            categories = df['Category'].to_list()
            classes = df['Class'].to_list()
            buckets = df['Bucket'].to_list()
            baseDict = {}
            for eachSubcategory, eachCategory, eachClass, eachBucket in zip(subcats,categories,classes,buckets):
                baseDict[eachSubcategory] = {"Category" : eachCategory, "Bucket" : eachBucket, "Class" : eachClass}
            for k, v in baseDict.items():
                print(f"{k}: {v}")

            with open("subcatMap.json", "w") as fh:
                json.dump(baseDict,fh,sort_keys= True, indent = 2)
        except Exception as e:
            print(e)

    @staticmethod
    def extractFileExtension(fileName):
        file_extension = os.path.splitext(fileName)[1]
        return file_extension

    @staticmethod
    def write2csv(row):
        with open("output.csv", "a", newline='') as fh:
            writer = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)

    @staticmethod
    def getYear(row):
        return row["Date"].year

    @staticmethod
    def getMonth(row):
        return row["Date"].month

    @staticmethod
    def allCapsify(row):
        term2convert = str(row["Description"])
        try:
            return term2convert.upper()
        except Exception as e:
            print(f"Probem capitalizing: {e}")
            return row["Description"] 
    
    @staticmethod
    def getSettings():
        # default settings
        settings = {
            "safeMode" : True,
            "theme" : 'Dark Blue',
            "fileName": sg.popup_get_file('Bank statement to categorise')
        }

        sg.change_look_and_feel("Dark Blue")

        settingsLayout = [
        [sg.CB("SafeMode", default = True, tooltip = "Recommended for first run", key="-SAFE MODE-")],
        [sg.Text("Note: When in safemode is OFF, the program will rely on previous categorisations only.")],
        [sg.Text("Choose a theme (optional)"), sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-THEME-')],
        [sg.Submit(), sg.Cancel()]
        ]

        # extracting from the window
        window = sg.Window("Choose Settings", settingsLayout)
        event, values = window.read()
        window.close()

        # Overwriting if necessary
        if event != None:
            try:
                settings['safeMode'] = values["-SAFE MODE-"]
                if len(values["-THEME-"])>0:
                    settings['theme'] = values["-THEME-"][0]
            except Exception as e:
                print(e)

        return settings