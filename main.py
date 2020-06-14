from Application import Application
from Helper import Helper
from Gui import Gui
import PySimpleGUI as sg
import os
from datetime import datetime

"""
TODO: X Fix Gui - hiding the once-off box logic fix
TODO: X Fix Gui - once-off disabled CB needs to be dynamic 
TODO: X Fix Gui - base collection of data on the flags at submit
TODO: X Refactor: change to be event based 
TODO: _ New feature: Right Click to edit or delete keyword
TODO: _ New feature: Adding a resume button
TODO: _ New feature: Add/remove categories
TODO: _ Refactor: collect the searching implementation into a method or class
TODO: ? Fix Application/GUI to use the Quick Match options - testing required
"""

def main():
    sg.change_look_and_feel('Dark Blue')
    # get the settings
    settings = Helper.getSettings()
    # set the theme 
    sg.change_look_and_feel(settings['theme'])
    
    # if it doesn't exist, create the kwMap file
    if not os.path.isfile("kwMap.json"):
        with open("kwMap.json", "w"):
            pass
    
    # generate base map        
    if not os.path.isfile("subcatMap.json"):
        Helper.generateBaseMap()
    
    # make an instance of the app class
    # app = Application(settings['fileName'], settings['safeMode'])
    app = Application(settings['fileName'],settings['safeMode'])
    Helper.write2csv([Helper.timestamp()]) # writing timestamp
    Helper.write2csv(["Date","Backdate","Description","Transaction","Balance","Year","Month","Searchable Description","Subcategory","Category","Bucket","Class"]) #writing titles
    app.loop()
    
    print(f"Finished at {Helper.timestamp()}") # Bookend
   
    

if __name__== "__main__":
    main()