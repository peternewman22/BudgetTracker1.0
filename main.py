from Application import Application
from Helper import Helper
import PySimpleGUI as sg
import os
import json
from datetime import datetime


def main():
    sg.change_look_and_feel('Dark Blue')
    # get the settings
    settings = Helper.getSettings()
    # set the theme 
    sg.change_look_and_feel(settings['theme'])
    
    # if it doesn't exist, create the kwMap file
    if not os.path.isfile("kwMap.json"):
        print("Creating kwMap.json")
        with open("kwMap.json", "w") as fh:
            json.dump({},fh)
    
    # generate base map        
    if not os.path.isfile("subcatMap.json"):
        print("Creating subcatMap.json")
        Helper.generateBaseMap()
    
    # make an instance of the app class
    app = Application(settings['fileName'],settings['safeMode'])
    Helper.write2csv([Helper.timestamp()]) # writing timestamp
    Helper.write2csv(["Date","Backdate","Description","Transaction","Balance","Year","Month","Searchable Description","Subcategory","Category","Bucket","Class"]) #writing titles
    app.loop()
    
    print(f"Finished at {Helper.timestamp()}") # Bookend
   
if __name__== "__main__":
    main()