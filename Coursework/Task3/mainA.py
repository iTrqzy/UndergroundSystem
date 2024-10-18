import pandas as pd
import matplotlib.pyplot as plt



file_path = 'London Underground data.xlsx' # Store the file path


data = pd.read_excel(file_path, sheet_name=None) # Store the contents in the Excel file in data


underground_data = data['Sheet1'] # Access the first sheet of the file


removed_nan_data = underground_data.dropna() # Removes any unnecessary data from the file
removed_nan_data.columns = ["Line","Station1","Station2","Journey_Duration"] # Add names to each column


plt.figure(figsize=(10, 6))
plt.hist(removed_nan_data["Journey_Duration"], bins=20, color='blue', edgecolor='black') # Retrieves the duration
                                                                                         # And plots it on the hist

# Add titles and labels
plt.title('Histogram of Journey Durations in Minutes')
plt.xlabel('Journey Duration (minutes)')
plt.ylabel('Frequency')

# Show the plot
plt.show()

