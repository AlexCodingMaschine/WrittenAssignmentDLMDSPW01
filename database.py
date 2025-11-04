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



# ------------------------------------------------------------------
# To load the ideal table into TABLE2 we will do a for loop, we could
# also do it manually but it would look pretty bad
# ------------------------------------------------------------------

ideal_path = 'Datasets/ideal.csv' 
df_ideal = pd.read_csv(ideal_path, header=None, skiprows=1)

# build column names: X, Y1..Yn (auto-detect number of function columns)
num_funcs = df_ideal.shape[1] - 1
#df_ideal.shape is a tuple with the number of rows and columns and for the Y Columns we just need 50 (we also just could hardcode it)




cols = ['X'] + [f'Y{i}' for i in range(1, num_funcs + 1)]
df_ideal.columns = cols

# convert all to numeric, basicly we are doing this for bokeh
for c in cols:
    df_ideal[c] = pd.to_numeric(df_ideal[c], errors='coerce')

# write to the DATABASE
df_ideal.to_sql('Table2', con=engine, if_exists='replace', index=False)

# show first 5 rows from the database just for testing
df_ideal_db = pd.read_sql('SELECT * FROM Table2', con=engine)
print('\nFirst 5 rows from the Table2 table:')
print(df_ideal_db.head())
#head() = head(5) -> Shows the first 5 rows of the database 






#HERE STARTS THE VISUALIZATION PART

# Output to static HTML file
output_file("bokeh_plot.html")

# Create a new plot with a title and axis labels
p = figure(title="X vs Y1", x_axis_label='X', y_axis_label='Y1')

# Add a line renderer with legend and line thickness
p.line(df['X'], df['Y1'], legend_label="Y1", line_width=2)

# Show the results
show(p)