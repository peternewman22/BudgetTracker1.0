"""
Note: Version 2 is much more action-based and extensively uses enable_events to direct updates
"""

import PySimpleGUI as sg
from SearchBox import SearchBox
from Keys import Keys

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
        self.searchSubcategory = SearchBox("Subcategory",self.subcategoryList,Keys.selection_subcategory,5,True,Keys.searchterm_subcategory)
        self.searchOnceOff = SearchBox("Onceoff",self.subcategoryList,Keys.selection_onceoff,5,True,Keys.searchterm_onceoff)
        self.searchCategory = SearchBox("Category",self.categoryList,Keys.selection_category,5,True,Keys.searchterm_category)
        self.searchBucket = SearchBox("Bucket",self.bucketList,Keys.selection_bucket,3,False,None)
        self.searchClass = SearchBox("Class",["Expenditure", "Income"],Keys.selection_class,2,False,None)
        self.showNewKWFrame = False # Use these to deterimine whether an update is due or if it's already been triggered
        self.showNewSubcatFrame = False
        self.showOnceOffFrame = False
        self.window = None
        self.validSubmit = False
        self.data = self.createDataTemplate()
        self.flagMap = {Keys.frame_new_kw : self.showNewKWFrame, Keys.frame_new_subcat : self.showNewSubcatFrame, Keys.frame_onceoff : self.showOnceOffFrame}
        self.flag2FrameMap = {Keys.flag_new_kw : Keys.frame_new_kw, Keys.flag_new_subcat : Keys.frame_new_subcat, Keys.flag_onceoff : Keys.frame_onceoff}
        self.submitTooltip = "Only unique keywords and subcategories can be submitted..."


    def generateKWButtonFrame(self):
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
        layout = []
        self.searchOnceOff.addToFrame(layout)
        return [sg.Frame("Once-Off Categorisation", layout = layout, visible=self.showOnceOffFrame, key=Keys.frame_onceoff)]

    # New Subcategory Frame
    def generateNewSubcatFrame(self):
        layout = [[sg.T("New Subcat: "), sg.InputText(key=Keys.new_subcategory)]]
        layout = self.searchCategory.addToFrame(layout)
        layout = self.searchBucket.addToFrame(layout) 
        layout = self.searchClass.addToFrame(layout)
        return [sg.Frame("New Subcategory", layout = layout, visible=self.showNewSubcatFrame , key=Keys.frame_new_subcat)]

    # New Keyword frame
    def generateNewKWFrame(self):
        layout = [[sg.T("New Keyword: "), sg.InputText(key=Keys.new_keyword)]]
        layout = self.searchSubcategory.addToFrame(layout)
        return [sg.Frame("New Keyword", layout = layout, visible=self.showNewKWFrame , key=Keys.frame_new_kw)]

    # Checkboxes / Flags
    def generateFlags(self):
        # makes checkboxes: debug, newKW, newSubcat --> used to reveal parts of the window
        debug = sg.CB("Debug Mode", default = True, key = Keys.flag_debug, enable_events=True)
        onceoff = sg.CB("Once-Off", default = False, key = Keys.flag_onceoff,enable_events=True)
        newKW = sg.CB("New Keyword", default = False, key = Keys.flag_new_kw,enable_events=True)
        newSubcat = sg.CB("New Subcat", default = False, key = Keys.flag_new_subcat,enable_events=True)
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
            [sg.Button(Keys.button_uncategorised.value),sg.Submit(disabled=False, key=Keys.button_submit, tooltip = self.submitTooltip), sg.Cancel(),sg.Button(Keys.button_end_program)]
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
            Keys.data_subcategory : Keys.button_uncategorised.value,
            Keys.data_new_kw: None,
            Keys.data_is_new_subcategory : False,
            Keys.data_category : None,
            Keys.data_bucket : "None",
            Keys.data_class : "Expenses", # default - most classes are
            Keys.data_end_flag : False # Triggers the end of the program
            }
    
    def filterList(self, searchTerm, searchList):
        """Prepares the search term and filters the list"""
        search = searchTerm.strip().title() # All subcategories are capitalized only
        if search == '':
            return searchList
        else:
            return list(filter(lambda eachItem: search == eachItem[:len(search)],searchList))

    def getSubcategoryLoop(self):
        """Uses the gui window to find the subcategory and new keyword/subcategory data"""
                
        self.window = self.generateWindow()
        while True:
            event, values = self.window.Read(timeout = 1000)

            # Cancel
            if event in (None, Keys.button_cancel.value, Keys.button_uncategorised): # has to be value for cancel to match sg.Cancel()
                print("Categorised as 'Uncategorised'")
                break

            elif event == "End Program":
                self.data[Keys.data_end_flag.value] = True
                print('Ending program without categorising the last value')
                break

            
            # showing debug information
            elif event != '__TIMEOUT__' and values[Keys.flag_debug.value]:
                print(f"event: {event} \nvalues: {values}\n")

            # detecting quick match selections
            if event in self.matches:
                self.data[Keys.data_subcategory.value] = self.kwMap[event] # look up the keyword mapping and overwrite Subcategory
                print(f"Categorised using {event} --> {self.data[Keys.data_subcategory.value]}")
                break

            # If submit...
            elif event == Keys.button_submit.value: #Only available in the case of a new keyword
                if values[Keys.flag_onceoff.value]:
                    self.data[Keys.data_subcategory.value] = values[Keys.selection_onceoff.value][0].title() #extract and format as title
                elif values[Keys.flag_new_kw.value]: # To be explicit, but submit can't be access without keyword
                    self.data[Keys.data_new_kw.value] = values[Keys.new_keyword.value].upper() # extract the keyword
                    if values[Keys.new_subcategory.value]: # changed to rely on the CB's 
                        self.data[Keys.data_subcategory.value] = values[Keys.new_subcategory.value].title()
                        self.data[Keys.data_category.value] = values[Keys.selection_category.value][0]
                        self.data[Keys.data_bucket.value] = values[Keys.selection_bucket.value][0]
                        self.data[Keys.data_class.value] = values[Keys.selection_class.value][0]
                    else:
                        self.data[Keys.data_subcategory.value] = values[Keys.selection_subcategory.value][0].title() # extract subcategory        
        
                print("Finished with the following data:")
                [print(f"{k}: {v}") for k, v in self.data.items()]
                break       

           # updating the search lists
            elif event == Keys.searchterm_subcategory.value: # if there's a change in the search term
                self.updateList(values[Keys.searchterm_subcategory.value], self.subcategoryList, Keys.selection_subcategory.value) # update subcategories on display
            
            elif event == Keys.searchterm_category.value: # if there's a change in the search term
                self.updateList(values[Keys.searchterm_category.value],self.categoryList,Keys.selection_category.value) # update categories on display
            
            elif event == Keys.searchterm_onceoff.value:
                self.updateList(values[Keys.searchterm_onceoff.value], self.subcategoryList, Keys.selection_onceoff.value)
                  

            # if there's a change to any of the flag checkboxes, update visibility
            # this can be refactored to be neater
            
            elif event == Keys.flag_new_kw.value:
                print(f"showNewKWFrame was {self.showNewKWFrame} and is now {not self.showNewKWFrame}")
                self.showNewKWFrame = not self.showNewKWFrame
                self.window[Keys.frame_new_kw.value].update(visible=self.showNewKWFrame)

            elif event == Keys.flag_new_subcat.value:
                print(f"showNewSubcatFrame was {self.showNewSubcatFrame} and is now {not self.showNewSubcatFrame}")
                self.showNewSubcatFrame = not self.showNewSubcatFrame
                self.window[Keys.frame_new_subcat.value].update(visible = self.showNewSubcatFrame)

            elif event == Keys.flag_onceoff.value:
                print(f"showNewSubcatFrame was {self.showNewSubcatFrame} and is now {not self.showNewSubcatFrame}")
                self.showOnceOffFrame = not self.showOnceOffFrame
                self.window[Keys.frame_onceoff.value].update(visible = self.showOnceOffFrame)

            # elif event in ("-NEW KW FLAG-", "-NEW SUBCAT FLAG-", "-ONCEOFF FLAG-"):
            #     toChange = self.flag2FrameMap[event]
            #     self.toggleFrameVisibility(toChange) # show or hide frames
            
            """disable/enable submit based on once-off checkbox"""
            # if values['-ONCEOFF FLAG-']:
                # self.window['-NEW KW FLAG-'].update(disabled = True) # if once off, disable NEW KEYWORD
                # if self.isSelected(values['-ONCEOFF LISTBOX-']):
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