#This program is for the first part of the task
#To load the csv files into the databases

from bokeh.plotting import figure, show, output_file
import pandas as pd
from sqlalchemy import create_engine, Column, Float, MetaData, Table

#My connection to the database
engine = create_engine('sqlite:///database.db')

#Holds Data about tables and schemas
meta = MetaData()

table1 = Table('Table1', meta,
               Column('X', Float, primary_key=True),
               Column('Y1', Float),
               Column('Y2', Float),
               Column('Y3', Float),
               Column('Y4', Float)
               )

#Create the table in the database with the defined schema stored in meta
meta.create_all(engine)

# Load data from CSV and insert into the database
df = pd.read_csv('Datasets/train.csv', header=None, skiprows=1)
df.columns = ['X', 'Y1', 'Y2', 'Y3', 'Y4']

# Convert columns to numeric (in case they are read as strings)
#PS: They are always read as strings (What a mess)
#And we need them numeric for bokeh to plot them
for col in ['X', 'Y1', 'Y2', 'Y3', 'Y4']:
    df[col] = pd.to_numeric(df[col], errors='coerce')


df.to_sql('Table1', con=engine, if_exists='replace', index=False)

# Read back and print the first 5 rows from the database
df_db = pd.read_sql('SELECT * FROM Table1', con=engine)
print('First 5 rows from the database:')
print(df_db.head())


# Debug: print DataFrame info before plotting: Checked for data type
#print(df.dtypes)
#print(df.isna().sum())







#HERE STARTS THE VISUALIZATION PART

# Output to static HTML file
output_file("bokeh_plot.html")

# Create a new plot with a title and axis labels
p = figure(title="X vs Y1", x_axis_label='X', y_axis_label='Y1')

# Add a line renderer with legend and line thickness
p.line(df['X'], df['Y1'], legend_label="Y1", line_width=2)

# Show the results
show(p)