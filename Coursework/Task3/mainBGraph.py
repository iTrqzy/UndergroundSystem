import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the London Underground data and add proper column names
file_path = 'London Underground data.xlsx'
london_underground_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Add column names: Line, Station1, Station2, Journey_Duration
london_underground_data.columns = ["Line", "Station1", "Station2", "Journey_Duration"]

# Step 2: Clean the data by removing rows with missing values in Station2 or Journey_Duration
cleaned_data = london_underground_data.dropna(subset=["Station2", "Journey_Duration"]).copy()

# Convert Journey_Duration to numeric (use .loc[] to avoid the warning)
cleaned_data.loc[:, 'Journey_Duration'] = pd.to_numeric(cleaned_data['Journey_Duration'], errors='coerce')

# Drop rows with invalid journey durations (e.g., NaN)
cleaned_data = cleaned_data.dropna(subset=["Journey_Duration"])

# Step 3: Plot the histogram of journey durations
plt.figure(figsize=(10, 6))
plt.hist(cleaned_data['Journey_Duration'], bins=20, color='blue', edgecolor='black')
plt.title('Histogram of Journey Durations Based on Time')
plt.xlabel('Journey Duration (Minutes)')
plt.ylabel('Frequency')
plt.grid(True)

# Display the plot
plt.show()
