import pandas as pd
from Helper import Helper
from Gui import Gui

class Application:
    """Can create the initial maps, handles dataframes, iterates through the descriptions"""
    def __init__(self, fname, in_manual_mode):
        self.statement = self.process_statement(fname)
        self.in_manual_mode = in_manual_mode
        self.descriptions = self.statement["Searchable Description"].to_list()
        self.subcat_map = self.get_subcat_map()
        self.subcategories = self.get_subcategories()
        self.categories = self.get_categories()
        self.bucket_list = self.get_bucket_list()
        self.kwMap = self.get_kw_map()
        self.kwList = self.get_kw_list()
        

    def get_bucket_list(self):
        return list(set(map(lambda x: x["Bucket"], self.subcat_map.values())))
    
    def process_statement(self, fname):
        df = None
        if Helper.extractFileExtension(fname) == '.xlsx':
            df =  pd.read_excel(fname,parse_dates=[0,1])
        elif Helper.extractFileExtension(fname) == '.csv':
            df = pd.read_csv(fname, parse_dates=[0,1])
        else:
            raise ValueError("filename must contain the file extension .xlsx or .csv")
       
        # Add Year, Month and Upper Case Description Columns
        df["Year"] = df.apply(lambda row: Helper.getYear(row), axis = 1)
        df["Month"] = df.apply(lambda row: Helper.getMonth(row), axis = 1)
        df["Searchable Description"] = df.apply(lambda row: Helper.allCapsify(row), axis=1)
        return df

    def get_subcat_map(self):
        return Helper.loadJson("subcatMap.json")
    
    def get_kw_map(self):
        return Helper.loadJson("kwMap.json")

    def get_kw_list(self):
        return list(set(self.kwMap.keys()))
    
    def get_subcategories(self):
        """Extract from subcategories from subcatMap"""
        return sorted(list(set(self.subcat_map.keys())))

    def get_categories(self):
        """Extract from categories from subcatMap"""
        return sorted(list(set(map(lambda eachValue: eachValue['Category'], self.subcat_map.values()))))

    def get_matches(self,desc):
        return list(set(filter(lambda eachKW: eachKW in desc, self.kwList)))

    def generate_GUI(self, desc, matches):
        return Gui(desc, self.kwMap, matches, self.subcat_map, self.subcategories, self.categories, self.bucket_list, self.kwList)
    
    def save_new_kw(self,newKW, subcategory):
        """Adds an entry to the kwMap then refreshes downstream lists"""
        print(f"Saving new Keyword: {newKW}")
        self.kwMap[newKW] = subcategory
        Helper.saveJson(self.kwMap,"kwMap.json")
        self.kwList = self.get_kw_list()

    def save_new_subcategory(self,subcategory,category,bucket,newSubcatClass):
        """Adds an entry to the subcatMap then refreshes downstream lists"""
        self.subcat_map[subcategory] = {"Category": category, "Bucket": bucket, "Class" : newSubcatClass}
        Helper.saveJson(self.subcat_map, "subcatMap.json")
        self.subcategories = self.get_subcategories()
        self.categories = self.get_categories()
        self.bucket_list = self.get_bucket_list()

    def loop(self):
        """Loops through the descriptions, gathering subcategories and writing to csv"""
        for index in range(len(self.descriptions)):
            eachDesc = self.descriptions[index]
            matches = self.get_matches(eachDesc)
            print(f"Matches found: {len(matches)}")
            if len(matches) != 1 or self.in_manual_mode: # If it's safeMode ALWAYS prompt
                gui = self.generate_GUI(eachDesc, matches)
                # use the gui to find the correct subcategory
                data = gui.getSubcategoryLoop()
                
                if data['End']: # Detecting end program trigger
                    break
                
                subcategory = data['Subcategory'] # extract the subcategory
                if data['New Keyword'] != None: # if a new keyword is declared, then save it and extract the subcategory which will be chosen
                    self.save_new_kw(data['New Keyword'], subcategory)
                if data['New Subcategory']: # if a new 
                    self.save_new_subcategory(subcategory, data['Category'], data['Bucket'], data['Class'])  
                
            elif not self.in_manual_mode and len(matches) == 1: # Alternative: subcategory is automatically categorised based on the keyword map
                subcategory = self.kwMap[matches[0]]
            
            row = self.statement.iloc[index,:].to_list() # construct the row from the dataframe and add the subcategory
            row.append(subcategory)
            row.append(self.subcat_map[subcategory]['Category'])
            row.append(self.subcat_map[subcategory]['Bucket'])
            row.append(self.subcat_map[subcategory]['Class'])
            # write the row to the output.csv file
            Helper.write2csv(row)


    
