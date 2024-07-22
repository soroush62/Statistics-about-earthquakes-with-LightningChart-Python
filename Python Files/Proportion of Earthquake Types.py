import pandas as pd
import lightningchart as lc
import seaborn as sns

lc.set_license('my-license-key')

file_path = 'usgs_main.csv'
data = pd.read_csv(file_path)

# Calculate the proportions of each earthquake type
mag_type_counts = data['type'].value_counts()

# Prepare the data for LightningChart
slices_data = [{'name': mag_type, 'value': count} for mag_type, count in mag_type_counts.items()]

# Create the pie chart
chart = lc.PieChart(
    labels_inside_slices=False,
    title='Proportion of Earthquake Types',
    theme=lc.Themes.White
)

# Add slices to the pie chart
chart.add_slices(slices_data)

# Set the inner radius for a donut chart effect (optional, can be set to 0 for a standard pie chart)
chart.set_inner_radius(50)

# Open the chart in the browser
chart.open()



