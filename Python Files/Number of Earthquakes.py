import pandas as pd
import lightningchart as lc
from datetime import datetime

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
data = pd.read_csv(file_path)

# Convert 'time' column to datetime
data['time'] = pd.to_datetime(data['time'])

# Resample data by month and count the number of earthquakes
monthly_data = data.set_index('time').resample('M').size()

# Prepare the data for LightningChart
x_values = [datetime.timestamp(d) * 1000 for d in monthly_data.index]  # Convert to timestamp in milliseconds
y_values = monthly_data.values.tolist()

# Create the chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='Number of Earthquakes Over Time'
)

# Add a line series
line_series = chart.add_line_series()
line_series.set_name('Earthquakes')
line_series.set_line_color(lc.Color(0, 0, 255))
line_series.set_line_thickness(2)

# Append data to the series
line_series.append_samples(
    x_values=x_values,
    y_values=y_values
)

# Customize x-axis
x_axis = chart.get_default_x_axis()
x_axis.set_title('Time')
x_axis.set_tick_strategy('DateTime', utc=True)

# Customize y-axis
y_axis = chart.get_default_y_axis()
y_axis.set_title('Number of Earthquakes')

chart.open()
