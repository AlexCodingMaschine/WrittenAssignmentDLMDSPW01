from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

DB = 'database.db'
engine = create_engine(f'sqlite:///{DB}')


def read_tables():
    df_train = pd.read_sql('SELECT * FROM Table1', con=engine)
    df_ideal = pd.read_sql('SELECT * FROM Table2', con=engine)
    try:
        df_chosen = pd.read_sql('SELECT * FROM ChosenIdeals', con=engine)
    except Exception:
        df_chosen = None
    try:
        df_test = pd.read_sql('SELECT * FROM Table3', con=engine)
    except Exception:
        df_test = None
    return df_train, df_ideal, df_chosen, df_test


def compute_top4_names(df_train, df_ideal):
    # Compute total SSE per ideal function
    x_train = df_train.iloc[:, 0].values
    train_cols = list(df_train.columns[1:])
    x_ideal = df_ideal.iloc[:, 0].values
    idx = np.argsort(x_ideal)
    x_ideal_sorted = x_ideal[idx]
    sse = []
    for col in df_ideal.columns[1:]:
        y = df_ideal[col].values[idx]
        y_at_train = np.interp(x_train, x_ideal_sorted, y, left=np.nan, right=np.nan)
        total = 0.0
        any_valid = False
        for t in train_cols:
            yt = df_train[t].values
            mask = (~np.isnan(y_at_train)) & (~np.isnan(yt))
            if mask.any():
                r = yt[mask] - y_at_train[mask]
                total += float((r**2).sum())
                any_valid = True
        if not any_valid:
            total = float('inf')
        sse.append((col, total))
    sse.sort(key=lambda x: x[1])
    return [name for name, _ in sse[:4]]


def make_confirm_plot(df_train, df_ideal, chosen_names, df_test=None):
    output_file('confirm_top4.html', title='Confirm top-4 vs training')
    p = figure(title='Training series + Top-4 Ideal Functions + Test Points',
               x_axis_label='X', y_axis_label='Y', height=500, width=800,
               background_fill_color="#fafafa")

    # === Training series ===
    x_train = df_train.iloc[:, 0].values
    for col in df_train.columns[1:6]:  # show only first few to avoid clutter
        p.line(x_train, df_train[col].values, line_alpha=0.5,
               line_width=1.5, color='gray', legend_label='Training series')

    # === Overlay chosen ideals ===
    x_ideal = df_ideal.iloc[:, 0].values
    idx = np.argsort(x_ideal)
    x_ideal_sorted = x_ideal[idx]
    colors = ['orange', 'green', 'blue', 'red']
    for i, name in enumerate(chosen_names[:4]):
        if name in df_ideal.columns:
            y = df_ideal[name].values[idx]
            p.line(x_ideal_sorted, y, line_color=colors[i],
                   line_width=2.5, legend_label=f'Ideal: {name}')

    # === Overlay test points (if available) ===
    if df_test is not None and not df_test.empty:
        color_map = {
            chosen_names[0]: 'orange',
            chosen_names[1]: 'green',
            chosen_names[2]: 'blue',
            chosen_names[3]: 'red'
        }
        for ideal in chosen_names:
            df_subset = df_test[df_test['IdealName'] == ideal]
            if not df_subset.empty:
                p.circle(df_subset['X'], df_subset['Y'],
                         size=6, color=color_map.get(ideal, 'black'),
                         alpha=0.8, legend_label=f'Test -> {ideal}')

        # Unassigned points (None)
        df_none = df_test[df_test['IdealName'].isna()]
        if not df_none.empty:
            p.cross(df_none['X'], df_none['Y'], size=6, color='black',
                    alpha=0.6, legend_label='Unassigned test points')

    p.legend.click_policy = 'hide'
    p.legend.label_text_font_size = "10pt"
    p.legend.location = "top_left"

    show(p)


def main():
    df_train, df_ideal, df_chosen, df_test = read_tables()

    # Prefer ChosenIdeals if present
    chosen_names = None
    if df_chosen is not None and not df_chosen.empty:
        if 'Name' in df_chosen.columns:
            chosen_names = df_chosen['Name'].astype(str).tolist()
        elif 'IdealName' in df_chosen.columns:
            chosen_names = df_chosen['IdealName'].astype(str).tolist()
        else:
            chosen_names = df_chosen.iloc[:, 0].astype(str).tolist()

    if chosen_names is None or len(chosen_names) < 4:
        chosen_names = compute_top4_names(df_train, df_ideal)

    print('Confirmed chosen/top-4 for plotting:', chosen_names[:4])
    make_confirm_plot(df_train, df_ideal, chosen_names, df_test)


if __name__ == '__main__':
    main()
