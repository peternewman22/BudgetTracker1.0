# BudgetTracker1.0
This is my tenth iteration of a project to automatically categorise transactions from a bank statement, now with GUI. By identifying key words and phrase in the descriptions, the program learns to categorise common purchases.

I'm fully aware that other services exist that already do this, but by building one from scratch, I knew I would learn a bunch and could make it as flexible and granular as I want it to be.

At the outset, this project is an opportunity for me to:
* Learn to code a full, complex program from scratch
* Futher explore classes
* Learn to code a GUI
* Make a useful tool for my own budget tracking

## How it works
1. Structure your categorisation in excel or google sheets: 
    * Subcategory eg: Groceries, Car Services, Movies 
    * Category eg: Food, Car Costs, Movies
    * Bucket (if you're a barefoot investor) eg: Blow, Splurge, Smile
    * Class eg: Expenditure, Income
1. Copy this to the clipboard and run the program.
1. Initialise a keyword:subcategory map file using the data from the clipboard. (Work in progress).
1. Identify the bankstatement and turn on **safeMode** (manually categorise ALL transactions) or turn off **safeMode** (where there is a single match for a keyword, categorise using the keyword:subcategory map file)
1. Make an instance of an Application class that processes the bank statement and extract the list of descriptions as well as pulling out the year and month and adding those as additional columns in a pandas dataframe
1. Iterate through the list, looking for keyword matches in the descriptions
    * 0 matches: make a GUI and categorise as a once-off interaction or add a new keyword. Note: Keyword needs to be useful (contained in the description) and valid (unique) before a Submit is allowed.
    * 1 match: if **safeMode** --> automatically categorise; if not **safeMode** --> give quick match options (buttons) or prompt once off and new keyword entry
    * 2+ matches: Give quick match options etc
    * If new keyword or subcategory, save to the json file *(need database)*
1. Use the gui or keyword map to identify the subcategory
1. Append to an output csv using the subcategory map you set up at the beginning

The validation is a bit buggy still, but otherwise, it work ok.
Much work to go.

### Why no database?
Embarasingly, I'm yet to learn how to use databases. My task for myself in this project so far is to learn to code a GUI. For now, reading and writing to json files will do.
