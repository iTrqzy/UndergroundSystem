import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
file_path = 'London Underground data.xlsx'
london_underground_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Rename columns for clarity and remove any rows with missing journey durations
london_underground_data.columns = ["Line", "Station1", "Station2", "Journey_Duration"]
clean_data = london_underground_data.dropna(subset=['Journey_Duration'])

# Count the number of stops between each station pair
total_stops = clean_data.groupby(['Station1', 'Station2']).size()

# Plot a histogram to visualize the number of stops
plt.figure(figsize=(10, 6))
plt.hist(total_stops, bins=20, color='green', edgecolor='black')
plt.title('Histogram of Number of Stops Between Stations')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')

# Show the plot
plt.show()
