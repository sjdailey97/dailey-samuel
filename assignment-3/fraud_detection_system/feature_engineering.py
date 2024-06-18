# Import necessary libraries
import pandas as pd
import json
from typing import Union, List, Dict, Tuple
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler


class FeatureConstructor:
    def __init__(self, raw_data: Union[str, pd.DataFrame], version: str):
        self.dataset = self.extract_data(raw_data)
        self.version = version
        self.data_sources = [raw_data] if isinstance(raw_data, str) else ['DataFrame input']

    def extract_data(self, dat: Union[str, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(dat, str):
            if dat.endswith('.csv'):
                return pd.read_csv(dat)
            elif dat.endswith('.parquet'):
                return pd.read_parquet(dat)
            elif dat.endswith('.json'):
                return pd.read_json(dat)
        elif isinstance(dat, pd.DataFrame):
            return dat
        else:
            raise ValueError("Invalid input: please provide a file path (csv, parquet, json) or a pandas DataFrame.")

    def load(self, output_filename: str, format: str = None) -> None:
        if format == 'csv' or output_filename.endswith('.csv'):
            self.dataset.to_csv(output_filename, index=False)
        elif format == 'parquet' or output_filename.endswith('.parquet'):
            self.dataset.to_parquet(output_filename)
        elif format == 'json' or output_filename.endswith('.json'):
            self.dataset.to_json(output_filename)
        else:
            raise ValueError("Invalid format: please provide 'csv', 'parquet', or 'json'.")

    def get_data_sources(self) -> List[str]:
        return self.data_sources

    def set_version(self, version: str) -> None:
        self.version = version

    def transform(self, *args, **kwargs) -> pd.DataFrame:
        if 'category' in self.dataset.columns:
            encoder = LabelEncoder()
            self.dataset['category_encoded'] = encoder.fit_transform(self.dataset['category'])

        # Feature Scaling
        if 'amt' in self.dataset.columns:
            scaler = StandardScaler()
            self.dataset['amt_scaled'] = scaler.fit_transform(self.dataset[['amt']])

        # Feature Extraction
        if 'trans_date_trans_time' in self.dataset.columns:
            self.dataset['transaction_hour'] = self.dataset['trans_date_trans_time'].dt.hour

        return self.dataset

    def describe(self, dataframe: pd.DataFrame, output_file: str = None) -> Dict:
        description = {
            'version': self.version,
            'data sources': self.data_sources,
            'column names': list(dataframe.columns),
            'date ranges': (dataframe.index.min(), dataframe.index.max())
        }
        measures = dataframe.describe().to_dict()
        result = {'description': description, 'measures': measures}
        if output_file is not None:
            with open(output_file, 'w') as f:
                json.dump(result, f)
        return result
