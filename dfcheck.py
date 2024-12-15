import pandas as pd

class DataFrameComparator:
    def __init__(self, df1, df2):
        """
        Initialize the comparator with two dataframes or objects that can be converted to dataframes.
        """
        if not isinstance(df1, pd.DataFrame):
            try:
                df1 = pd.DataFrame(df1)
            except Exception as e:
                raise ValueError("df1 must be a pandas DataFrame or convertible to one.") from e

        if not isinstance(df2, pd.DataFrame):
            try:
                df2 = pd.DataFrame(df2)
            except Exception as e:
                raise ValueError("df2 must be a pandas DataFrame or convertible to one.") from e

        self.df1 = df1
        self.df2 = df2


    def compare_row_count(self) -> pd.DataFrame:
        """
        Compare the row counts of the two dataframes and calculate the percentage change in df2 from df1.
        """
        row_count_df1 = len(self.df1)
        row_count_df2 = len(self.df2)

        # Calculate percentage change
        if row_count_df1 == 0:  
            percentage_change = None  
        else:
            percentage_change = ((row_count_df2 - row_count_df1) / row_count_df1) * 100

        # Create the result DataFrame
        comparison = {
            'DataFrame': ['df1', 'df2'],
            'Row Count': [row_count_df1, row_count_df2],
            'Percentage Change': [None, percentage_change] 
        }
        return pd.DataFrame(comparison)


    def check_nulls(self, df: pd.DataFrame, name_column: str) -> pd.DataFrame:
        """
        Identify rows where any of the target columns contain null values and return the corresponding rows.
        
        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            name_column (str): The column containing names (e.g., employee names).
        
        Returns:
            pd.DataFrame: A DataFrame with the rows where any of the columns (except name_column) have null values.
        """
        # Ensure the name column exists in the DataFrame
        if name_column not in df.columns:
            raise ValueError(f"Column '{name_column}' does not exist in the DataFrame.")
        
        # Determine target columns (all columns except the name_column)
        target_columns = [col for col in df.columns if col != name_column]
        
        # Find rows with nulls in any target column
        null_rows = df[target_columns].isnull().any(axis=1)
        
        # Filter the DataFrame to only the rows with nulls
        filtered_df = df[null_rows]
        
        # Return the relevant columns (including the name column and all original columns)
        result = filtered_df.reset_index(drop=True)
        
        return result

    def filter_by_column_value(self, df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
        """
        Filter rows in the DataFrame where the given column matches the specified value.
        
        Args:
            df (pd.DataFrame): The DataFrame to filter.
            column (str): The column to filter on.
            value (str): The value to filter by.
        
        Returns:
            pd.DataFrame: A DataFrame containing only the rows where the column matches the value.
        """
        # Ensure the column exists in the DataFrame
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
        # Filter the DataFrame based on the value in the given column
        filtered_df = df[df[column] == value]
        
        return filtered_df
   

    def check_row_count(self, df: pd.DataFrame, value: int) -> pd.DataFrame:
        """
        Check if the number of rows in the DataFrame exceeds the given value and return a report with 'Greater' or 'Lesser' result.
        
        Args:
            df (pd.DataFrame): The DataFrame to check.
            value (int): The value to compare the number of rows against.
        
        Returns:
            pd.DataFrame: A DataFrame with the row count, threshold value, and a comparison result ("Greater" or "Lesser").
        """
        # Get the number of rows in the DataFrame
        row_count = len(df)
        
        # Compare the row count with the given value
        if row_count > value:
            result = "Greater"  # Row count is greater than the value
        else:
            result = "Lesser"  # Row count is less than or equal to the value
        
        # Create a DataFrame to hold the result
        result_df = pd.DataFrame({
            'Row Count': [row_count],
            'Threshold Value': [value],
            'Comparison Result': [result]
        })
        
        return result_df


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

