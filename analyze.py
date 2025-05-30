import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_df(file, columns=None):
    """
    Reads a CSV file and returns a pandas DataFrame.
    
    Parameters:
        filename (str): Path to the CSV file.
        columns (list, optional): List of column names to read. If None, reads all columns.
    
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    if columns:
        return df[columns]
    else:
        return df

course = "coursename"

# Files

# Course name
activity_file = "filename" # File from New Analytics
content_file = "filename" # File from custom code

# Dataframes
activity_frame = get_df(activity_file, ["content_type", "content_name", "times_viewed"])
content_frame = get_df(content_file)

# Aggregate views
aggregated_views = activity_frame.groupby("content_name", as_index=False)["times_viewed"].sum()

# Use the line below to only include published content
content_frame = content_frame[content_frame["published"] == "Published"]


# Merge the frames
result_frame = pd.merge(
    content_frame[['position', 'title']],
    aggregated_views,
    left_on = 'title',
    right_on = 'content_name',
    how = 'inner'
).sort_values(by='position').reset_index(drop=False)

print(result_frame.head())

if result_frame.shape[0] == 0:
    print("No views found for module content.")
    exit(0)

# Extract range and values
x = result_frame['index']
y = result_frame['times_viewed']

# Plot the results
result_frame.plot.scatter(x = 'index', y = 'times_viewed', label = "Views")

plt.xlabel('Position on modules page')
plt.ylabel('Number of Views')
plt.title(f'Views per Module Entry for {course}')


# Create a trend line
slope, intercept = np.polyfit(x,y,1)
trend_line = slope * x + intercept

# Compute R-squared
y_mean = np.mean(y)
ss_total = np.sum((y - y_mean) ** 2)
ss_residual = np.sum((y - trend_line) ** 2)
r_squared = 1 - (ss_residual / ss_total)


# Plot trendline
plt.plot(x, trend_line, color='red', label="Trend line")

# Annotate with slope and R²
# Determine coordinates for placing text box
x_pos = x.max() * 0.8  # 80% of the x-range
y_pos = y.max() * 1.05  # Slightly above the max y-value
equation_text = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r_squared:.3f}"
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
plt.legend()

plt.show()

