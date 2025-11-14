""" This program is for the main part of the task
 Uses the databases created by `database.py`.
 Step 1 (implemented here): find the best 4 ideal functions that fit the
 entire training set (aggregate SSE). The chosen four are saved to the DB
 in table `ChosenIdeals` and to `chosen_ideals.csv` for easy inspection."""

import numpy as np	#numerical computations
import pandas as pd	#reading/writing tables
from sqlalchemy import create_engine #Python to SQLite-database
import math #mathematical constants and functions (for sqrt)

#db_path: path to the sqlite database file
#table_train: name of the training data table
#table_ideal: name of the ideal functions table
#save_table: name of the table to save the chosen ideals


#The first defined functions returns the top4 ideal functions (smallest SSE)
def select_top4_ideals(db_path='database.db',
					  table_train='Table1',
					  table_ideal='Table2',
					  save_table='ChosenIdeals'): #Put that away maybe later

	#connect to database via sqlalchemy
	engine = create_engine(f'sqlite:///{db_path}')

	# Read tables, Read everything from both tables (into DataFrames)
	df_train = pd.read_sql(f'SELECT * FROM {table_train}', con=engine)
	df_ideal = pd.read_sql(f'SELECT * FROM {table_ideal}', con=engine)

	#print(df_train.head()) = test
	#print(df_ideal.head()) = test

	#Get the x-Column from the training data
	x_train_col = df_train.columns[0]
	
    #Gets all Y-Columns from the training data
	train_value_cols = list(df_train.columns[1:])
	#print(f'Train value columns: {train_value_cols}') = test

	#Same thing for the ideal functions table
	x_ideal_col = df_ideal.columns[0]
	ideal_cols = list(df_ideal.columns[1:])
	#print(f'Ideal function columns: {ideal_cols}') = test

	#Extract the X-values from the training data into a NumPy array
	x_train = df_train[x_train_col].values
	# print a short summary instead of the full array (too verbose)
	print(f"train X: n={len(x_train)}, min={x_train.min():.6g}, max={x_train.max():.6g}")



	#Just an empty list to later store the results
	sse_results = []

	#np.argsort = sort X ascendingly
	ideal_sort_idx = np.argsort(df_ideal[x_ideal_col].values)
	#print(ideal_sort_idx) = test 
	
	#x_ideal_sorted = sorted list of ideal X-values
	x_ideal_sorted = df_ideal[x_ideal_col].values[ideal_sort_idx]


	#At this point we have sorted train and ideal X values and now can



    #Loop through each ideal function column
	for col in ideal_cols:
		y_ideal = df_ideal[col].values[ideal_sort_idx]
		#y_ideal are sorted Y-values to match x_ideal_sorted 

		# Interpolate ideal onto train X grid; out-of-range -> NaN (conservative)
		y_at_train = np.interp(x_train, x_ideal_sorted, y_ideal, left=np.nan, right=np.nan)

		total_sse = 0.0
		any_valid = False
		#Valid Interpolation detection


		# Sum SSE across all train series
		for tcol in train_value_cols:
			y_train = df_train[tcol].values
			# residuals where both are finite
			mask = (~np.isnan(y_at_train)) & (~np.isnan(y_train))
			#Create a mask to ignore NaN values.
			if mask.any():
				res = y_train[mask] - y_at_train[mask]
				total_sse += float(np.sum(res * res))
				#Sum on top

				any_valid = True

		# If the ideal function had no overlapping X-values with training data
		if not any_valid:
			total_sse = float('inf')
			#We just give the SSE something very big so it never will be chosen

		# Store result in a tupel
		sse_results.append((col, total_sse))

	# Sort by SSE ascending and take the top 4 smallest to accomplish the first part of the task
	sse_results.sort(key=lambda x: x[1])
	top4 = sse_results[:4]


	# Print results for testing and the function returns the top4 functions
	print('Top 4 ideal functions (name, total_sse):')
	for name, sse in top4:
		print(f'  {name}: {sse}')

	return top4
	#At this point we accomplished the "fist" part of the task


def main():
	# Full pipeline: select top-4, match test points, and write Table3
	top4 = select_top4_ideals()
	# top4 is list of tuples (name, sse) -> extract names
	top4_names = [name for name, _ in top4]

	# perform matching and write results to Table3
	match_test_to_table3(top4_names)

	print('\nPipeline complete: Table3 written to database.db')


#We will call this function in main and give it the following parameters 
#We will calcualte the max. deviation for each ideal function with the training data
def compute_deviation_for_ideals(db_path='database.db', table_train='Table1', table_ideal='Table2', ideal_names=None):
	
	engine = create_engine(f'sqlite:///{db_path}')
	df_train = pd.read_sql(f'SELECT * FROM {table_train}', con=engine)
	df_ideal = pd.read_sql(f'SELECT * FROM {table_ideal}', con=engine)
	#Here we connect to database and also load the tables

	#X-Columns from train
	x_train = df_train.iloc[:, 0].values
	#Y-Columns from train
	train_value_cols = list(df_train.columns[1:])

	#Again sorting ideal X-values for the following interpolation
	x_ideal = df_ideal.iloc[:, 0].values
	sort_idx = np.argsort(x_ideal)
	x_ideal_sorted = x_ideal[sort_idx]

	#Here we will store the results for each ideal (the deviation)
	M = {}
	
	#For that we need to loop through each ideal
	for name in ideal_names:
		y_ideal = df_ideal[name].values[sort_idx]

		#Interpolation of ideal and training X-Values  
		#For better understanding:
		#Estimate what the ideal function’s Y-values would be
		#at the same X positions as the training data.
		# = compare them at the same X positions
		y_at_train = np.interp(x_train, x_ideal_sorted, y_ideal, left=np.nan, right=np.nan)
		

		#The diffrences between the ideal function and the training data
		abs_res = []
		#loop through each training Y-Column
		for tcol in train_value_cols:

			#extract the training Y-values for this column
			y_train = df_train[tcol].values

			#Thats a "Security-Check" to only compare numeric data points
			mask = (~np.isnan(y_at_train)) & (~np.isnan(y_train))

			if mask.any():
				#Here we compute the absolute differences
				res = np.abs(y_train[mask] - y_at_train[mask])
				#print (res) = test

				#Store them in abs_res
				abs_res.append(res)

		if len(abs_res) == 0:
			#No data there = NaN
			M[name] = np.nan
		else:
			# Find the maximum deviation and store it in M
			M[name] = float(np.max(np.concatenate(abs_res)))


	return M


# The final function that matches the test data to the ideal functions and writes Table3
# Load test data, compare EACH test point to EACH ideal function, find which ideal fits best
# Check the acceptance crtierion, write results to Table3
def match_test_to_table3(ideal_names, db_path='database.db', table_ideal='Table2', test_csv='Datasets/test.csv', out_table='Table3', multiplier=math.sqrt(2)):
	
	#Again connect to database
	engine = create_engine(f'sqlite:///{db_path}')
	
	
	# Read ideal table and test data
	df_ideal = pd.read_sql(f'SELECT * FROM {table_ideal}', con=engine)
	df_test = pd.read_csv(test_csv)


	# normalize test columns, that means that we rename them to X and Y (like in the assignment)
	# and convert them to numeric values
	if 'x' in df_test.columns:
		df_test = df_test.rename(columns={'x': 'X', 'y': 'Y'})
	else:
		df_test.columns = ['X', 'Y']
	df_test['X'] = pd.to_numeric(df_test['X'], errors='coerce') #df_test['X'] → numeric X values
	df_test['Y'] = pd.to_numeric(df_test['Y'], errors='coerce') #df_test['Y'] → numeric Y values

	# Just like before we sort the x-Values of ideal for interpolation
	x_ideal = df_ideal.iloc[:, 0].values
	sort_idx = np.argsort(x_ideal)
	x_ideal_sorted = x_ideal[sort_idx]

	# Compute the maximum allowed deviation (with the function defined before)
	M = compute_deviation_for_ideals(db_path=db_path, table_train='Table1', table_ideal=table_ideal, ideal_names=ideal_names)

	# The following part is the core calculation
	x_test = df_test['X'].values
	dev_cols = []
	for name in ideal_names:
		y_ideal = df_ideal[name].values[sort_idx]
		y_pred = np.interp(x_test, x_ideal_sorted, y_ideal, left=np.nan, right=np.nan) # interpolate the ideal Y values at each test X value
		dev = np.abs(df_test['Y'].values - y_pred) #Compute the absolute deviation from the actual test Y value
		#Create new columns
		colname = f'Dev_{name}'
		df_test[colname] = dev
		dev_cols.append(colname) #Store those deviations in new columns

	# choose best and apply acceptance
	chosen = []
	delta = []
	for i, row in df_test.iterrows(): #loop each row in the test data
		devs = row[dev_cols].values	#extract all deviation values from the row for each ideal
		mask = ~np.isnan(devs) #again a mask and check to see if there are any valid values 
		if not mask.any():
			chosen.append(None) #nothing fits
			delta.append(np.nan) #no deviation
			continue #skip to next row
		true_idxs = np.where(mask)[0] #get the INDEZES of valid deviations
		best_rel_idx = int(np.argmin(devs[mask])) #Find smallest deviation (= our best fit)
		chosen_idx = true_idxs[best_rel_idx] #translate to original index (only needed if some were NaN)
		best_name = ideal_names[chosen_idx] #Find the name of the ideal function corresponding to that smallest deviation
		best_dev = float(devs[chosen_idx])#Get the actual deviation value (delta Y)
		deviation = M.get(best_name, np.nan) #Here we are getting the max. allowed deviation for that ideal function as the acceptance criterion
		if np.isnan(deviation): #we skip if there is no valid deviation
			chosen.append(None)
			delta.append(np.nan)
		else:
			threshold = multiplier * deviation #compute max. allowed deviation for acceptance
			if best_dev <= threshold: #check if the actual deviation is smaller than the allowed one
				chosen.append(best_name) #store the name of the ideal function
				delta.append(best_dev) #store the actual deviation value
			else:
				chosen.append(None) #no ideal function accepted
				delta.append(np.nan) #no deviation

	#Create DataFrame with the output columns (Table3)
	df_out = pd.DataFrame({'X': df_test['X'], 'Y': df_test['Y'], 'DeltaY': delta, 'IdealName': chosen})

	# write that to the database
	df_out.to_sql(out_table, con=engine, if_exists='replace', index=False)

	# print summary
	total = len(df_out) #count total rows (test points)
	assigned = df_out['IdealName'].notnull().sum() #and count how many where assigned to an ideal function
	unassigned = total - assigned #unassigned = total - assigned

	#Print the summary with context
	print(f'Wrote {len(df_out)} rows to {out_table} (assigned: {assigned}, unassigned: {unassigned})') 
	print('\nPer-ideal assignment counts:')
	print(df_out['IdealName'].value_counts(dropna=True))


if __name__ == '__main__': #this is the standard entry point of the program
	main()
