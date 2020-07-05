from enum import Enum, auto

class Flag(Enum):
    flag_new_kw = "flag_new_kw"
    flag_new_subcat = "flag_new_subcat"
    flag_onceoff = "flag_onceoff"
    flag_debug = "flag_debug"

class Button(Enum):
    button_submit = "button_submit"
    button_end_program = "button_end_program"

class Data(Enum):
    data_subcategory = "data_subcategory"
    data_new_kw = "data_new_kw"
    data_is_new_subcategory = "data_is_new_subcategory"
    data_category = "data_category"
    data_bucket = "data_bucket"
    data_class = "data_class"
    data_end_flag = "data_end_flag"

class Frame(Enum):    
    frame_new_kw = "frame_new_kw"
    frame_new_subcat = "frame_new_subcat"
    frame_onceoff = "frame_onceoff"

class New(Enum):
    new_keyword = "new_keyword"
    new_subcategory = "new_subcategory"

class Selection(Enum):
    selection_category = "selection_category"
    selection_subcategory = "selection_subcategory"
    selection_bucket = "selection_bucket"
    selection_onceoff = "selection_onceoff"
    selection_class = "selection_class"
    
class SearchTerm(Enum):
    searchterm_onceoff = "searchterm_onceoff"
    searchterm_subcategory = "searchterm_subcategory"
    searchterm_category = "searchterm_category"   
    
class Tooltips(Enum):
    tooltip_submit = "Only unique keywords and subcategories can be submitted..."