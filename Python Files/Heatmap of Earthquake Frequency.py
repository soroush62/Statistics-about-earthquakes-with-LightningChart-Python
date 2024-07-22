import lightningchart as lc
import pandas as pd
import numpy as np
import builtins

lc.set_license('my-license-key')

file_path = 'usgs_main.csv'
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

# Flatten the grid for the heatmap
mag_grid_flat = mag_grid.flatten()

# Create the chart
chart = lc.ChartXY(
    title="Heatmap of Earthquake Magnitudes by Latitude and Longitude",
    theme=lc.Themes.White 
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
heatmap_series.set_intensity_interpolation(False)

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
