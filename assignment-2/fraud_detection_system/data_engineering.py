import pandas as pd
import numpy as np

class DataEngineering():
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            self.dataset = data
        elif data[:-4] == '.csv':
            self.dataset = self.load_dataset(data)

    def load_dataset(self, filename):
        return pd.read_csv(filename)

    def describe(self, N):
        print(self.dataset.head(N))

        # Total number of rows
        total_rows = len(self.dataset)
        # Column names
        column_names = self.dataset.columns.tolist()
        # Data types of columns
        column_types = self.dataset.dtypes
        results = {
            "Total number of rows": total_rows,
            "Column names": column_names,
            "Data types of columns": column_types,
            "Number of columns": len(column_names)
        }
        return results


    def clean_missing_values(self):
        self.dataset = self.dataset.dropna()

    def remove_duplicates(self):
        self.dataframe = self.dataset.drop_duplicates()

    def standardize_dates(self, column_names='trans_date_trans_time'):
        self.dataset[column_names] = pd.to_datetime(self.dataset[column_names])

    def trim_spaces(self, column_name):
        if column_name in self.dataset.columns:
            self.dataset[column_name] = self.dataset[column_name].str.strip()

    def resolve_anomalous_dates(self, column_name):
        if column_name in self.dataset.columns:
            # Convert the column to datetime if it's not already
            if self.dataset[column_name].dtype != 'datetime64[ns]':
                self.dataset[column_name] = pd.to_datetime(self.dataset[column_name])

    def expand_dates(self, column_name='trans_date_trans_time'):
        self.dataset[column_name] = pd.to_datetime(self.dataset[column_name])
        self.dataset['day_of_week'] = self.dataset[column_name].dt.dayofweek
        self.dataset['hour_of_day'] = self.dataset[column_name].dt.hour
        return self.dataset

    def categorize_transactions(self, low, medium, high):
        conditions = [
            (self.dataset['amt'] <= low),
            (self.dataset['amt'] > low) & (self.dataset['amt'] <= medium),
            (self.dataset['amt'] > medium)
        ]
        categories = ['low', 'medium', 'high']
        self.dataset['amt_category'] = np.select(conditions, categories, default='high')
        return self.dataset

    def range_checks(self):
        expected_ranges = {
            'amt': (0, 10000),  # transaction amounts should be between 0 and 10,000
            'lat': (-90, 90),  # latitude should be between -90 and 90
            'long': (-180, 180),  # longitude should be between -180 and 180
            'zip': (0, 99999),  # zip codes should be between 0 and 99999
            'city_pop': (0, 10**8),  # city population should be between 0 and 100 million
            'unix_time': (10**9, 10**10),  # unix time should be between 1 billion and 10 billion
            'merch_lat': (-90, 90),  # merchant latitude should be between -90 and 90
            'merch_long': (-180, 180),  # merchant longitude should be between -180 and 180
            'is_fraud': (0, 1),  # is_fraud should be either 0 or 1
        }

        for column, (lower_bound, upper_bound) in expected_ranges.items():
            if column in self.dataset.columns:
                if not (self.dataset[column].min() >= lower_bound and self.dataset[column].max() <= upper_bound):
                    return False

        return True

    def null_checks(self):
        return not self.dataset.isnull().values.any()

    def type_validation(self):
        # Define the expected data types
        expected_dtypes = {
            'trans_date_trans_time': 'object',
            'cc_num': 'int64',
            'merchant': 'object',
            'category': 'object',
            'amt': 'float64',
            'first': 'object',
            'last': 'object',
            'sex': 'object',
            'street': 'object',
            'city': 'object',
            'state': 'object',
            'zip': 'float64',
            'lat': 'float64',
            'long': 'float64',
            'city_pop': 'float64',
            'job': 'object',
            'dob': 'object',
            'trans_num': 'object',
            'unix_time': 'float64',
            'merch_lat': 'float64',
            'merch_long': 'float64',
            'is_fraud': 'float64'
        }

        # Get the actual data types of the dataframe
        actual_dtypes = self.dataset.dtypes.to_dict()

        # Validate the data types
        for column, expected_dtype in expected_dtypes.items():
            actual_dtype = actual_dtypes.get(column)
            if actual_dtype != expected_dtype:
                return False
        return True


    def uniqueness_validation(self):
        # Check if all rows are unique
        if self.dataset.duplicated().any():
            return False
        else:
            True

    def historical_data_consistency(self):
        # Implement your historical data consistency check here
        return self.type_validation() and self.uniqueness_validation()


    def categorical_data_validation(self):
        # Define the expected values
        expected_values = {np.nan, 'F', 'M'}

        # Get the unique values in the 'sex' column
        actual_values = set(self.dataset['sex'].unique())

        # Check if all actual values are in the expected values
        if actual_values.issubset(expected_values):
            return True
        else:
            return False
        
    def clean_data(self):
        self.clean_missing_values()
        self.remove_duplicates()
        self.standardize_dates()
        self.expand_dates()
        return self.dataset