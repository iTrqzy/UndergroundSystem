import pandas as pd
import matplotlib.pyplot as plt

file = 'London Underground data.xlsx'  # File path for the Excel file
underground_data = pd.read_excel(file, sheet_name='Sheet1')  # Load data from the first sheet

underground_data.columns = ["Line", "Station_A", "Station_B", "Duration"]  # Rename columns for easier use

# Convert 'Duration' to numeric and handle non-numeric values (convert them to NaN)
underground_data['Duration'] = pd.to_numeric(underground_data['Duration'], errors='coerce')

# Drop rows where 'Duration' is missing or invalid
underground_data.dropna(subset=['Duration'], inplace=True)

# Create a range of bins based on the min and max duration
duration_bins = range(int(underground_data['Duration'].min()), int(underground_data['Duration'].max()) + 1)

plt.figure(figsize=(10, 6))  # Set the plot size
plt.hist(underground_data['Duration'], bins=duration_bins, color='green', edgecolor='black', align='left')  # Create the histogram

# Add labels and title
plt.title('London Underground Journey Duration Distribution')
plt.xlabel('Journey Duration (Minutes)')
plt.ylabel('Frequency')

plt.show()  # Display the plot
