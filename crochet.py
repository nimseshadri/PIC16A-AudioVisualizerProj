import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps


class CrochetDataVisualizer:
    def __init__(self, df):
        self.df = self.preprocess(df)
    
    def preprocess(self, df):
        '''
        Takes in the dataframe that is input. Cleans up data so that it only includes what we plan to be able to work with.
        Drops unnecessary indexes, makes the dates column into dates python can read and gets rid of additional columns. Gets rid of outiers in the df.
        Reformats data in columns so that the computer can read it.
        Args:
        Clare Cox Crochet dataframe
        Returns:
        Clare Cox Crochet dataframe but cleaned up
        '''
        df.drop(["Unnamed: 0"], axis=1, inplace=True)  # get rid of unnecessary index
        
        df['Date'] = pd.to_datetime(df["Date"])  # make dates
        df.drop(['Day of Week', 'Month', 'Year'], axis=1, inplace=True)  # no longer need this info
        
        df = df[df["number of pictures in post"] != 'video'].copy()            # get rid of outlier: video
        # turn percent following column into floats
        df["percent weren't following"] = df["percent weren't following"].replace({'-': '-1', '': '-1'}).astype(np.float64).replace({-1.:np.nan}) 
        numerify = ["number of pictures in post", 'profile visits', "follows"] # columns whose datatype should be made into numbers put into an array
        df[numerify] = df[numerify].astype(np.int16)                           # turns appropriate data in the data frame into numbers (int16)
        
        df["number of days since previous post"] = df['Date'].diff()           # .diff() will get the number of days between each date there was a post
        
        df["product type"] = df["product type"].fillna("none")                 # replaces null items in product type to 'none'
        
        general_product_types = [] # create a list that will become a new column in the dataframe with the more general categories of 
        
        # loop through all the items in the product type column and search for substrings to put them in a more general category of product
        for item in df.loc[:, 'product type']:
            item = str(item)                          # convert item to a string to check for substrings
            if 'top' in item:                         # if top is in an item then add top to its index in general_product_types
                general_product_types.append('top')
            elif 'sweater' in item:                   # if sweater is in the item string then add it as top in general_product_types
                general_product_types.append('top')
            elif 'hat' in item:                       # if hat is in the item string add it as hat
                general_product_types.append('hat')
            elif 'beanie' in item:                    # if beanie is in the item string at it as hat
                general_product_types.append('hat')
            elif 'bag' in item:                       # if bag is in the item string add it as bag
                general_product_types.append('bag')
            elif 'pack' in item:                      # if pack is in the item string add it as bag
                general_product_types.append('bag')
            else:
                general_product_types.append('other') # if none of the above strings appear in an item of 'product types' append 'other' to the general_product_types
        
        # turn general_product_types into a new column in the data frame
        df['general_product_types'] = general_product_types 
       
        # converts categorical variables into dummies where numbers will correstp
        cats = {"who's featured": None, 'product type': None, 'purpose': None, 'season': None} # a dict of the categorical variables we want to work with
        for cat in cats:                                                                       # loops through them and gets the dummies of the variables
            onehot = pd.get_dummies(df[cat])
            cats[cat] = onehot                                                                 # replaces the categorical items with the dummies
            
        df.rename(lambda string: string.replace(" ", "_"), axis=1, inplace=True)               # rename strings in the df and replace spaces with underscores
        
        return df
    
    def _validate_columns(self, *cols):
        """
        Validates column names
        Args:
        - *cols: every positional argument should be a column name
        Returns:
        - None
        Raises:
        - KeyError if the column name isn't in self.df
        """
        for col in cols:      # loop through the columns that were input
            try:              # first try the column
                self.df[col]
            except KeyError:  # if there's a KeyError print this
                raise KeyError(f'"{col}" is not a column in the crochet data')
                
    def _validate_column_dec(func):
        """
        Decorator that checks to make sure the positional arguments of a method are column names of self.df
        Used for plot methods below, because these only accept column names as positional arguments
        Args:
        - func: a method of CrochetDataVisualizer that should only accept column names as positional arguments
        Returns:
        - the same function with the added validation logic (raises descriptive KeyError when column is not found)
        """
        @wraps(func)                   
        def ret_func(self, *pos, **kw):
            self._validate_columns(*pos)
            return func(self, *pos, **kw)
        return ret_func
        
    @_validate_column_dec
    def scatterplot(self, x, y):
        """
        Creates a scatterplot
        Args:
        - x: column name
        - y: column name
        Returns:
        - None
        Displays:
        - scatterplot of y vs x
        """
        plt.scatter(self.df[x], self.df[y], color = 'pink')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(x + " vs. " + y)
        plt.show()
        
    @_validate_column_dec
    def timeline(self, y):
    '''
    For creating plots which show how a variable changesover time. creates the x-axis and then calls _validate_column_dec
    Args:
    y: a column in the data frame which will be plotted in the y axis
    Returns:
    Nothing
    
    '''
        plt.scatter(self.df["Date"], self.df[y], color = 'pink')
        plt.xticks(rotation = 90)
        plt.xlabel("Date")
        plt.title(y + " overtime")
        plt.ylabel(y)
        plt.show()
        
    @_validate_column_dec
    def histogram(self, *xs):
        for x in xs:
            plt.hist(self.df[x], alpha=0.5, label=x)
        plt.title("frequency of inputted data")
        plt.legend()
        plt.show()
    
    @_validate_column_dec
    def boxplot(self, y, groups=None):
        if groups is not None:
            self._validate_columns(groups)
            labs, boxes = zip(*((group, df[y]) for group, df in self.df.groupby(groups)))
            plt.boxplot(boxes,labels=labs)
            plt.xlabel(groups)
        else:
            plt.boxplot(self.df[y])
        plt.ylabel(y)
        plt.title(y + " data summary")
        plt.show()
        
    @_validate_column_dec
    def barplot(self, x, y):
        plt.bar(self.df[x], self.df[y], color = 'pink')
        plt.xticks(rotation = 90)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(x + " vs. " + y)
        plt.show()

        
input_sym = "> "

def print_colnames(viz):
    print("Here are the column names:")
    for name in viz.df.columns:
        print(name)

def runner(viz, func):
    print("Choose some column names (case sensitive). Enter 1-2 inputs, separate with spaces. Inputs correspond to (x,y) respectively. ")
    while True:
        try:
            colnames = input(input_sym).split()
            func(*colnames)
            return
        except KeyError:
            print("Please give valid column names:")
            print_colnames(viz)
    
def main():
    dataviz = CrochetDataVisualizer(pd.read_csv("Clare Cox Crochet Social Media Data - Instagram Data.csv"))
    
    welcome = """
    Welcome to the plotter!
    Choose a number from this menu:
    """
    
    menu = {
        1: dataviz.scatterplot,
        2: dataviz.timeline,
        3: dataviz.histogram,
        4: dataviz.boxplot,
        5: dataviz.barplot
    }
    
    print(welcome)
    while True:
        print("0.\tquit")
        for num, func in menu.items():
            print(f"{num}.\t{func.__name__}")
        
        try:
            user_num = int(input(input_sym))
        except ValueError:
            print("Please enter valid input")
            continue
        
        if user_num == 0:
            print("Quitting plotter...")
            return
        
        try:
            func = menu[user_num]
        except KeyError:
            print("Please enter valid input")
            continue
            
        runner(dataviz, func)


if __name__ == '__main__':
    main()
