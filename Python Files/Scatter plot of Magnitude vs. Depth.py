import lightningchart as lc
import pandas as pd
import numpy as np
import builtins

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
data = pd.read_csv(file_path)

x_values = data['depth'].values.tolist()
y_values = data['mag'].values.tolist()
min_value=int(builtins.min(y_values))
max_value=int(builtins.max(y_values))
lookup_values = y_values

chart = lc.ScatterChart(
    theme=lc.Themes.White,
    title='Magnitude vs. Depth',
    point_size=10,
    point_shape='circle',
    xlabel='Depth (km)',
    ylabel='Magnitude',
    individual_colors=True,
    individual_lookup_values=True
)
series = chart.series.append_samples(
    x_values=x_values,
    y_values=y_values,
    lookup_values=lookup_values
)
series.set_palette_colors(
    steps=[
        {'value': min_value, 'color': lc.Color(0, 64, 128)},
        {'value': max_value, 'color': lc.Color(255, 128, 64)},
    ],
    look_up_property='value',
    percentage_values=False
)
legend = chart.add_legend(data=chart).set_title('Magnitude')
chart.open()
