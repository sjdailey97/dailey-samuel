import pandas as pd
import numpy as np
from datetime import datetime

class DataEngineering():
    def __init__(self, filename):
        self.dataset = self.load_dataset(filename)

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

    def standardize_dates(self, column_names):
        self.dataset[column_names] = pd.to_datetime(self.dataset[column_names])

    def trim_spaces(self, column_names):
        if not isinstance(column_names,list):
            column_names = [column_names]
        for column_name in column_names:
            if column_name in self.dataset.columns:
                self.dataset[column_name] = self.dataset[column_name].str.strip()

    def resolve_anomalous_dates(self, column_name):
        if column_name in self.dataset.columns:
            # Convert the column to datetime if it's not already
            now = datetime.now()
            self.dataset[column_name] = self.dataset[column_name][self.dataset[column_name] <= now]

    def expand_dates(self, column_name):
        self.dataset[column_name] = pd.to_datetime(self.dataset[column_name])
        self.dataset['day_of_week'] = self.dataset[column_name].dt.dayofweek
        self.dataset['hour_of_day'] = self.dataset[column_name].dt.hour
        return self.dataset

    def categorize_transactions(self):
        low = self.dataset.amt.quantile(0.25)
        medium = self.dataset.amt.quantile(0.75)
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
            'amt': (0, 1000000),  # transaction amounts should be between 0 and 1,000,000
            'lat': (-180, 180),  # latitude should be between -180 and 180
            'long': (-90, 90),  # longitude should be between -180 and 180
            'zip': (0, 99999),  # zip codes should be between 0 and 99999
            'city_pop': (0, 10**10),  # city population should be between 0 and 10 Billion
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
        mean = self.dataset['amt'].mean()
        std = self.dataset['amt'].std()
        return not any(abs(self.dataset['amt'] - mean) > 60*std)

    def categorical_data_validation(self):
        # Define the expected values
        categories = [
            'SHOPPING_POS', 'misc_pos', 'GROCERY_POS', 'MISC_POS',
            'grocery_pos', 'MISC_NET', 'SHOPPING_NET', 'gas_transport',
            'grocery_net', 'shopping_pos', 'FOOD_DINING', 'misc_net',
            'GROCERY_NET', 'GAS_TRANSPORT', 'shopping_net', 'entertainment',
            'ENTERTAINMENT', 'food_dining', 'health_fitness', 'HOME',
            'personal_care', 'KIDS_PETS', 'PERSONAL_CARE', 'home',
            'kids_pets', 'travel', 'TRAVEL', 'HEALTH_FITNESS']
        sexes = ['F', 'M']

        # Get the unique values in the 'sex' column
        if not set(self.dataset['sex'].unique()).issubset(sexes):
            return False
        # Check if all actual values are in the expected values
        if not set(self.category.unique()).issubset(categories):
            return False
        return True

    def clean_data(self):
        self.clean_missing_values()
        self.remove_duplicates()
        self.standardize_dates('trans_date_trans_time')
        self.trim_spaces(['category','sex','merchant','first','last','job'])
        self.resolve_anomalous_dates('trans_date_trans_time')

    def data_transformation(self):
        self.expand_dates('trans_date_trans_time')
        self.categorize_transactions()

    def data_validation(self):
        return (self.range_checks() and self.null_checks() and
                self.type_validation() and self.uniqueness_validation() and
                self.historical_data_consistency() and self.categorical_data_validation())

# def main():
#     # Initialize the DataEngineering object
#     data_engineering = DataEngineering('fraud_detection_system/transactions_0.csv')
#     data_engineering.clean_data()
#     data_engineering.data_transformation()
#     data_engineering.data_validation()
#     # Test the describe function
#     print("Describe function output:")
#     print(data_engineering.describe(5))

#     # Test the clean_missing_values function
#     data_engineering.clean_missing_values()
#     print("Missing values cleaned.")

#     # Test the remove_duplicates function
#     data_engineering.remove_duplicates()
#     print("Duplicates removed.")

#     # Test the standardize_dates function
#     # Assuming 'date' is a column in your dataset
#     data_engineering.standardize_dates('trans_date_trans_time')
#     print("Dates standardized.")

#     # Test the trim_spaces function
#     # Assuming 'name' is a column in your dataset
#     data_engineering.trim_spaces(['merchant'])
#     print("Spaces trimmed.")

#     # Test the resolve_anomalous_dates function
#     # Assuming 'date' is a column in your dataset
#     data_engineering.resolve_anomalous_dates('trans_date_trans_time')
#     print("Anomalous dates resolved.")

#     # Test the expand_dates function
#     # Assuming 'date' is a column in your dataset
#     data_engineering.expand_dates('trans_date_trans_time')
#     print("Dates expanded.")

#     # Test the categorize_transactions function
#     data_engineering.categorize_transactions()
#     print("Transactions categorized.")

#     # Test the range_checks function
#     print("Range checks passed: ", data_engineering.range_checks())

#     # Test the null_checks function
#     print("Null checks passed: ", data_engineering.null_checks())

#     # Test the type_validation function
#     print("Type validation passed: ", data_engineering.type_validation())

#     # Test the uniqueness_validation function
#     print("Uniqueness validation passed: ", data_engineering.uniqueness_validation())

#     # Test the historical_data_consistency function
#     print("Historical data consistency check passed: ", data_engineering.historical_data_consistency())

#     # Test the categorical_data_validation function
#     print("Categorical data validation passed: ", data_engineering.categorical_data_validation())

if __name__ == "__main__":
    main()
