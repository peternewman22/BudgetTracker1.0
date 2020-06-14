"""
Note: Version 2 is much more action-based and extensively uses enable_events to direct updates
"""

import PySimpleGUI as sg

class Gui:
    """Handles creating each window, gathering the subcategory"""
    def __init__(self, desc, kwMap, matches, subcatMap, subcategoryList, categoryList, bucketList, keywordList):
        self.desc = desc
        self.matches = matches
        self.subcatMap = subcatMap
        self.subcategoryList = subcategoryList
        self.categoryList = categoryList
        self.bucketList = bucketList
        self.kwMap = kwMap
        self.kwList = keywordList
        self.yetToShowNewKWFrame = True # Use these to deterimine whether an update is due or if it's already been triggered
        self.yetToShowNewSubcatFrame = True
        self.yetToShowOnceOff = True
        self.window = None
        self.flagMap = {'-NEW KW FRAME-' : self.yetToShowNewKWFrame, '-NEW SUBCAT FRAME-' : self.yetToShowNewSubcatFrame, '-ONCEOFF FRAME-' : self.yetToShowOnceOff}
        self.submitTooltip = "Only unique keywords and subcategories can be submitted..."


    def generateKWButtonFrame(self):
        """Creates the KW Buttons frame"""
        # if there are no matches, return a message in the frame instead of buttons
        if len(self.matches) == 0:
            noMatchLayout = [[sg.Text("No Quick Matches Found")]]
            return [sg.Frame("Quick Match", layout = noMatchLayout)]
        else:
            frameLayout = []
            for eachMatch in self.matches:
                frameLayout.append([sg.Button(eachMatch),sg.T(f"maps to {self.kwMap[eachMatch]}")])
            return [sg.Frame("Quick Match",layout=frameLayout)]

    def validateNewKeyword(self, newKW):
        """Checks to see if a new keyword has already been used"""
        newKW = newKW.upper() # all keywords are upper
        return newKW not in self.kwList

    def filteredList(self, searchTerm, searchList):
        """Filters the subcategories by the search term"""
        search = searchTerm.upper().strip()
        if search == '':
            return self.subcategoryList
        else:
            return list(filter(lambda eachSubcat: searchTerm == eachSubcat[:len(search)], searchList))

    # Once-off categorisation frame    
    def generateOnceOffFrame(self):
        """Generates the Once-Off Categorisation Frame"""
        layout = [
            [sg.T("Search:"),sg.InputText(key="-ONCEOFF SEARCH TERM-", enable_events= True)],
            [sg.Listbox(self.subcategoryList, key='-ONCEOFF SUBCATEGORY-', size = (20, 10), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]
        ]
        return [sg.Frame("Once-Off Categorisation", layout = layout, visible=False, key='-ONCEOFF FRAME-')]

    # New Subcategory Frame
    def generateNewSubcatFrame(self):
        """Generates the New Subcategory Frame"""
        newSubcatLayout = [
            [sg.T("New Subcat: "), sg.InputText(key='-NEW SUBCAT-')],
            [sg.T("Choose a category: "), sg.InputText(key='-CAT SEARCH TERM-', enable_events = True)],
            [sg.Listbox(self.categoryList, key = '-CAT LISTBOX-', size=(20,10), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)],
            [sg.T("Choose a bucket")],
            [sg.Listbox(self.bucketList, key='-BUCKET-', size = (20,len(self.bucketList)), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events =True)],
            [sg.T("Choose a class")],
            [sg.Listbox(["Expenditure","Income"], key='-CLASS-',size = (20,2),select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]
        ]
        return [sg.Frame("New Subcategory", layout = newSubcatLayout, visible=False , key='-NEW SUBCAT FRAME-')]

    # New Keyword frame
    def generateNewKWFrame(self):
        """Generates the New Keyword Frame"""
        newKWLayout = [
            [sg.T("New Keyword: "), sg.InputText(key='-NEW KW-')],
            [sg.T("Choose a subcategory: "), sg.InputText(key='-SUBCAT SEARCH TERM-', enable_events= True)],
            [sg.Listbox(self.subcategoryList, key = '-SUBCAT LISTBOX-', size=(20,10), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events = True)]
        ]
        return [sg.Frame("New Keyword", layout = newKWLayout, visible=False , key='-NEW KW FRAME-')]

    # Checkboxes / Flags
    def generateFlags(self):
        """Generates checkboxes"""
        # makes checkboxes: debug, newKW, newSubcat --> used to reveal parts of the window
        debug = sg.CB("Debug Mode", default = True, key = '-DEBUG-', enable_events=True)
        onceoff = sg.CB("Once-Off", default = False, key = '-ONCEOFF FLAG-',enable_events=True)
        newKW = sg.CB("New Keyword", default = False, key = '-NEW KW FLAG-',enable_events=True)
        newSubcat = sg.CB("New Subcat", default = False, key = '-NEW SUBCAT FLAG-', disabled = True)
        return [debug, onceoff, newKW, newSubcat]

    # final layout
    def generateCompleteLayout(self):
        """The final layout"""
        return [
            [sg.Text(f"Description: {self.desc}")],
            self.generateFlags(),
            self.generateKWButtonFrame(),
            self.generateOnceOffFrame(),
            self.generateNewKWFrame(),
            self.generateNewSubcatFrame(),
            [sg.Button("Uncategorised"),sg.Submit(disabled=True, key='-SUBMIT-', tooltip = self.submitTooltip), sg.Cancel()]
        ]
    
    def checkFrameVisibility(self, flagValue, frameKey):
        """Toggles visibility for frames within the window"""
        if flagValue and self.flagMap[frameKey]:
            self.window[frameKey].update(visible=True)
            self.flagMap[frameKey] = False

        elif not flagValue and not self.flagMap[frameKey]:
            self.window[frameKey].update(visible=False)
            self.flagMap[frameKey] = True

    def filterList(self, searchTerm, searchList):
        """Prepares the search term and filters the list"""
        search = searchTerm.strip().title() # All subcategories are capitalized only
        if search == '':
            return searchList
        else:
            return list(filter(lambda eachItem: search == eachItem[:len(search)],searchList))
    
    def updateList(self, searchTerm, searchList, listboxKey):
        """Updates listbox based on a filtered list"""
        filteredList = self.filterList(searchTerm, searchList)
        self.window[listboxKey].update(values=filteredList)

    def validate(self,checkType,userInput,referenceList):
        """Adjusts the text accordingly and checks for existence within a reference list"""
        if checkType == "kw":
            term = userInput.strip().upper()
        elif checkType == "subcat":
            term = userInput.strip().title()
        return term not in referenceList and term != ''

    def usefulKeyword(self, kw):
        """Tests to see if the proposed keyword is actually in the description i.e. can it be used to identify the tag"""
        testKW = kw.upper() # all keywords are in upper case
        return testKW in self.desc

    def isSelected(self, listToCheck):
        """Checks if a single selection is made"""
        return len(listToCheck) == 1

    def generateWindow(self):
        """Creates a new window"""
        return sg.Window("Categorise Me!", self.generateCompleteLayout())

    def getSubcategoryLoop(self):
        """Uses the window to find the subcategory and new keyword/subcategory data"""
        data = {
            "Subcategory" : "Uncategorised", # default
            "New Keyword": None,
            "New Subcategory" : False,
            "Category" : None,
            "Bucket" : None,
            "Class" : "Expenses" # default
            }
        
        self.window = self.generateWindow()
        while True:
            event, values = self.window.Read(timeout = 1000)
            # Have we closed the window?
            if event in (None, "Cancel", "Uncategorised"):
                subcategory = "Uncategorised"
                print("Categorised as 'Uncategorised'")
                break

            # If submit...
            if event == "-SUBMIT-": #Only available in the case of a new keyword
                if values['-ONCEOFF FLAG-']:
                    subcategory = values['-ONCEOFF SUBCATEGORY-'][0].title() #format as title
                elif values['-NEW KW-']: # To be explicit, but submit can't be access without keyword
                    data['New Keyword'] = values['-NEW KW-'].upper() # extract the keyword
                    if values['-NEW SUBCAT-']: # changed to rely on the CB's 
                        data['Subcategory'] = values['-NEW SUBCAT-'].title()
                        data['Category'] = values['-CAT LISTBOX-'][0]
                        data['Bucket'] = values['-BUCKET-'][0]
                        data['Class'] = values['-CLASS-'][0]
                    else:
                        data['Subcategory'] = values['-SUBCAT LISTBOX-'][0].title() # subcategory        
                
                print("Finished with the following data:")
                [print(f"{k}: {v}") for k, v in data.items()]
                break
            
            # detecting quick match selections
            if event in self.matches:
                data['Subcateogry'] = self.subcatMap[event] # look up the keyword mapping and overwrite Subcategory
                print(f"Categorised as {subcategory} --> {self.kwMap[subcategory]}")
                break

           # updating the search lists
            if event == '-SUBCAT SEARCH TERM-': # if there's a change in the search term
                self.updateList(values['-SUBCAT SEARCH TERM-'], self.subcategoryList, '-SUBCAT LISTBOX-') # update subcategories on display
            if event == '-CAT SEARCH TERM-': # if there's a change in the search term
                self.updateList(values['-CAT SEARCH TERM-'],self.categoryList,'-CAT LISTBOX-') # update categories on display
            if event == '-ONCEOFF SEARCH TERM-':
                self.updateList(values['-ONCEOFF SEARCH TERM-'], self.subcategoryList, '-ONCEOFF SUBCATEGORY-')
            
            # showing debug information
            if event != '__TIMEOUT__' and values['-DEBUG-']:
                print(f"event: {event}, values: {values}")

            # if there's a change to any of the flag checkboxes, update visibility
            if event in ("-NEW KW FLAG-", "-NEW SUBCAT FLAG-", "-ONCEOFF FLAG-"):
                self.checkFrameVisibility(values['-NEW KW FLAG-'], '-NEW KW FRAME-') # show or hide KW Frame
                self.checkFrameVisibility(values['-NEW SUBCAT FLAG-'], '-NEW SUBCAT FRAME-') # show or hide the Subcat Frame
                self.checkFrameVisibility(values['-ONCEOFF FLAG-'], '-ONCEOFF FRAME-' ) # show or hide the Once-Off Frame
            
            # disable/enable submit based on once-off checkbox
            if values['-ONCEOFF FLAG-']:
                self.window['-NEW KW FLAG-'].update(disabled = True) # if once off, disable NEW KEYWORD
                if self.isSelected(values['-ONCEOFF SUBCATEGORY-']):
                    self.window['-SUBMIT-'].update(disabled = False)
            elif not values['-ONCEOFF FLAG-']:
                self.window['-NEW KW FLAG-'].update(disabled = False)

            # disable/enable submit based on new kw flag
            if values['-NEW KW FLAG-']:
                self.window['-NEW SUBCAT FLAG-'].update(disabled=False) # if new kw flag, then allow new subcat flag
                validKWInfo = all([self.validate("kw", values['-NEW KW-'], self.kwList), self.usefulKeyword(values['-NEW KW-'])]) # If the kw is useful and valid           
                if not values['-NEW SUBCAT FLAG-']: # if we're NOT using a new subcategory
                    data["New Subcategory"] = False # declare
                    if validKWInfo and self.isSelected(values['-SUBCAT LISTBOX-']): # allow submit if valid, useful keyword and a subcategory selection made
                        self.window['-SUBMIT-'].update(disabled = False)
                    else:
                        self.window['-SUBMIT-'].update(disabled = True)
                if values['-NEW SUBCAT FLAG-']:
                    data["New Subcategory"] = True
                    validSubcatInfo = self.validate("subcat", '-NEW SUBCAT-', self.subcategoryList)
                    if validKWInfo and validSubcatInfo and self.isSelected(values['-CAT LISTBOX-']) and self.isSelected(values['-BUCKET-']) and self.isSelected(values['-CLASS-']):
                        self.window['-SUBMIT-'].update(disabled = False)
                    else:
                        self.window['-SUBMIT-'].update(disabled = True)

            
            

        self.window.close()
        self.window = None
        
        return data