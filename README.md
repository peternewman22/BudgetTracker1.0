# BudgetTracker1.0

This is my tenth iteration of a project to automatically categorise transactions from a bank statement, now with GUI. By identifying key words and phrase in the descriptions, the program learns to categorise common purchases.

I'm fully aware that other services exist that already do this. I wanted to make one from the ground up. By building one from scratch, I knew I would learn a bunch and could make it as flexible and granular as I want it to be (my main frustration with services like Pocket).

At the outset, this project is an opportunity for me to:

* Learn to code a full, complex program from scratch
* Futher explore classes
* Learn to code a GUI
* Make a useful tool for my own budget tracking

## How it works

Some flowchart terminology:

* Quick Match: Uses previous keyword:subcategory mapping
* New KW: Saving a NEW KW mapping
* Once-off: Manually pick a subcategory but don't save a new keyword:subcategory pair

![Flow Diagram](FlowDiagram.png?raw=True)

## Screenshots

* Base structure example

![Example Base map](ExampleBaseMap.png?raw=True)

* All categorisation options: Quick Match, Once Off, Establishing a new Keyword pairing with the option of adding a new subcategory. (NB: Please choose different theme to this one. Luckily, you have the options at the beginning of the program.)

![All fields](Fields.png?raw=True)

## Why no database

Embarrassingly, I'm yet to learn how to use databases. My task for myself in this project so far is to learn to code a GUI. For now, reading and writing to json files will do

## To do / Progress / Targets

* ~~General restucture to improve readability and to modularize more~~
* ~~Fix Gui - hiding the once-off box logic fix~~
* ~~Fix Gui - once-off disabled CB needs to be dynamic~~
* ~~Fix Gui - base collection of data on the flags at submit~~
* ~~Refactor: change to be event based~~
* ~~Refactor: collect creating searchbox into a method or class~~
* ~~Fix visibility bug~~
* ~~Strip away buggy validation~~
* New feature: user to specify output filename and location
* Refactor: sort out muddle of functionality - searching and updating the searchbox is currently done in GUI. Ideally, it would be under SearchBox.
* New feature: Right Click to edit or delete keyword
* New feature: Adding a resume button
* New feature: Add/remove categories
* Fix Application/GUI to use the Quick Match options - testing require
* Restructure adding search boxes to frames. Very clunky right now.

## Current Bugs

* Detecting new subcategory error

## Stretch Goals / Next Moves for BudgetTracker1.0

* Integrate with database
* Set up to generate the base map programmatically
* Create a Gui to examine and change keyword:subcategories and subcategories:category,bucket,class
* Call up PayPal services - bank transcripts aren't very descriptive here
* Auto-complete on search terms
* Move to a webservice? Possibly integrate with Google Sheets
* Rewrite as a Google Sheets extension
