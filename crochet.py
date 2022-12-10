import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps


class CrochetDataVisualizer:
    '''
    A class which bundles the cleaning and treatment of a dataset 
    containing post statistics, plus the methods for creating 5 
    different visualizations for the user's desired variables from the df. 
    
    '''
    def __init__(self, df):
        self.df = self.preprocess(df)
    
    def preprocess(self, df):
        '''
        Cleans the dataframe by sorting variables, fixing mistakes,  
        & other preliminary tasks to prepare the data to be plotted.
        Args:
            - df: the original dataframe containing the Instagram data  
        Returns:
            - df: the cleaned dataframe ready to be read
        '''
        df.drop(["Unnamed: 0"], axis=1, inplace=True)  # get rid of unnecessary index
        
        df['Date'] = pd.to_datetime(df["Date"])  # creates the dates
        df.drop(['Day of Week', 'Month', 'Year'], axis=1, inplace=True)  # no longer need this info since dates are calculated
        
        df = df[df["number of pictures in post"] != 'video'].copy()  # get rid of outlier: video
        df["percent weren't following"] = df["percent weren't following"].replace({'-': '-1', '': '-1'}).astype(np.float64).replace({-1.:np.nan})  # turn percent following column into floats
        numerify = ["number of pictures in post", 'profile visits', "follows"]
        df[numerify] = df[numerify].astype(np.int16)
        
        df["number of days since previous post"] = df['Date'].diff() # converts a
        
        df["product type"] = df["product type"].fillna("none") # fills missing values 
        
        general_product_types = [] # create a list that will become a new column in the dataframe with the more general categories of products posted about
     
        for item in df.loc[:, 'product type']:
            item = str(item)
            if 'top' in item:
                general_product_types.append('top')
            elif 'sweater' in item:
                general_product_types.append('top')
            elif 'hat' in item:
                general_product_types.append('hat')
            elif 'beanie' in item:
                general_product_types.append('hat')
            elif 'bag' in item:
                general_product_types.append('bag')
            elif 'pack' in item:
                general_product_types.append('bag')
            else:
                general_product_types.append('other')
        
        df['general_product_types'] = general_product_types # adds column to df 
       
        categories = {"who's featured": None, 'product type': None, 'purpose': None, 'season': None} # dummy codes the df for 
        for cat in categories:
            onehot = pd.get_dummies(df[cat])
            categories[cat] = onehot
            
        df.rename(lambda string: string.replace(" ", "_"), axis=1, inplace=True) # replaces the spaces with _ in column names
        
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
        for col in cols: # goes thru column names to check if name entered is valid 
            try:
                self.df[col]
            except KeyError: # if not, raise a KeyError
                raise KeyError(f'"{col}" is not a column in the crochet data')
                
    def validate_column_dec(func):
        """
        Decorator that checks to make sure the positional arguments of a method are column names of self.df
        Used for plot methods below, because these only accept column names as positional arguments
        Args:
            - func: a method of CrochetDataVisualizer that should only accept column names as positional arguments
        Returns:
            - the same function with the new validation logic (raises descriptive KeyError when column is not found)
        """
        @wraps(func) 
        def ret_func(self, *pos, **kw): # creates a function that can be applied to each plotting method 
            self._validate_columns(*pos) 
            return func(self, *pos, **kw)
        return ret_func
        
    @validate_column_dec
    def scatterplot(self, x, y):
        """
        Creates a scatterplot
        Args:
            - x: column name
            - y: column name
        Returns:
            - None
        Displays:
            - scatterplot of x vs y
        """
        plt.scatter(self.df[x], self.df[y], color = 'pink') # creates a scatter plot of data for inputted columns, makes plotted dot colors pink
        plt.xlabel(x) # labels x-axis with x column name
        plt.ylabel(y) # labels y-axis with y column name
        plt.title(x + " vs. " + y) # gives graph title 
        plt.show() # displays graph
        
    @validate_column_dec
    def timeline(self, y):
        """
        Creates a timeline
        Args:
            - y: column name
        Returns:
            - None
        Displays:
            - timeline of y overtime
        """
        plt.scatter(self.df["Date"], self.df[y], color = 'pink') # creates a scattered image of Date vs inputted y data, makes plotted dot colors pink
        plt.xticks(rotation = 90) # x-axis ticks of dates are written out at a 90 deg angle
        plt.xlabel("Date") # labels x-axis as "Date"
        plt.title(y + " overtime") # gives graph title 
        plt.ylabel(y) # labels y-axis with y column name
        plt.show() # displays graph
        
    @validate_column_dec
    def histogram(self, *xs):
        """
        Creates a histogram
        Args:
            - x: column names
        Returns:
            - None
        Displays:
            - historgram of frequncy of inputted data
        """
        for x in xs:
            plt.hist(self.df[x], alpha=0.5, label=x) # create histogram with frequency of inputted data, gives graph bars transparency of 0.5 and labels axis with x inputted data
        plt.title("frequency of inputted data") # give graph title
        plt.legend() # creates a legend indicating which bar on the graph corresponds to which collection of data
        plt.show() # shows graph
    
    @validate_column_dec
    def boxplot(self, y, groups=None):
        """
        Creates a boxplot
        Args:
            - y: column name
        Returns:
            - None
        Displays:
            - a boxplot with minimum, first quartile, median, third quartile, and maximum of inputted data
        """
        if groups is not None: # groups data that is not included in preprocessing code
            self._validate_columns(groups) 
            labs, boxes = zip(*((group, df[y]) for group, df in self.df.groupby(groups))) 
            plt.boxplot(boxes,labels=labs) # creates boxes with labels for groups
            plt.xlabel(groups) # labels graph with said groups
        else: # if data is not part of grouping it continues to plot the following
            plt.boxplot(self.df[y]) # creates box plot with inputted y column data
        plt.ylabel(y) # labels y-axis with y data name
        plt.title(y + " data summary") # gives graph title
        plt.show() # shows plot
        
    @validate_column_dec
    def barplot(self, x, y):
        """
        Creates a boxplot
        Args:
            - x: column name 
            - y: column name 
        Returns:
            - None
        Displays:
            - a barplot of x vs y
        """
        plt.bar(self.df[x], self.df[y], color = 'pink') # creates a scatter plot of data for inputted columns, makes plotted dot colors pink
        plt.xticks(rotation = 90) # x-axis ticks of dates are written out at a 90 deg angle
        plt.xlabel(x) # labels x-axis with x column name
        plt.ylabel(y) # labels y-axis with y column name
        plt.title(x + " vs. " + y) # gives graph title
        plt.show() # shows plot

        
input_sym = "> "

def print_colnames(viz):
    '''
    Prints the column names for the input to choose from
    Args:
        - viz:
    Returns:
        - None

    '''
    for name in viz.df.columns:
        print(name)

def runner(viz, func):
    '''
    Function to run the 
    Args:
        - viz:
        - func:
    Returns:
        - 
    '''
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
    '''
    Function to execute the data vizualization tool 
    Args:
        - None
    Returns:
        - None
    '''
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
