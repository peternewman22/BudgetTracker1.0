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
        self.event = None
        self.values = None
        self.event_dict = self.generate_event_dict()
        self.looping = True
        
    def generate_event_dict(self) -> dict:
        event_dict =  {
            Keys.event_submit : self.handle_event_submit,
            Keys.event_end_program : self.handle_event_end_program_break_loop,
            Keys.event_cancel : self.handle_event_cancel_break_loop,
            Keys.event_uncategorised : self.handle_event_uncategorised_break_loop,
            Keys.searchterm_subcategory : lambda : self.updateList(self.values[Keys.searchterm_subcategory], self.subcategoryList, Keys.selection_subcategory),
            Keys.searchterm_category : lambda : self.updateList(self.values[Keys.searchterm_category],self.categoryList,Keys.selection_category),
            Keys.searchterm_onceoff :  lambda : self.updateList(self.values[Keys.searchterm_onceoff], self.subcategoryList, Keys.selection_onceoff),
            Keys.flag_new_kw : self.handle_event_flag_new_kw_toggle_visibility,
            Keys.flag_new_subcat : self.handle_event_flag_new_subcat_toggle_visibility,
            Keys.flag_onceoff : self.handle_event_flag_onceoff_toggle_visibility
        }
        # adding the quickmatches to the dictionary
        for eachMatch in self.matches:
            event_dict[eachMatch] = lambda : self.handle_quickmatch(eachMatch)

        return event_dict
    
    def handle_event(self) -> None:
        self.event_dict[self.event]
    
    def handle_quickmatch(self, quickMatch: str) -> None:
        self.data[Keys.data_subcategory] = self.kwMap[quickMatch]
        print(f"Categorised using {quickMatch} --> {self.data[Keys.data_subcategory]}")
        self.looping = False

    def handle_event_submit(self) -> None:
        if self.values[Keys.flag_onceoff]:
                self.data[Keys.data_subcategory] = self.values[Keys.selection_onceoff][0].title() #extract and format as title
        elif self.values[Keys.flag_new_kw]: # To be explicit, but submit can't be access without keyword
                self.data[Keys.data_new_kw] = self.values[Keys.new_keyword].upper() # extract the keyword
                if self.values[Keys.new_subcategory]: # changed to rely on the CB's 
                    self.data[Keys.data_subcategory] = self.values[Keys.new_subcategory].title()
                    self.data[Keys.data_category] = self.values[Keys.selection_category][0]
                    self.data[Keys.data_bucket] = self.values[Keys.selection_bucket][0]
                    self.data[Keys.data_class] = self.values[Keys.selection_class][0]
                else:
                    self.data[Keys.data_subcategory] = self.values[Keys.selection_subcategory][0].title() # extract subcategory        
    
        print("Finished with the following data:")
        [print(f"{k}: {v}") for k, v in self.data.items()]
        self.looping = False   

    def handle_event_end_program_break_loop(self) -> None:
        self.data[Keys.data_end_flag] = True
        print('Ending program without categorising the last value')
        self.looping = False

    def handle_event_cancel_break_loop(self) -> None:
        print("Categorised as 'Uncategorised'")
        self.looping = False

    def handle_event_uncategorised_break_loop(self):
        print("Categorised as 'Uncategorised'")
        self.looping = False

    def handle_event_flag_new_kw_toggle_visibility(self):
        self.showNewKWFrame = not self.showNewKWFrame
        self.window[Keys.frame_new_kw].update(visible=self.showNewKWFrame)

    def handle_event_flag_new_subcat_toggle_visibility(self):
        self.showNewSubcatFrame = not self.showNewSubcatFrame
        self.window[Keys.frame_new_subcat].update(visible = self.showNewSubcatFrame)
    
    def handle_event_flag_onceoff_toggle_visibility(self):
        self.showOnceOffFrame = not self.showOnceOffFrame
        self.window[Keys.frame_onceoff].update(visible = self.showOnceOffFrame)

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
        # makes checkboxes: newKW, newSubcat --> used to reveal parts of the window
        onceoff = sg.CB("Once-Off", default = False, key = Keys.flag_onceoff, enable_events=True)
        newKW = sg.CB("New Keyword", default = False, key = Keys.flag_new_kw, enable_events=True)
        newSubcat = sg.CB("New Subcat", default = False, key = Keys.flag_new_subcat, enable_events=True)
        return [onceoff, newKW, newSubcat]

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
            [sg.Button(Keys.event_uncategorised.value,key=Keys.event_uncategorised),sg.Submit(disabled=False, key=Keys.event_submit, tooltip = self.submitTooltip), sg.Cancel(key=Keys.event_cancel),sg.Button(Keys.event_end_program.value, key=Keys.event_end_program)]
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
        return len(listToCheck) == 1

    def generateWindow(self):
        """Creates a new window"""
        return sg.Window("Categorise Me!", self.generateCompleteLayout())
    
    def createDataTemplate(self):
        return {
            Keys.data_subcategory : Keys.event_uncategorised.value,
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
        while self.looping:
            self.event, self.values = self.window.Read(timeout = 1000)
            self.handle_event()

        self.window.close()
        self.window = None
        return self.data