# import pandas as pd
# import lightningchart as lc
# import numpy as np

# # Read the license key from a file
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load data from the CSV file
# file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
# df = pd.read_csv(file_path)

# # Extract the required columns
# latitudes = df['latitude']
# longitudes = df['longitude']
# magnitudes = df['mag']

# # Normalize latitude and longitude for plotting
# norm_lat = (latitudes - latitudes.min()) / (latitudes.max() - latitudes.min())
# norm_long = (longitudes - longitudes.min()) / (longitudes.max() - longitudes.min())

# # Create a 3D chart
# chart = lc.Chart3D(
#     theme=lc.Themes.White,
#     title='Earthquake Magnitudes by Location'
# )

# # Define grid size based on the number of points
# grid_size = 100
# surface_data = np.full((grid_size, grid_size), np.nan)

# # Fill the grid with actual magnitudes
# for i in range(len(norm_lat)):
#     x_index = int(norm_long.iloc[i] * (grid_size - 1))
#     y_index = int(norm_lat.iloc[i] * (grid_size - 1))
#     surface_data[y_index, x_index] = magnitudes.iloc[i]

# # Handle NaN values by interpolating
# surface_data = np.nan_to_num(surface_data, nan=np.nanmean(surface_data))

# # Add a surface grid series to the chart
# series = chart.add_surface_grid_series(columns=grid_size, rows=grid_size)

# # Set the surface data
# series.invalidate_height_map(surface_data.tolist())

# # Set start and end coordinates
# series.set_start(x=longitudes.min(), z=latitudes.min())
# series.set_end(x=longitudes.max(), z=latitudes.max())

# # Set step size
# series.set_step(
#     x=(longitudes.max() - longitudes.min()) / grid_size,
#     z=(latitudes.max() - latitudes.min()) / grid_size
# )

# # Set color palette for the series
# series.set_palette_colors(
#     steps=[
#         {'value': -1, 'color': lc.Color(255, 0, 0)},  # Red for lower magnitudes
#         {'value': 3, 'color': lc.Color(255, 255, 0)},  # Yellow for mid magnitudes
#         {'value': 6, 'color': lc.Color(0, 128, 255)},  # Blue for higher magnitudes
#     ],
#     look_up_property='value',
#     percentage_values=False
# )

# # Invalidate intensity values
# series.invalidate_intensity_values(surface_data.tolist())

# # Set the axes titles
# chart.get_default_x_axis().set_title('Longitude')
# chart.get_default_y_axis().set_title('Latitude')
# chart.get_default_z_axis().set_title('Magnitude')

# # Set the Z-axis range
# chart.get_default_z_axis().set_interval(-1, 6)

# # Open the chart in a viewer
# chart.open()




import pandas as pd
import lightningchart as lc
import numpy as np
from scipy.interpolate import griddata

# Read the license key from a file
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load data from the CSV file
file_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project5/usgs_main.csv'
data = pd.read_csv(file_path)

# Extract latitude, longitude, and magnitude values
latitudes = data['latitude'].values
longitudes = data['longitude'].values
magnitudes = data['mag'].values

# Create grid data for the surface plot
grid_lat, grid_lon = np.meshgrid(
    np.linspace(latitudes.min(), latitudes.max(), 100),
    np.linspace(longitudes.min(), longitudes.max(), 100)
)

# Perform interpolation
grid_mag = griddata(
    (latitudes, longitudes), magnitudes,
    (grid_lat, grid_lon),
    method='linear'
)

# Fill NaN values with the mean of the magnitudes
nan_mask = np.isnan(grid_mag)
grid_mag[nan_mask] = np.nanmean(magnitudes)

# Initialize a 3D chart
chart = lc.Chart3D(
    theme=lc.Themes.White,
    title='3D Surface of Earthquake Magnitudes'
)

# Create a SurfaceGridSeries
surface_series = chart.add_surface_grid_series(
    columns=grid_mag.shape[1],
    rows=grid_mag.shape[0]
)

# Set start and end coordinates
surface_series.set_start(x=longitudes.min(), z=latitudes.min())
surface_series.set_end(x=longitudes.max(), z=latitudes.max())

# Set step size
surface_series.set_step(
    x=(longitudes.max() - longitudes.min()) / grid_mag.shape[1],
    z=(latitudes.max() - latitudes.min()) / grid_mag.shape[0]
)

# Invalidate height map
surface_series.invalidate_height_map(grid_mag.tolist())

# Define custom palette
surface_series.set_palette_colors(
    steps=[
        {"value": np.nanmin(grid_mag), "color": lc.Color(0, 0, 255)},       # Blue for lower magnitudes
        {"value": np.nanpercentile(grid_mag, 25), "color": lc.Color(0, 255, 255)},     # Cyan for lower mid magnitudes
        {"value": np.nanmedian(grid_mag), "color": lc.Color(0, 255, 0)},    # Green for median magnitudes
        {"value": np.nanpercentile(grid_mag, 75), "color": lc.Color(255, 255, 0)},     # Yellow for upper mid magnitudes
        {"value": np.nanmax(grid_mag), "color": lc.Color(255, 0, 0)}        # Red for higher magnitudes
    ],
    look_up_property='value',
    percentage_values=False
)

# Invalidate intensity values (for color mapping)
surface_series.invalidate_intensity_values(grid_mag.tolist())


# Set axis titles
chart.get_default_x_axis().set_title('Longitude')
chart.get_default_y_axis().set_title('Latitude')
chart.get_default_z_axis().set_title('Magnitude')

chart.add_legend(data=surface_series)
# Open the chart
chart.open()
