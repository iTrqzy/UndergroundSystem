import matplotlib.pyplot as plt

# The empirical times in minutes
empirical_times_dijkstra = [7.8564, 10.23268, 13.01709, 16.26894, 20.04461, 24.34297, 29.22217, 34.70576, 45.28391]
stations_dijkstra = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 2000]

# Theoretical O(n^3) times for comparison
theoretical_times_dijkstra = [(n ** 3) / 10 ** 7 for n in stations_dijkstra]

fig, ax1 = plt.subplots()

# Plot the empirical times on the first y-axis
ax1.plot(stations_dijkstra, empirical_times_dijkstra, marker='o', linestyle='-', color='b', label='Empirical Time')
ax1.set_xlabel('Number of Stations (n)')
ax1.set_ylabel('Empirical Execution Time Based On Stops (minutes)', color='b')
ax1.set_ylim(10, 90)
ax1.tick_params(axis='y', labelcolor='b')

# Create a secondary y-axis for the theoretical times
ax2 = ax1.twinx()
ax2.plot(stations_dijkstra, theoretical_times_dijkstra, linestyle='--', color='r', label="Theoretical O(n^3)")
ax2.set_ylabel('Empirical Time (Stops)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add a title and grid
plt.title('Empirical vs Theoretical Time Complexity')
plt.grid(True)

# Show the plot
fig.tight_layout()  # Adjust layout to prevent overlap
plt.show()
