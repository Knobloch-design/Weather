import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import re
# Path to the CSV file
csv_file_path = r"C:\Users\aleck\OneDrive\Documents\GitHub\Weather\Weather_Data.csv"
df = pd.read_csv(csv_file_path)
#print("df Head: ",df.columns)
def read_csv_to_numpy(csv_file_path):
    try:
        # Read the CSV file into a pandas DataFrame
        

        # Convert DataFrame to a NumPy array
        data_array = df.to_numpy()

        return data_array
    except Exception as e:
        print(f"Error: {e}")
        return None
    

# Call the function to read CSV and convert to NumPy array
weather_data_array = read_csv_to_numpy(csv_file_path)
"""
print(weather_data_array[0][5])
print(type(weather_data_array[0][5]))
print(pd.isnull(weather_data_array[0][5]))
"""

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

    # Find columns with null percentage greater than or equal to 0.9 (90%)
    columns_to_remove = null_percentages[null_percentages >= 1].index
    
    removed_columns = ""
    column_names = list(df.columns.values)

    for x in columns_to_remove:
        removed_columns= removed_columns+", "+ x
    #print("columns_to_remove: ", columns_to_remove)
    #print("columns_to_remove_length: ", len(columns_to_remove))
    # Remove columns with high null percentage
    cleaned_df = df.drop(columns=columns_to_remove)

    # Convert the cleaned DataFrame back to a NumPy array
    cleaned_data_array = pd.DataFrame(cleaned_df)

    return cleaned_data_array



print("Original data array:")
#print(weather_data_array)

# Remove columns with majority null values
cleaned_data_array = remove_columns_with_majority_null(df)
#print(cleaned_data_array.columns)

#print(cleaned_data_array.describe())
#print(cleaned_data_array.head())
keyFeatures = ['DATE', 'DailyAverageWindSpeed','DailyPeakWindSpeed', 'DailyPrecipitation','DailySustainedWindSpeed','HourlyDewPointTemperature',
                'HourlyPrecipitation', 'HourlyPresentWeatherType','HourlyDryBulbTemperature','HourlyWetBulbTemperature',
                'HourlyRelativeHumidity', 'HourlySkyConditions', 'HourlyWindGustSpeed', 'HourlyWindSpeed','Sunrise', 'Sunset' ]

keyFeatures = pd.DataFrame(cleaned_data_array[keyFeatures])
#print(keyFeatures.head())
#print(cleaned_data_array.head())
#keyData = cleaned_data_array[keyFeatures]


#print(keyData.describe())

#TODO Hourly visibility and possibly other data columns have '*' entries and 
#other characters randomly throughout dataset
y = cleaned_data_array['HourlyVisibility']

y.astype('str')

for i in range(len(y)):

    if y.loc[i] == '*':
         cleaned_data_array.loc[i,'HourlyVisibility'] = '0.0'
    if bool(re.search('[a-zA-Z]', y.loc[i])):
        re.sub(cleaned_data_array.loc[i,'HourlyVisibility'], '', '[a-zA-Z]')



y = pd.DataFrame(y[:100])

try:
    y = pd.to_numeric(y,errors='coerce')
except Exception as e:
    print(f"Error: {e}")

y = y.dropna()

y = y['HourlyVisibility']
print("type y: ", type(y))
x = cleaned_data_array['DATE']
x = x[:len(y)]
for n in y:
    print("type: ",type(n))
print("y: ",y)
print("x: ",x)
"""
a = cleaned_data_array['HourlyDryBulbTemperature']
b = cleaned_data_array['HourlyWetBulbTemperature']
"""


#y = [i for i in range(10)]
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')






ax.plot(x, y, label='HourlyVisibility')  # Plot some data on the axes.
#ax.plot(x, b, label='HourlyWetBulbTemperature')  # Plot more data on the axes...
ax.set_xlabel('Time')  # Add an x-label to the axes.
ax.set_ylabel('Temperature')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.
plt.show()


#DecisionTreeRegressor does not work with time variables
#model = DecisionTreeRegressor(random_state=1)
"""model.fit(keyData, y)
print("The predictions are")
print(model.predict(keyData))"""

#print("\nCleaned data array (removed columns with majority null values):")
#print(cleaned_data_array)

"""if weather_data_array is not None:
    print("Weather data successfully loaded into NumPy array:")
    print(weather_data_array)
else:
    print("Failed to load weather data into NumPy array.")
"""
