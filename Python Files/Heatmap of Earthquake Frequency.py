# import lightningchart as lc
# import numpy as np
# import pandas as pd
# from scipy.interpolate import griddata

# # Read the license key from a file
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the seismic data
# file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
# data = pd.read_csv(file_path)

# # Debugging: Print the first few rows of the dataset
# print("First few rows of the dataset:")
# print(data.head())

# # Check for NaN values and remove rows with NaNs
# data = data.dropna(subset=['latitude', 'longitude', 'depth'])

# grid_size = 500  # Reduced grid size for faster processing
# x_values = data['latitude'].astype(float).tolist()
# y_values = data['longitude'].astype(float).tolist()

# # Debugging: Print the range of latitude and longitude values
# print(f"Latitude range: {min(x_values)} to {max(x_values)}")
# print(f"Longitude range: {min(y_values)} to {max(y_values)}")

# # Create a grid of points
# grid_x, grid_y = np.mgrid[min(x_values):max(x_values):complex(grid_size), min(y_values):max(y_values):complex(grid_size)]

# # Interpolate Z values on the grid using linear interpolation
# grid_z = griddata((data['latitude'], data['longitude']), data['depth'], (grid_x, grid_y), method='linear')

# # Check for NaN values in the interpolated grid and fill them
# if np.isnan(grid_z).any():
#     grid_z = np.where(np.isnan(grid_z), griddata((data['latitude'], data['longitude']), data['depth'], (grid_x, grid_y), method='nearest'), grid_z)

# # Debugging: Print the range of depth values before converting to float
# print(f"Depth range before conversion: {np.min(grid_z)} to {np.max(grid_z)}")

# # Convert numpy int to Python int
# grid_z = grid_z.astype(float)

# # Debugging: Print the range of depth values after converting to float
# print(f"Depth range after conversion: {np.min(grid_z)} to {np.max(grid_z)}")

# # Initialize a chart
# chart = lc.ChartXY(theme=lc.Themes.Dark, title='Heatmap of Earthquake Frequency')

# # Create HeatmapGridSeries
# heatmap = chart.add_heatmap_grid_series(
#     columns=grid_size,
#     rows=grid_size,
# )

# # Set start and end coordinates
# heatmap.set_start(x=min(x_values), y=min(y_values))
# heatmap.set_end(x=max(x_values), y=max(y_values))

# # Set step size
# heatmap.set_step(x=(max(x_values) - min(x_values)) / grid_size, y=(max(y_values) - min(y_values)) / grid_size)

# # Enable intensity interpolation
# heatmap.set_intensity_interpolation(True)

# # Invalidate intensity values
# heatmap.invalidate_intensity_values(grid_z)

# # Hide wireframe
# heatmap.hide_wireframe()

# # Define custom palette to match the second image
# custom_palette = [
#     {"value": np.min(grid_z), "color": lc.Color(0, 0, 255)},       # Blue
#     {"value": np.percentile(grid_z, 25), "color": lc.Color(0, 128, 255)},  # Light Blue
#     {"value": np.percentile(grid_z, 50), "color": lc.Color(255, 255, 255)},    # White
#     {"value": np.percentile(grid_z, 75), "color": lc.Color(255, 255, 0)},      # Yellow
#     {"value": np.max(grid_z), "color": lc.Color(255, 0, 0)},        # Red
# ]

# # Debugging: Print the custom palette steps
# print("Custom palette steps:")
# for step in custom_palette:
#     print(step)

# heatmap.set_palette_colors(
#     steps=custom_palette,
#     look_up_property='value',
#     interpolate=True
# )

# # Set axis titles
# chart.get_default_x_axis().set_title('Longitude')
# chart.get_default_y_axis().set_title('Latitude')

# # Set axis limits based on the actual data ranges
# chart.get_default_x_axis().set_interval(min(x_values), max(x_values))
# chart.get_default_y_axis().set_interval(min(y_values), max(y_values))

# # Display chart
# chart.open()









# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from scipy.interpolate import griddata

# # Read the license key from a file
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the seismic data
# file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
# data = pd.read_csv(file_path)

# # Binning latitude and longitude
# data['latitude_bin'] = pd.cut(data['latitude'], bins=30, labels=False)
# data['longitude_bin'] = pd.cut(data['longitude'], bins=30, labels=False)

# # Create a pivot table to count the number of earthquakes in each bin
# heatmap_data = data.pivot_table(index='latitude_bin', columns='longitude_bin', values='mag', aggfunc='count').fillna(0)

# # Convert the pivot table to a numpy array
# z_values = heatmap_data.values
# x_bins = heatmap_data.columns
# y_bins = heatmap_data.index

# # Create the grid for x and y values
# x_values = np.linspace(data['longitude'].min(), data['longitude'].max(), len(x_bins))
# y_values = np.linspace(data['latitude'].min(), data['latitude'].max(), len(y_bins))

# # Initialize a chart
# chart = lc.ChartXY(theme=lc.Themes.Dark, title='Heatmap of Earthquake Frequency')

# # Create HeatmapGridSeries
# heatmap = chart.add_heatmap_grid_series(
#     columns=len(x_bins),
#     rows=len(y_bins),
# )

# # Set start and end coordinates
# heatmap.set_start(x=x_values.min(), y=y_values.min())
# heatmap.set_end(x=x_values.max(), y=y_values.max())

# # Normalize the z-values for better visualization
# z_min, z_max = z_values.min(), z_values.max()
# z_normalized = (z_values - z_min) / (z_max - z_min)

# # Set the intensity values
# heatmap.invalidate_intensity_values(z_normalized.tolist())

# # Define custom palette
# custom_palette = [
#     {"value": 0, "color": lc.Color(0, 0, 0)},      # Black
#     {"value": 0.25, "color": lc.Color(50, 50, 255)},  # Blue
#     {"value": 0.5, "color": lc.Color(255, 255, 255)},  # White
#     {"value": 0.75, "color": lc.Color(255, 255, 0)},   # Yellow
#     {"value": 1.0, "color": lc.Color(255, 0, 0)},      # Red
# ]

# heatmap.set_palette_colors(
#     steps=custom_palette,
#     look_up_property='value',
#     interpolate=True
# )

# # Set axis titles
# chart.get_default_x_axis().set_title('Longitude')
# chart.get_default_y_axis().set_title('Latitude')

# # Set axis limits based on the actual data ranges
# chart.get_default_x_axis().set_interval(x_values.min(), x_values.max())
# chart.get_default_y_axis().set_interval(y_values.min(), y_values.max())

# # Display chart
# chart.open()







# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from scipy.interpolate import griddata

# # Read the license key from a file
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the seismic data
# file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
# data = pd.read_csv(file_path)

# # Extract relevant columns
# latitude = data['latitude'].astype(float).tolist()
# longitude = data['longitude'].astype(float).tolist()
# magnitude = data['mag'].astype(float).tolist()

# # Create a grid of points for the heatmap
# grid_size = 500  # Adjust grid size as needed
# grid_x, grid_y = np.meshgrid(
#     np.linspace(min(longitude), max(longitude), grid_size),
#     np.linspace(min(latitude), max(latitude), grid_size)
# )

# # Use griddata to interpolate depth values on the grid
# grid_z = griddata(
#     (longitude, latitude),
#     magnitude,
#     (grid_x, grid_y),
#     method='linear'
# )

# # Fill any remaining NaN values with nearest method
# grid_z = np.where(np.isnan(grid_z), griddata((longitude, latitude), magnitude, (grid_x, grid_y), method='nearest'), grid_z)

# # Initialize a chart
# chart = lc.ChartXY(theme=lc.Themes.Dark, title='Heatmap of Earthquake Frequency')

# # Create HeatmapGridSeries
# heatmap = chart.add_heatmap_grid_series(
#     columns=grid_size,
#     rows=grid_size,
# )

# # Set start and end coordinates
# heatmap.set_start(x=min(longitude), y=min(latitude))
# heatmap.set_end(x=max(longitude), y=max(latitude))

# # Set step size
# heatmap.set_step(
#     x=(max(longitude) - min(longitude)) / grid_size,
#     y=(max(latitude) - min(latitude)) / grid_size
# )

# # Enable intensity interpolation
# heatmap.set_intensity_interpolation(True)

# # Invalidate intensity values
# heatmap.invalidate_intensity_values(grid_z)

# # Hide wireframe
# heatmap.hide_wireframe()

# # Define custom palette
# custom_palette = [
#     {"value": np.nanmin(grid_z), "color": lc.Color(0, 0, 255)},       # Blue
#     {"value": np.nanpercentile(grid_z, 25), "color": lc.Color(0, 255, 255)},     # Cyan
#     {"value": np.nanmedian(grid_z), "color": lc.Color(0, 255, 0)},    # Green
#     {"value": np.nanpercentile(grid_z, 75), "color": lc.Color(255, 255, 0)},     # Yellow
#     {"value": np.nanmax(grid_z), "color": lc.Color(255, 0, 0)},        # Red
# ]

# heatmap.set_palette_colors(
#     steps=custom_palette,
#     look_up_property='value',
#     interpolate=True
# )

# # Set axis titles
# chart.get_default_x_axis().set_title('Longitude')
# chart.get_default_y_axis().set_title('Latitude')

# # Set axis limits based on the actual data ranges
# chart.get_default_x_axis().set_interval(min(longitude), max(longitude))
# chart.get_default_y_axis().set_interval(min(latitude), max(latitude))

# # Display chart
# chart.open()






import lightningchart as lc
import pandas as pd
import numpy as np
import builtins

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
data = pd.read_csv(file_path)

# Create a grid to interpolate the magnitude values
latitudes = np.linspace(data['latitude'].min(), data['latitude'].max(), 100)
longitudes = np.linspace(data['longitude'].min(), data['longitude'].max(), 100)
lat_grid, lon_grid = np.meshgrid(latitudes, longitudes)

# Interpolate magnitude values on the grid
mag_grid = np.zeros_like(lat_grid)
grid_z = []
# Simple nearest neighbor interpolation for this example
for i in range(lat_grid.shape[0]):
    for j in range(lon_grid.shape[1]):
        # Find the closest point in the dataset
        distances = np.sqrt((data['latitude'] - lat_grid[i, j])**2 + (data['longitude'] - lon_grid[i, j])**2)
        closest_index = distances.idxmin()
        mag_grid[i, j] = data.loc[closest_index, 'mag']
        grid_z.append(data.loc[closest_index, 'mag'])
print(min(grid_z))
print(max(grid_z))
# Flatten the grid for the heatmap
mag_grid_flat = mag_grid.flatten()

# Create the chart
chart = lc.ChartXY(
    title="Heatmap of Earthquake Magnitudes by Latitude and Longitude",
    theme=lc.Themes.White  # Use White theme
)

# Create the heatmap series
heatmap_series = chart.add_heatmap_grid_series(
    columns=len(longitudes),
    rows=len(latitudes),
    x_axis=chart.get_default_x_axis(),
    y_axis=chart.get_default_y_axis()
)

# Set the data for the heatmap
heatmap_series.invalidate_intensity_values(mag_grid)

# Set start and end coordinates
heatmap_series.set_start(x=data['longitude'].min(), y=data['latitude'].min())
heatmap_series.set_end(x=data['longitude'].max(), y=data['latitude'].max())

# Simplified custom palette
custom_palette = [
    {"value": np.nanmin(grid_z), "color": lc.Color(0, 0, 255)},       # Blue
    {"value": np.nanpercentile(grid_z, 25), "color": lc.Color(0, 255, 255)},     # Cyan
    {"value": np.nanmedian(grid_z), "color": lc.Color(0, 255, 0)},    # Green
    {"value": np.nanpercentile(grid_z, 75), "color": lc.Color(255, 255, 0)},     # Yellow
    {"value": np.nanmax(grid_z), "color": lc.Color(255, 0, 0)},        # Red
]

heatmap_series.set_palette_colors(
    steps=custom_palette,
    look_up_property='value',
    interpolate=True
)

# Set axis titles
chart.get_default_x_axis().set_title('Longitude')
chart.get_default_y_axis().set_title('Latitude')

# Set axis limits based on the actual data ranges
chart.get_default_x_axis().set_interval(data['longitude'].min(), data['longitude'].max())
chart.get_default_y_axis().set_interval(data['latitude'].min(), data['latitude'].max())
chart.add_legend(data=heatmap_series)

chart.open()
