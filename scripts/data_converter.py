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
    def clean_data_types(self, df):
        """
        Reviews and corrects the data types of columns in the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame to clean.

        Returns:
            pd.DataFrame: The DataFrame with corrected data types.
        """
        if not isinstance(df, pd.DataFrame):
            print("Error: Input is not a pandas DataFrame.")
            return df

        print("\n--- Starting Data Type Cleaning ---")

        # --- A. Convert to datetime ---
        print("Converting date columns...")
        date_cols = ['TransactionMonth', 'VehicleIntroDate']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"  - '{col}' converted to datetime.")

        # --- B. Convert to float (numeric) ---
        print("\nConverting numerical columns from object to float...")
        # Columns that might have non-numeric characters like 'R' or commas
        float_cols = ['CapitalOutstanding', 'ExcessSelected']
        for col in float_cols:
            if col in df.columns:
                # Special handling for 'ExcessSelected' to remove 'R'
                if col == 'ExcessSelected':
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace('R', '').str.strip(),
                        errors='coerce'
                    )
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"  - '{col}' converted to float.")

        # --- C. Convert to Integer or Boolean ---
        print("\nConverting count/binary columns...")

        # For integer columns (counts, codes, year)
        int_cols = ['Cylinders', 'NumberOfDoors', 'mmcode', 'RegistrationYear', 'PostalCode'] # PostalCode might be better as object/category for grouping
        for col in int_cols:
            if col in df.columns:
                # Use pandas' nullable integer type (`Int64`)
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                print(f"  - '{col}' converted to nullable integer (Int64).")

        # For binary columns ('Yes'/'No' like)
        binary_cols = ['AlarmImmobiliser', 'TrackingDevice', 'NewVehicle', 'WrittenOff',
                       'Rebuilt', 'Converted', 'CrossBorder', 'IsVATRegistered'] # Added IsVATRegistered here
        
        # More robust mapping dictionary
        binary_mapping_robust = {
            'yes': 1, 'Yes': 1, 'Y': 1, 'TRUE': 1, 'True': 1, 1: 1, '1': 1,
            'no': 0, 'No': 0, 'N': 0, 'FALSE': 0, 'False': 0, 0: 0, '0': 0
        }

        for col in binary_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.title().map(binary_mapping_robust)
                df[col] = df[col].astype('Int64', errors='ignore') # Use nullable integer
                print(f"  - '{col}' converted to binary integer (Int64).")
                
        # --- D. Convert to categorical for memory efficiency ---
        print("\nConverting object columns to category...")
        # Explicitly define categorical columns to avoid converting IDs or potentially unique strings
        categorical_cols = [
            'Citizenship', 'LegalType', 'Title', 'Language', 'Bank', 'AccountType', 'MaritalStatus',
            'Gender', 'Country', 'Province', 'MainCrestaZone', 'SubCrestaZone',
            'ItemType', 'VehicleType', 'make', 'Model', 'bodytype', 'CoverCategory',
            'CoverType', 'CoverGroup', 'Section', 'Product', 'StatutoryClass', 'StatutoryRiskType',
            'TermFrequency' # TermFrequency is likely categorical
        ]

        for col in categorical_cols:
            if col in df.columns and df[col].dtype == 'object': # Only convert if current dtype is object
                df[col] = df[col].astype('category')
                print(f"  - '{col}' converted to category.")
            elif col in df.columns and df[col].dtype != 'category': # If it's already converted to Int64 by mistake
                # This handles cases where a categorical column might have been picked up as int/float due to mixed types
                # but should ultimately be categorical
                if df[col].nunique() < len(df) / 10: # Heuristic: if unique values are less than 10% of total
                    df[col] = df[col].astype('category')
                    print(f"  - '{col}' re-converted to category (from non-object).")


        # --- E. Drop columns with no data ---
        print("\nChecking for and dropping columns with all null values...")
        cols_to_drop = [col for col in df.columns if df[col].isnull().all()]
        if cols_to_drop:
            df.drop(columns=cols_to_drop, inplace=True)
            print(f"  - Dropped columns with all nulls: {cols_to_drop}")
        else:
            print("  - No columns with all null values found to drop.")

        print("\n--- Data Type Cleaning Complete ---")
        return df
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