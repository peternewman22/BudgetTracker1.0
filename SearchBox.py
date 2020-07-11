import PySimpleGUI as sg

class SearchBox:
    """Handles construction of a searchbox"""
    def __init__(self, search_desc, search_list, choice_key, display_rows, is_searchable=True, search_key=None ):
        self.search_desc = search_desc # fills the blank: Choose a ____
        self.search_list = search_list # list to filter
        self.choice_key = choice_key
        self.display_rows = display_rows
        self.is_searchable = is_searchable
        self.search_key = search_key # to id search key and detect updates        

    def getRows(self):
        """Creates layout depending on if searchability"""
        if self.is_searchable:
            return [
                [sg.T(f"Choose a {self.search_desc}: "), sg.InputText(key=self.search_key, enable_events = True)],
                [sg.Listbox(self.search_list, key = self.choice_key, size=(20,self.display_rows), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]]
        else:
            return [
                [sg.T(f"Choose a {self.search_desc}: ")],
                [sg.Listbox(self.search_list, key = self.choice_key, size=(20,self.display_rows), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]]
    
    def addToFrame(self,frameLayout):
        for eachRow in self.getRows():
            frameLayout.append(eachRow)
        return frameLayout