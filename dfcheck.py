import pandas as pd

class DataFrameComparator:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """Initialize the comparator with two dataframes."""
        self.df1 = df1
        self.df2 = df2

    def compare_row_count(self) -> pd.DataFrame:
        """Compare the row counts of the two dataframes."""
        comparison = {
            'DataFrame': ['df1', 'df2'],
            'Row Count': [len(self.df1), len(self.df2)]
        }
        return pd.DataFrame(comparison)

    def check_null_counts(self) -> pd.DataFrame:
        """Check the null counts in both dataframes and compare."""
        df1_nulls = self.df1.isnull().sum()
        df2_nulls = self.df2.isnull().sum()
        comparison = pd.DataFrame({
            'Column': self.df1.columns,
            'df1 Null Count': df1_nulls,
            'df2 Null Count': df2_nulls
        }).reset_index(drop=True)
        return comparison

    def compare_columns(self) -> pd.DataFrame:
        """Compare the column names of the two dataframes."""
        df1_columns = set(self.df1.columns)
        df2_columns = set(self.df2.columns)

        comparison = {
            'Columns in df1 Only': list(df1_columns - df2_columns),
            'Columns in df2 Only': list(df2_columns - df1_columns),
            'Common Columns': list(df1_columns & df2_columns)
        }
        return pd.DataFrame({key: pd.Series(value) for key, value in comparison.items()})

    def compare_summary(self) -> pd.DataFrame:
        """Provide a summary comparison for numeric columns."""
        common_columns = self.df1.columns.intersection(self.df2.columns)
        numeric_columns = [col for col in common_columns if pd.api.types.is_numeric_dtype(self.df1[col])]

        summary = []
        for col in numeric_columns:
            df1_stats = self.df1[col].describe()
            df2_stats = self.df2[col].describe()
            comparison = {
                'Metric': df1_stats.index,
                f'{col} in df1': df1_stats.values,
                f'{col} in df2': df2_stats.values
            }
            summary.append(pd.DataFrame(comparison))

        return pd.concat(summary, ignore_index=True) if summary else pd.DataFrame()

