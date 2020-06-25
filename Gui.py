"""
Note: Version 2 is much more action-based and extensively uses enable_events to direct updates
"""

import PySimpleGUI as sg
from SearchBox import SearchBox

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
        self.searchOnceOff = SearchBox("OnceOff Subcategory","-ONCEOFF LISTBOX-",self.subcategoryList,5,True,'-ONCEOFF SEARCH TERM-')
        self.searchSubcategory = SearchBox("Subcategory","-SUBCAT LISTBOX-",self.subcategoryList,"-SUBCAT SEARCH TERM-", )
        self.searchCategory = SearchBox("Category","-CAT LISTBOX-",self.categoryList,5,True,"-CAT SEARCH TERM-")
        self.searchBucket = SearchBox("Bucket","-BUCKET-",self.bucketList,3,False)
        self.searchClass = SearchBox("Class","-CLASS-",["Expenditure", "Income"],2,False)
        self.showNewKWFrame = False # Use these to deterimine whether an update is due or if it's already been triggered
        self.showNewSubcatFrame = False
        self.showOnceOffFrame = False
        self.window = None
        self.validSubmit = False
        self.data = self.createDataTemplate()
        self.flagMap = {'-NEW KW FRAME-' : self.showNewKWFrame, '-NEW SUBCAT FRAME-' : self.showNewSubcatFrame, '-ONCEOFF FRAME-' : self.showOnceOffFrame}
        self.flag2FrameMap = {'-NEW KW FLAG-':'-NEW KW FRAME-', '-NEW SUBCAT FLAG-':'-NEW SUBCAT FRAME-', '-ONCEOFF FLAG-':'-ONCEOFF FRAME-'}
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


    # Once-off categorisation frame    
    def generateOnceOffFrame(self):
        """Generates the Once-Off Categorisation Frame"""
        layout = []
        self.searchOnceOff.addToFrame(layout)
        return [sg.Frame("Once-Off Categorisation", layout = layout, visible=False, key='-ONCEOFF FRAME-')]

    # New Subcategory Frame
    def generateNewSubcatFrame(self):
        """Generates the New Subcategory Frame"""
        layout = [[sg.T("New Subcat: "), sg.InputText(key='-NEW SUBCAT-')]]
        layout = self.searchCategory.addToFrame(layout)
        layout = self.searchBucket.addToFrame(layout) 
        layout = self.searchClass.addToFrame(layout)
        return [sg.Frame("New Subcategory", layout = layout, visible=True , key='-NEW SUBCAT FRAME-')]

    # New Keyword frame
    def generateNewKWFrame(self):
        """Generates the New Keyword Frame"""
        layout = [[sg.T("New Keyword: "), sg.InputText(key='-NEW KW-')]]
        layout = self.searchSubcategory.addToFrame(layout)
        return [sg.Frame("New Keyword", layout = layout, visible=False , key='-NEW KW FRAME-')]

    # Checkboxes / Flags
    def generateFlags(self):
        """Generates checkboxes"""
        # makes checkboxes: debug, newKW, newSubcat --> used to reveal parts of the window
        debug = sg.CB("Debug Mode", default = True, key = '-DEBUG-', enable_events=True)
        onceoff = sg.CB("Once-Off", default = False, key = '-ONCEOFF FLAG-',enable_events=True)
        newKW = sg.CB("New Keyword", default = False, key = '-NEW KW FLAG-',enable_events=True)
        newSubcat = sg.CB("New Subcat", default = False, key = '-NEW SUBCAT FLAG-',enable_events=True)
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
            [sg.Button("Uncategorised"),sg.Submit(disabled=False, key='-SUBMIT-', tooltip = self.submitTooltip), sg.Cancel()]
        ]
    def validateNewKeyword(self, newKW):
        """Checks to see if a new keyword has already been used"""
        newKW = newKW.upper() # all keywords are upper
        return newKW not in self.kwList

    def toggleFrameVisibility(self, frameKey):
        """Toggles visibility for frames within the window"""
        print(f'Changing {frameKey}. Was {self.flagMap[frameKey]} now {not self.flagMap[frameKey]}')
        self.flagMap[frameKey] = not self.flagMap[frameKey] # toggle flag
        self.window[frameKey].update(visible=self.flagMap[frameKey]) # set visibility to new value of flag
        
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
    
    def createDataTemplate(self):
        """Creates the template for data to be gathered"""
        return {
            "Subcategory" : "Uncategorised", # default
            "New Keyword": None,
            "New Subcategory" : False,
            "Category" : None,
            "Bucket" : None,
            "Class" : "Expenses" # default
            }
    
    def filterList(self, searchTerm, searchList):
        """Prepares the search term and filters the list"""
        search = searchTerm.strip().title() # All subcategories are capitalized only
        if search == '':
            return searchList
        else:
            return list(filter(lambda eachItem: search == eachItem[:len(search)],searchList))

    def getSubcategoryLoop(self):
        """Uses the window to find the subcategory and new keyword/subcategory data"""
                
        self.window = self.generateWindow()
        while True:
            event, values = self.window.Read(timeout = 1000)

            # Cancel?
            if event in (None, "Cancel", "Uncategorised"):
                print("Categorised as 'Uncategorised'")
                break
            
            # showing debug information
            if event != '__TIMEOUT__' and values['-DEBUG-']:
                print(f"event: {event} \nvalues: {values}\n\n")

            # detecting quick match selections
            elif event in self.matches:
                self.data['Subcategory'] = self.kwMap[event] # look up the keyword mapping and overwrite Subcategory
                print(f"Categorised using {event} --> {self.data['Subcategory']}")
                break

            # If submit...
            elif event == "-SUBMIT-": #Only available in the case of a new keyword
                if values['-ONCEOFF FLAG-']:
                    self.data['Subcategory'] = values['-ONCEOFF SUBCATEGORY-'][0].title() #extract and format as title
                elif values['-NEW KW-']: # To be explicit, but submit can't be access without keyword
                    self.data['New Keyword'] = values['-NEW KW-'].upper() # extract the keyword
                    if values['-NEW SUBCAT-']: # changed to rely on the CB's 
                        self.data['Subcategory'] = values['-NEW SUBCAT-'].title()
                        self.data['Category'] = values['-CAT LISTBOX-'][0]
                        self.data['Bucket'] = values['-BUCKET-'][0]
                        self.data['Class'] = values['-CLASS-'][0]
                    else:
                        self.data['Subcategory'] = values['-SUBCAT LISTBOX-'][0].title() # extract subcategory        
        
                print("Finished with the following data:")
                [print(f"{k}: {v}") for k, v in self.data.items()]
                break       

           # updating the search lists
            elif event == '-SUBCAT SEARCH TERM-': # if there's a change in the search term
                self.updateList(values['-SUBCAT SEARCH TERM-'], self.subcategoryList, '-SUBCAT LISTBOX-') # update subcategories on display
            
            elif event == '-CAT SEARCH TERM-': # if there's a change in the search term
                self.updateList(values['-CAT SEARCH TERM-'],self.categoryList,'-CAT LISTBOX-') # update categories on display
            
            elif event == '-ONCEOFF SEARCH TERM-':
                self.updateList(values['-ONCEOFF SEARCH TERM-'], self.subcategoryList, '-ONCEOFF SUBCATEGORY-')
                  

            # if there's a change to any of the flag checkboxes, update visibility
            elif event in ("-NEW KW FLAG-", "-NEW SUBCAT FLAG-", "-ONCEOFF FLAG-"):
                toChange = self.flag2FrameMap[event]
                self.toggleFrameVisibility(toChange) # show or hide frames
            
            """disable/enable submit based on once-off checkbox"""
            # if values['-ONCEOFF FLAG-']:
                # self.window['-NEW KW FLAG-'].update(disabled = True) # if once off, disable NEW KEYWORD
                # if self.isSelected(values['-ONCEOFF SUBCATEGORY-']):
                    # self.window['-SUBMIT-'].update(disabled = False)
            # elif not values['-ONCEOFF FLAG-']:
            #     self.window['-NEW KW FLAG-'].update(disabled = False)

            """disable/enable submit based on new kw flag"""
            # if values['-NEW KW FLAG-']:
            #     # self.window['-NEW SUBCAT FLAG-'].update(disabled=False) # if new kw flag, then allow new subcat flag
            #     validKWInfo = all([self.validate("kw", values['-NEW KW-'], self.kwList), self.usefulKeyword(values['-NEW KW-'])]) # If the kw is useful and valid           
            #     if not values['-NEW SUBCAT FLAG-']: # if we're NOT using a new subcategory
            #         self.data["New Subcategory"] = False # set new subcat explicitly to false
            #         # if validKWInfo and self.isSelected(values['-SUBCAT LISTBOX-']): # allow submit if valid, useful keyword and a subcategory selection made
            #         #     self.window['-SUBMIT-'].update(disabled = False)
            #         # else:
            #         #     self.window['-SUBMIT-'].update(disabled = True)
            #     if values['-NEW SUBCAT FLAG-']:
            #         self.data["New Subcategory"] = True
            #         # validSubcatInfo = self.validate("subcat", '-NEW SUBCAT-', self.subcategoryList)
            #         # if validKWInfo and validSubcatInfo and self.isSelected(values['-CAT LISTBOX-']) and self.isSelected(values['-BUCKET-']) and self.isSelected(values['-CLASS-']):
            #         #     self.window['-SUBMIT-'].update(disabled = False)
            #         # else:
            #         #     self.window['-SUBMIT-'].update(disabled = True)

            
            

        self.window.close()
        self.window = None
        return self.data