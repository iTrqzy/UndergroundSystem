import pandas as pd
import matplotlib.pyplot as plt

# Define the file path for the Excel file
file_path = 'London Underground data.xlsx'

# Load the data from the Excel file, reading all sheets into a dictionary
data = pd.read_excel(file_path, sheet_name=None)

# Access the first sheet of the Excel file
underground_data = data['Sheet1']

# Clean the data by removing any rows with missing values
clean_data = underground_data.dropna()

# Rename the columns for clarity
clean_data.columns = ["Line", "Station1", "Station2", "Journey_Duration"]

# Create a histogram of journey durations
plt.figure(figsize=(10, 6))
plt.hist(clean_data["Journey_Duration"], bins=20, color='blue', edgecolor='black')

# Add title and labels
plt.title('Histogram of Journey Durations in Minutes')
plt.xlabel('Journey Duration (minutes)')
plt.ylabel('Frequency')

# Show the plot
plt.show()
