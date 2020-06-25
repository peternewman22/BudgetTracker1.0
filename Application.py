import pandas as pd
from Helper import Helper
from Gui import Gui

class Application:
    """Can create the initial maps, handles dataframes, iterates through the descriptions"""
    def __init__(self, fname, safeMode):
        self.statement = self.processStatement(fname)
        self.safeMode = safeMode
        self.descriptions = self.statement["Searchable Description"].to_list()
        self.subcatMap = self.getSubcatMap()
        self.subcategories = self.getSubcategories()
        self.categories = self.getCategories()
        self.bucketList = self.getBucketList()
        self.kwMap = self.getKWMap()
        self.kwList = self.getKWList()
        

    def getBucketList(self):
        """Returns a complete, unique list of buckets"""
        return list(set(map(lambda x: x["Bucket"], self.subcatMap.values())))
    
    def processStatement(self, fname):
        df = None
        if Helper.extractFileExtension(fname) == '.xlsx':
            df =  pd.read_excel(fname,parse_dates=True)
        elif Helper.extractFileExtension(fname) == '.csv':
            df = pd.read_csv(fname, parse_dates=True)

        # Add Year Column
        try:
            df["Year"] = df.apply(lambda row: Helper.getYear(row), axis = 1)
        except Exception as e:
            print(f"Error extracting year: {e}")

        # Add Month Column
        try:
            df["Month"] = df.apply(lambda row: Helper.getMonth(row), axis = 1)
        except Exception as e:
            print(f"Error extracting month: {e}")

        # Making each Description entirely upper case
        try:
            df["Searchable Description"] = df.apply(lambda row: Helper.allCapsify(row), axis=1)
        except Exception as e:
            print(f"Problems capitalizing descriptions: {e}")
        return df

    def getSubcatMap(self):
        return Helper.loadJson("subcatMap.json")
    
    def getKWMap(self):
        return Helper.loadJson("kwMap.json")

    def getKWList(self):
        return list(set(self.kwMap.keys()))
    
    def getSubcategories(self):
        """Extract from subcategories from subcatMap"""
        return sorted(list(set(self.subcatMap.keys())))

    def getCategories(self):
        """Extract from categories from subcatMap"""
        return sorted(list(set(map(lambda eachValue: eachValue['Category'], self.subcatMap.values()))))

    def getMatches(self,desc):
        return list(set(filter(lambda eachKW: eachKW in desc, self.kwList)))

    def generateGUI(self, desc, matches):
        return Gui(desc, self.kwMap, matches, self.subcatMap, self.subcategories, self.categories, self.bucketList, self.kwList)
    
    def saveNewKW(self,newKW, subcategory):
        """Adds an entry to the kwMap then refreshes downstream lists"""
        print(f"Saving new Keyword: {newKW}")
        self.kwMap[newKW] = subcategory
        Helper.saveJson(self.kwMap,"kwMap.json")
        self.kwList = self.getKWList()

    def saveNewSubcategory(self,subcategory,category,bucket,newSubcatClass):
        """Adds an entry to the subcatMap then refreshes downstream lists"""
        self.subcatMap[subcategory] = {"Category": category, "Bucket": bucket, "Class" : newSubcatClass}
        Helper.saveJson(self.subcatMap, "subcatMap.json")
        self.subcategories = self.getSubcategories()
        self.categories = self.getCategories()
        self.bucketList = self.getBucketList()

    def loop(self):
        """Loops through the descriptions, gathering subcategories and writing to csv"""
        for index in range(len(self.descriptions)): # use an index so we can also get the whole row from the df
            eachDesc = self.descriptions[index]
            # find kw matches
            matches = self.getMatches(eachDesc)
            print(f"Matches found: {len(matches)}")
            # construct a gui object
            if len(matches) != 1 or self.safeMode: # If it's safeMode ALWAYS prompt
                gui = self.generateGUI(eachDesc, matches)
                # use the gui to find the correct subcategory
                data = gui.getSubcategoryLoop()
                subcategory = data['Subcategory'] # extract the subcategory
                if data['New Keyword'] != None: # if a new keyword is declared, then save it and extract the subcategory which will be chosen
                    self.saveNewKW(data['Keyword'], subcategory)
                if data['New Subcategory']: # if a new 
                    self.saveNewSubcategory(subcategory, data['Category'], data['Bucket'], data['Class'])
                
                
            elif not self.safeMode and len(matches) == 1:
                subcategory = self.kwMap[matches[0]]
            # construct the row from the dataframe and add the subcategory
            row = self.statement.iloc[index,:].to_list()
            row.append(subcategory)
            row.append(self.subcatMap[subcategory]['Category'])
            row.append(self.subcatMap[subcategory]['Bucket'])
            row.append(self.subcatMap[subcategory]['Class'])
            # write the row to the output.csv file
            Helper.write2csv(row)


    
