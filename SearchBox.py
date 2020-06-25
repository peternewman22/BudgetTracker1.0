import PySimpleGUI as sg

class SearchBox:
    """Handles construction of a searchbox"""
    def __init__(self, title, choiceKey, searchList, displaySize, searchable=True, searchKey=None ):
        self.title = title # fills the blank: Choose a ____
        self.choiceKey = choiceKey # to id user choice
        self.searchable = searchable # doesn't have to be searchable
        self.searchKey = searchKey # to id search key and detect updates
        self.searchList = searchList # list to filter
        self.displaySize = displaySize # how many rows to display

    def getRows(self):
        """Creates layout depending on if searchability"""
        if self.searchable:
            return [
                [sg.T(f"Choose a {self.title}: "), sg.InputText(key=self.searchKey, enable_events = True)],
                [sg.Listbox(self.searchList, key = self.choiceKey, size=(20,self.displaySize), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]]
        else:
            return [
                [sg.T(f"Choose a {self.title}: ")],
                [sg.Listbox(self.searchList, key = self.choiceKey, size=(20,self.displaySize), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]]
    
    def addToFrame(self,frameLayout):
        for eachRow in self.getRows():
            frameLayout.append(eachRow)
        return frameLayout