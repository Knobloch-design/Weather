import numpy as np
import pandas as pd

# Path to the CSV file
csv_file_path = r"C:\Users\aleck\OneDrive\Documents\GitHub\Weather\Weather_Data.csv"

def read_csv_to_numpy(csv_file_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame to a NumPy array
        data_array = df.to_numpy()

        return data_array
    except Exception as e:
        print(f"Error: {e}")
        return None
    

# Call the function to read CSV and convert to NumPy array
weather_data_array = read_csv_to_numpy(csv_file_path)

print(weather_data_array[0][5])
print(type(weather_data_array[0][5]))
print(pd.isnull(weather_data_array[0][5]))


def remove_columns_with_majority_null(data_array):
    """
    Removes columns from a NumPy array if the majority of values in the column are null.

    Args:
        data_array (numpy.ndarray): The input NumPy array.

    Returns:
        numpy.ndarray: The cleaned NumPy array with columns containing majority null values removed.
    """
    # Convert the NumPy array to a pandas DataFrame
    df = pd.DataFrame(data_array)

    # Calculate the percentage of null values in each column
    null_percentages = df.isnull().mean()

    # Find columns with null percentage greater than or equal to 0.8 (80%)
    columns_to_remove = null_percentages[null_percentages >= 0.9].index
    
    removed_columns = ""
    for x in columns_to_remove:
        removed_columns= removed_columns+", "+str(x)
    print("removed columns: ", removed_columns)
    print("columns_to_remove: ", columns_to_remove)
    # Remove columns with high null percentage
    cleaned_df = df.drop(columns=columns_to_remove)

    # Convert the cleaned DataFrame back to a NumPy array
    cleaned_data_array = cleaned_df.to_numpy()

    return cleaned_data_array



print("Original data array:")
#print(weather_data_array)

# Remove columns with majority null values
cleaned_data_array = remove_columns_with_majority_null(weather_data_array)

print("\nCleaned data array (removed columns with majority null values):")
print(cleaned_data_array)

if weather_data_array is not None:
    print("Weather data successfully loaded into NumPy array:")
    print(weather_data_array)
else:
    print("Failed to load weather data into NumPy array.")

