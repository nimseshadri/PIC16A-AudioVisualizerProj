# PIC16A-ClareCoxCrochetDataAnalysis
 
## Group members: @ubpollack, @nimdseshadri, @clarenellie

### Project Description
In this project, we created a data visualizer tool that takes in user input to first select a type of visualization and has the user to input the variables which will be plottef on the chosen visualization. We constructed this program/tool around data from one of our members Nellie's small crochet business on instagram, in which she had recorded the relevant variables of each post she created from over 3 years ago.

### Packages + Versions Used
The following packages were employed to complete this project:
- pandas 1.4.2
- numpy 1.23.5
- matplotlib 3.5.1
- functools

### Demo File Instructions
(How to run it, expected outputs, and any explanations/interpretations of the results + 2 figures of visualizations w/ titles, captions, and sufficient explanation in text here)
When you first run the demo file "Data Viz Program Demo"--which is a Jupyter notebook that imports the main crochet.py file--it begins by welcoming the user to the program and asking them to choose a number from the menu. The menu, numbered 0 to 5, lists 5 possible visualization options to choose from, as well as the choice to enter 0 to quit the program. 

Each vizualization can either take one or two variables (defined as the column names in the data spreadsheet) from the Instagram accounts' post dataset, depending on the visualization chosen and the types of data it is intended for. To specify,
- The scatterplot intakes 2 variable arguments, ideally of numerical nature
- The timeline takes 1 variable argument and plots it's behavior over the recorded years
- The histogram can take 2 variable arguments, ideally of categorical nature
- The boxplot takes 2 variable arguments, it
Though there are ideal variables to be used in each kind of visualizarion, there are many instances in which the plotter will run and create a visually unappealing graph; there are simply too many combinations of column variables which woulc

To execute this program, 

### Scope and Limitations
(Any ethical implications, accessibility concerns, and ideas for potential extensions)
This program has a limited scope as it was specifically designed to be able to work with a single dataframe which was provided by group member 
@clarenellie. The program is able to analyze social media data for a microbusiness which sells and posts about crochet items. The program will not provide
very specific insights for an individuals personal account but it may do a good job for data from another business account, assuming the dataframe is 
formatted the same as the Clare Cox Crochet Social Media dataframe the program was designed for.

### References and Acknowledgment (?)

### Background of Dataset 
This data was hand-collected over the course of 3 years by Nellie Cox. Everytime she created a post on the business account @clarecox.crochet, she hand-recorded all relevant information to describe the post, such as date posted, the type of item featured, likes received, comments, saves, etc. This 
amounted to a total of 19 recorded variables/columns.

### Software demo video: 
Extra credit video demoing use of this program


