import pandas as pd
import lightningchart as lc
import seaborn as sns

# Set your LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
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




import pandas as pd
import lightningchart as lc

lc.set_license('my-license-key')

file_path = 'usgs_main.csv'
data = pd.read_csv(file_path)

# Calculate proportions
mag_type_counts = data['type'].value_counts()
slices_data = [{'name': mag_type, 'value': count} for mag_type, count in mag_type_counts.items()]

# Create and customize pie chart
chart = lc.PieChart(labels_inside_slices=False, title='Proportion of Earthquake Types', theme=lc.Themes.White)
chart.add_slices(slices_data)
chart.set_inner_radius(50)  # For donut chart effect
chart.open()

