import logging

import pandas as pd

logger = logging.getLogger(__name__)


def split_date_column(data, date_column, new_prefix=None):
    """
    :param data: The DataFrame containing the date column to be split.
    :param date_column: The name of the column containing date/time values.
    :param new_prefix: An optional prefix to be added to the names of the new columns.
    :return: The DataFrame with the original date column replaced by new columns for year, month, day, day of the week, hour, and minute.
    """
    data[date_column] = pd.to_datetime(data[date_column])
    year_name = "year" if new_prefix is None else f"{new_prefix}Year"
    month_name = "month" if new_prefix is None else f"{new_prefix}Month"
    day_name = "day" if new_prefix is None else f"{new_prefix}Day"
    day_of_week_name = "weekDay" if new_prefix is None else f"{new_prefix}WeekDay"
    hour_name = "hour" if new_prefix is None else f"{new_prefix}Hour"
    minute_name = "minute" if new_prefix is None else f"{new_prefix}Minute"
    data[year_name] = data[date_column].dt.year.astype(int)
    data[month_name] = data[date_column].dt.month.astype(int)
    data[day_name] = data[date_column].dt.day.astype(int)
    day_names = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    data[day_of_week_name] = data[date_column].dt.dayofweek.map(day_names)
    # data[day_of_week_name] = data[date_column].dt.dayofweek.astype(int)
    if data[date_column].dt.time.nunique() > 1:
        data[hour_name] = data[date_column].dt.hour.astype(int)
        data[minute_name] = data[date_column].dt.minute.astype(int)
    data.drop(columns=[date_column], inplace=True)


def combine_dataframes_on_columns(df1, df2, columns):
    """
    :param df1: First dataframe to be combined.
    :type df1: pandas.DataFrame
    :param df2: Second dataframe to be combined.
    :type df2: pandas.DataFrame
    :param columns: List of column pairs (tuples) to merge on, where each tuple represents the column names in the respective dataframes.
    :type columns: list of tuple
    :return: Combined dataframe with columns merged on specified column pairs.
    :rtype: pandas.DataFrame
    """
    combined_df = pd.merge(
        df1,
        df2,
        left_on=[col[0] for col in columns],
        right_on=[col[1] for col in columns],
        how="outer",
        suffixes=("_left", "_right"),
    )
    combined_df = combined_df.drop_duplicates(
        subset=[col[0] for col in columns], keep="first"
    )
    combined_df.columns = combined_df.columns.str.replace(
        "_left|_right", "", regex=True
    )
    return combined_df


def change_naps(df, column):
    """
    :param df: The DataFrame containing the data to be processed.
    :param column: The name of the column in the DataFrame where the function will apply the nap classification.
    :return: The modified DataFrame with updated values in the specified column, categorizing entries as "With nap" or "Without nap" based on their content.
    """
    df[column] = df[column].apply(
        lambda x: "With nap" if pd.notna(x) and x != "" else "Without nap"
    )


def remove_column_by_name(df, column_name):
    """
    :param df: The input dataframe from which a column needs to be removed
    :type df: pandas.DataFrame

    :param column_name: The name of the column that needs to be removed from the dataframe
    :type column_name: str

    :return: None
    """
    if column_name in df.columns:
        df.drop(columns=[column_name], inplace=True)


def remove_columns_by_names(df, column_names):
    """
    :param df: DataFrame from which columns should be removed.
    :type df: pandas.DataFrame
    :param column_names: List of column names to be removed from the DataFrame.
    :type column_names: list of str
    :return: DataFrame with specified columns removed.
    :rtype: pandas.DataFrame
    """
    for column_name in column_names:
        if column_name in df.columns:
            df.drop(columns=[column_name], inplace=True)


def remove_rows_with_empty_cells(df):
    """
    :param df: A Pandas DataFrame from which rows with any empty cells should be removed.
    :return: A new DataFrame with rows containing empty cells dropped.
    """
    return df.dropna(how="any")


def combine_columns(df, col1, col2, new_col):
    """
    :param df: DataFrame containing the columns to be combined
    :param col1: Name of the first column to be combined, containing day values
    :param col2: Name of the second column to be combined, containing month values
    :param new_col: Name of the new column to be created, containing the combined datetime values
    :return: DataFrame with the new combined column added
    """
    df[new_col] = pd.to_datetime(
        df[col1].astype(str) + "-" + df[col2].astype(str).str.zfill(2),
        format="%d-%m",
        errors="coerce",
    )


def scale(row, hour_name, minute_name, is_two_days, middle):
    """
    :param row: Dictionary containing time data with keys corresponding to `hour_name` and `minute_name`.
    :param hour_name: Key in the `row` dictionary representing the hour.
    :param minute_name: Key in the `row` dictionary representing the minute.
    :param is_two_days: Boolean indicating if the time calculation should account for a two-day span.
    :param middle: Hour in the range 0-24 used as the midpoint to determine if hours should increment by 24 due to spanning two days.
    :return: Time in hours as a float, rounded to two decimal places.
    """
    complex_hour = row[hour_name] + row[minute_name] / 60
    if is_two_days and complex_hour < middle:
        complex_hour += 24
    return round(complex_hour, 2)


def scale_hour_minute(
    df, hour_name, minute_name, new_hour_name, is_two_days=False, middle=15
):
    """
    :param df: DataFrame containing the data to be scaled.
    :param hour_name: Name of the column in the DataFrame representing the hour.
    :param minute_name: Name of the column in the DataFrame representing the minute.
    :param new_hour_name: Name of the new column to be added to the DataFrame after scaling.
    :param is_two_days: Boolean flag indicating if the time range covers two days.
    :param middle: The middle minute value for determining the scaling.
    :return: DataFrame with the new scaled hour column added.
    """
    df[new_hour_name] = df.apply(
        lambda row: scale(row, hour_name, minute_name, is_two_days, middle), axis=1
    )
    return df


def round_all_columns(df):
    """
    :param df: A pandas DataFrame whose numerical columns need to be rounded to the nearest integer.
    :return: A pandas DataFrame with all numerical columns rounded to the nearest integer.
    """
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.round().astype(int))
    return df
