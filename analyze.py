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

print(content_frame.head())

