import pandas as pd
import matplotlib.pyplot as plt

# Setup the excel file ready for use
file_path = 'London Underground data.xlsx'
london_underground_data = pd.read_excel(file_path, sheet_name='Sheet1')

london_underground_data.columns = ["Line", "Station1", "Station2", "Journey_Duration"] # Add column names to make it easier

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(london_underground_data['Journey_Duration'], bins=20, color='green', edgecolor='black')
plt.title('Histogram of Journey Durations Based on Time')
plt.xlabel('Journey Duration (Minutes)')
plt.ylabel('Frequency')


# Display the plot
plt.show()
