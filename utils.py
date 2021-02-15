

def clean_df(df, bill_year: str = None, bill_month: str = None):
    """
    Return a filtered df according to the year and month wanted,
    with an extra column with daysinmonth generated data
    :param df: (pd.Dataframe) to clean
    :param bill_year: (str)
    :param bill_month: (str)
    :return: (pd.Dataframe) with current month, year data and previous (if it exists)
    (e.g. for bill_year, bill_month = 2017, 08, returns 2017, 07 and 08 data)
    """

    # Create df year and month/s filters
    bill_year_filter = df['readingDate'].dt.year == int(bill_year)

    bill_month_filter = df['readingDate'].dt.month == int(bill_month)
    shift_month_filter = df['readingDate'].dt.month == int(bill_month) - 1
    interest_months_filter = bill_month_filter | shift_month_filter

    df_year = df[bill_year_filter]
    filtered_df = df_year[interest_months_filter].copy()
    if filtered_df.empty:
        filtered_df = df_year

    filtered_df['daysinmonth'] = filtered_df['readingDate'].dt.daysinmonth
    return filtered_df


def calculate_avg(df):
    """
    Returns the month and day average of consumption,
    calculated with the last 12 months cumulative registers
    :param df: (pd.Dataframe) clean df
    :return: (tuple) month_avg, day_avg
    """
    df.sort_values(by='readingDate')
    year_consum = df.iloc[-1]['cumulative'] - df.iloc[0]['cumulative']
    month_avg = year_consum / 12
    day_avg = year_consum / 360

    return month_avg, day_avg


def pre_calculus(df, first_month: bool = False, day_avg: float = None):
    """
    Calculus and add 'avg_day_kwh' and ''month_kwh' to the df
    :param df: (pd.Dataframe)
    :param first_month: (bool) If `True`, 'avg_day_kwh' is the calculated
    with cumulative year consumption one, otherwise it is obtained with the
    previous month data.
    :param day_avg: (float) calculated with cumulative year consumption
    :return: (pd.Dataframe) with interest data added
    """

    if first_month:
        df['avg_day_consum'] = day_avg
    else:
        df['consum_delta'] = df.cumulative.diff().shift(0)
        df['days_delta'] = df.readingDate.diff().shift(0)
        df['avg_day_consum'] = df['consum_delta'] / df['days_delta'].dt.days

    df['month_consum'] = int(df['avg_day_consum'].iloc[-1] * df['daysinmonth'].iloc[-1])

    return df

