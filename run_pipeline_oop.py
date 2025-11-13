"""Run the pipeline using the OO wrappers in `ooproject`.

This script demonstrates how to instantiate the DBClient, DataLoader,
IdealSelector, Matcher and Visualizer objects and run the pipeline without
modifying the original procedural files.

It intentionally delegates to the existing functions (no logic changed).
"""
from ooproject import DBClient, DataLoader, IdealSelector, Matcher, Visualizer


def main():
    db = DBClient('database.db')
    loader = DataLoader(db_client=db)
    loader.load_from_db()  # loads Table1 and Table2 from DB

    selector = IdealSelector(loader)
    top4 = selector.select_top_k(4)
    print('Top4 (name, sse):')
    for name, sse in top4:
        print(' ', name, sse)

    top4_names = [name for name, _ in top4]

    matcher = Matcher(loader, top4_names)
    # This will call the existing match_test_to_table3 and write Table3 to DB
    matcher.match_and_write_table3()

    viz = Visualizer(loader)
    # This will call the existing visualize.py main() to produce confirm_top4.html
    viz.confirm_top4()

    print('\nOO pipeline run complete. Outputs: Table3 (DB) and confirm_top4.html')


if __name__ == '__main__':
    main()
