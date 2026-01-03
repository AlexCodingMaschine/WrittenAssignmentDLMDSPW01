from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

DB = 'database.db'
engine = create_engine(f'sqlite:///{DB}')


def read_tables():
    """Read tables from database."""
    df_train = pd.read_sql('SELECT * FROM Table1', con=engine) #Training data
    df_ideal = pd.read_sql('SELECT * FROM Table2', con=engine) #Ideal functions
    try:
        df_test = pd.read_sql('SELECT * FROM Table3', con=engine) #Test matches
    except Exception:
        df_test = None
    return df_train, df_ideal, df_test #Return training, ideal, and test dataframes


def make_confirm_plot(df_train, df_ideal, chosen_names, df_test=None): #Plot the training data, chosen ideal functions, and test points
    """Make a confirmation plot showing training data, chosen ideal functions, and test points."""
    output_file('confirm_top4.html', title='Confirm top-4 vs training') #Tells Bokeh to output to this HTML file
    p = figure(title='Training series + Top-4 Ideal Functions + Test Points', #Creates a Bokeh figure with labels, size, and background color
               x_axis_label='X', y_axis_label='Y', height=500, width=800,
               background_fill_color="#fafafa")


    """Takes the first column as X values,
    Loops through the first 5 Y columns and plots them as gray lines,
    these represent the original training data"""
    x_train = df_train.iloc[:, 0].values
    for col in df_train.columns[1:6]:  # show only first few to avoid clutter
        p.line(x_train, df_train[col].values, line_alpha=0.5,
               line_width=1.5, color='gray', legend_label='Training series')

    """Sorts X values for ideal functions (to make smooth lines),
    plots the top 4 chosen ideal functions in different colors"""
    x_ideal = df_ideal.iloc[:, 0].values
    idx = np.argsort(x_ideal)
    x_ideal_sorted = x_ideal[idx]
    colors = ['orange', 'green', 'blue', 'red']
    for i, name in enumerate(chosen_names[:4]):
        if name in df_ideal.columns:
            y = df_ideal[name].values[idx]
            p.line(x_ideal_sorted, y, line_color=colors[i],
                   line_width=2.5, legend_label=f'Ideal: {name}')

    #Overlay test points
    """For each ideal function, plots test points assigned to it as colored dots.
    If a test point wasn’t assigned to any ideal, its plotted as a black cross (there will be no)"""
    if df_test is not None and not df_test.empty:
        color_map = {
            chosen_names[0]: 'orange',
            chosen_names[1]: 'green',
            chosen_names[2]: 'blue',
            chosen_names[3]: 'red'
        }
        for ideal in chosen_names: #Loop through each chosen ideal function
            df_subset = df_test[df_test['IdealName'] == ideal] #Filter test points for this ideal
            if not df_subset.empty: #If there are test points for this ideal
                p.scatter(df_subset['X'], df_subset['Y'],
                          size=6, color=color_map.get(ideal, 'black'), 
                          alpha=0.8, legend_label=f'Test -> {ideal}') #Plot test points as colored dots

        # Unassigned points (None)
        df_none = df_test[df_test['IdealName'].isna()]
        if not df_none.empty:
            p.cross(df_none['X'], df_none['Y'], size=6, color='black',
                    alpha=0.6, legend_label='Unassigned test points') #black crosses for unassigned points

    p.legend.click_policy = 'hide' #Make legend entries clickable for hiding
    p.legend.label_text_font_size = "10pt" #font size
    p.legend.location = "top_left" #legend location will be top left when the html will be opened

    show(p) #we automatically open the plot in the browser


"""Reads tables,
extracts the list of chosen ideal functions from Table3 and
calls make_confirm_plot() to generate the visualization."""
def main():
    """Generate visualization from database tables."""
    df_train, df_ideal, df_test = read_tables()

    # Get chosen ideals from Table3 (which ideals were actually used)
    if df_test is not None and not df_test.empty:
        chosen_names = df_test['IdealName'].dropna().unique().tolist()
    else:
        raise ValueError("Table3 not found. Run the pipeline first to generate test matches.")

    print('Confirmed chosen/top-4 for plotting:', chosen_names[:4])
    make_confirm_plot(df_train, df_ideal, chosen_names, df_test)


if __name__ == '__main__':
    main() #Call main
