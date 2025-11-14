"""Run the pipeline using the OO wrapping and classes in ooprojet

This script demonstrates how to instantiate the DBClient, DataLoader,
IdealSelector, Matcher and Visualizer objects like in Java and make a pipeline
without modifying the original procedural files

It intentionally delegates to the existing functions (no logic changed).

If we then compare main.py and this OO-Approach, we can see how the OO approach
organizes the code into classes and methods, an making it more easily reusable and
understandable.
"""
from ooproject import (
    DBClient, DataLoader, IdealSelector, Matcher, Visualizer,
    PipelineError, DataLoadError, SelectionError, MatchingError, ValidationError
)


def main():
    try:
        db = DBClient('database.db')#we create a DBClient object to handle the database connection
        loader = DataLoader(db_client=db)#we create a DataLoader object to load data from the database
        loader.load_from_db()  # loads Table1 and Table2 from DB

        selector = IdealSelector(loader)#we create an IdealSelector object to select the top ideal functions
        top4 = selector.select_top_k(4)#we select the top 4 ideal functions
        print('Top4 (name, sse):')
        for name, sse in top4:
            print(' ', name, sse)

        top4_names = [name for name, _ in top4] #extract only the names

        matcher = Matcher(loader, top4_names)#we create a Matcher object to match test data to the top ideal functions
        # This will call the existing match_test_to_table3 and write Table3 to DB
        matcher.match_and_write_table3()#we perform the matching and write the results to Table3

        viz = Visualizer(loader)#we create a Visualizer object to visualize the results
        # This will call the existing visualize.py main() to produce confirm_top4.html
        viz.confirm_top4()#we visualize the results

        print('\nOO pipeline run complete. Outputs: Table3 (DB) and confirm_top4.html')

        """We basically have our exception handling in the classes themselves
          there we raise the exceptions and in this "main" we catch them an print,
          so the control of the Exceptions then jumps back here"""
        
    except DataLoadError as e:
        print(f"\n Data loading failed: {e}")
        print("   Check that database.db exists and contains Table1 and Table2")
        
    except ValidationError as e:
        print(f"\n Data validation failed: {e}")
        print("   Check that your data tables are not empty and have correct columns")
        
    except SelectionError as e:
        print(f"\n Ideal selection failed: {e}")
        print("   Check training and ideal data quality")
        
    except MatchingError as e:
        print(f"\n Test matching failed: {e}")
        print("   Check test.csv exists and is properly formatted")
        
    except PipelineError as e:
        print(f"\n Pipeline error: {e}")
        
    except ValueError as e:
        print(f"\n Invalid parameter: {e}")
        
    except Exception as e:
        print(f"\n Unexpected error: {e}")


if __name__ == '__main__':
    main()
