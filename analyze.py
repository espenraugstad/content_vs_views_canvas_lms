import pandas as pd

def get_df(file, columns=None):
    """
    Reads a CSV file and returns a pandas DataFrame.
    
    Parameters:
        filename (str): Path to the CSV file.
        columns (list, optional): List of column names to read. If None, reads all columns.
    
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    if columns:
        return pd.read_csv(file, usecols=columns)
    else:
        return pd.read_csv(file)

# File names
# List of activities
activity_file = "activity 28.5.2025 (3).csv"
activity_frame = get_df(activity_file, ["Content type", "Content Name", "Times viewed"])
# List of content
content_file = "Content_IKT902-1 25V Introduksjon til kunstig intelligens-teknologi.csv"
content_frame = get_df(content_file)

# Aggregate views
aggregated_views = activity_frame.groupby("Content Name", as_index=False)["Times viewed"].sum()

# Merge the frames
result_frame = pd.merge(
    content_frame[['Position', 'Title']],
    aggregated_views,
    left_on = 'Title',
    right_on = 'Content Name',
    how = 'inner'
).sort_values(by='Position').reset_index(drop=True)

print(result_frame.head())

