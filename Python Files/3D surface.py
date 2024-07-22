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
chart.get_default_y_axis().set_title('Magnitude')
chart.get_default_z_axis().set_title('Latitude')

chart.add_legend(data=surface_series)
# Open the chart
chart.open()




# Convert 'time' column to datetime
data['time'] = pd.to_datetime(data['time'])

# Handle missing values (example: filling NaN in 'mag' column with the mean)
data['mag'].fillna(data['mag'].mean(), inplace=True)

# Resample data by month for time-series analysis
monthly_data = data.set_index('time').resample('M').size()

# Aggregate categorical data for proportions
type_counts = data['type'].value_counts()

# Prepare data for heatmap and 3D surface plot
latitudes = data['latitude'].values
longitudes = data['longitude'].values
magnitudes = data['mag'].values

# Create grid data for the surface plot
grid_lat, grid_lon = np.meshgrid(
    np.linspace(latitudes.min(), latitudes.max(), 100),
    np.linspace(longitudes.min(), longitudes.max(), 100))

# Perform interpolation
grid_mag = griddata((latitudes, longitudes), magnitudes,(grid_lat, grid_lon), method='linear')

# Fill NaN values with the mean of the magnitudes
nan_mask = np.isnan(grid_mag)
grid_mag[nan_mask] = np.nanmean(magnitudes)






# import pandas as pd
# import lightningchart as lc
# import numpy as np
# from scipy.interpolate import griddata

# lc.set_license('my-license-key')
# file_path = 'usgs_main.csv'
# data = pd.read_csv(file_path)

# # Extract data and create grid
# latitudes = data['latitude'].values
# longitudes = data['longitude'].values
# magnitudes = data['mag'].values
# grid_lat, grid_lon = np.meshgrid(np.linspace(latitudes.min(), latitudes.max(), 100), np.linspace(longitudes.min(), longitudes.max(), 100))
# grid_mag = griddata((latitudes, longitudes), magnitudes, (grid_lat, grid_lon), method='linear')

# # Fill NaN values
# nan_mask = np.isnan(grid_mag)
# grid_mag[nan_mask] = np.nanmean(magnitudes)

# # Create and customize 3D chart
# chart = lc.Chart3D(theme=lc.Themes.White, title='3D Surface of Earthquake Magnitudes')
# surface_series = chart.add_surface_grid_series(columns=grid_mag.shape[1], rows=grid_mag.shape[0])
# surface_series.set_start(x=longitudes.min(), z=latitudes.min())
# surface_series.set_end(x=longitudes.max(), z=latitudes.max())
# surface_series.set_step(x=(longitudes.max() - longitudes.min()) / grid_mag.shape[1], z=(latitudes.max() - latitudes.min()) / grid_mag.shape[0])
# surface_series.invalidate_height_map(grid_mag.tolist())
# surface_series.set_palette_colors(steps=[{"value": np.nanmin(grid_mag), "color": lc.Color(0, 0, 255)},
#              {"value": np.nanpercentile(grid_mag, 25), "color": lc.Color(0, 255, 255)}, 
#     {"value": np.nanmedian(grid_mag), "color": lc.Color(0, 255, 0)}, {"value": np.nanpercentile(grid_mag, 75),
#  "color": lc.Color(255, 255, 0)}, {"value": np.nanmax(grid_mag), "color": lc.Color(255, 0, 0)}], look_up_property='value', percentage_values=False)
# surface_series.invalidate_intensity_values(grid_mag.tolist())

# chart.get_default_x_axis().set_title('Longitude')
# chart.get_default_y_axis().set_title('Magnitude')
# chart.get_default_z_axis().set_title('Latitude')
# chart.add_legend(data=surface_series)
# chart.open()

