import pandas as pd
import os

class DataConverter:
    """
    A class to handle data conversion from a pipe-delimited TXT file
    to a comma-separated CSV file.
    """
    def __init__(self, input_filepath, output_filepath):
        """
        Initializes the DataConverter with input and output file paths.

        Args:
            input_filepath (str): The path to the input pipe-delimited .txt file.
            output_filepath (str): The path for the output comma-separated .csv file.
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def convert_to_csv(self, delimiter='|'):
        """
        Reads the specified input file and converts it to a CSV file.

        Args:
            delimiter (str): The delimiter used in the input file. Defaults to '|'.

        Returns:
            str: The path to the converted CSV file if successful, otherwise None.
        """
        # Check if the input file exists
        if not os.path.exists(self.input_filepath):
            print(f"Error: The input file '{self.input_filepath}' was not found.")
            return None

        print(f"Attempting to read '{self.input_filepath}'...")
        
        try:
            # Read the pipe-delimited file into a pandas DataFrame
            df = pd.read_csv(self.input_filepath, sep=delimiter)
            print("File read successfully.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

        print(f"Converting and saving data to '{self.output_filepath}'...")
        
        try:
            # Save the DataFrame to a CSV file
            # index=False prevents pandas from writing the DataFrame index to the CSV.
            df.to_csv(self.output_filepath, index=False)
            print(f"Conversion successful! The file is saved at '{self.output_filepath}'.")
            return self.output_filepath
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")
            return None

    def load_data_as_dataframe(self):
        """
        Loads the converted CSV file into a pandas DataFrame.
        If the CSV file does not exist, it will first convert the TXT file.

        Returns:
            pandas.DataFrame: The DataFrame containing the data. Returns None if conversion or loading fails.
        """
        # If the CSV file doesn't exist, convert it first
        if not os.path.exists(self.output_filepath):
            print(f"CSV file '{self.output_filepath}' not found. Converting from TXT...")
            converted_path = self.convert_to_csv()
            if converted_path is None:
                print("Failed to convert the file. Cannot load DataFrame.")
                return None
        
        # Now, load the CSV file into a DataFrame
        print(f"Loading data from '{self.output_filepath}' into a DataFrame...")
        try:
            df = pd.read_csv(self.output_filepath)
            print("DataFrame loaded successfully.")
            return df
        except Exception as e:
            print(f"An error occurred while loading the CSV file: {e}")
            return None

# testing the class independently)
if __name__ == '__main__':
  
    input_file_path = 'data/MachineLearningRating_v3.txt' 
    output_file_path = 'data/MachineLearningRating_v3.csv'

    converter = DataConverter(input_file_path, output_file_path)
    
    # This will convert the file and create the CSV
    csv_path = converter.convert_to_csv()
    
    if csv_path:
        # This will load the newly created CSV into a DataFrame
        df = converter.load_data_as_dataframe()
        if df is not None:
            print("\nDataFrame Info:")
            print(df.info())
            print("\nFirst 5 rows of the DataFrame:")
            print(df.head())