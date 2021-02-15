import pandas as pd

from tariff import BULB_TARIFF
from load_readings import get_readings
from utils import clean_df, calculate_avg, pre_calculus


def calculate_bill(member_id: str = None,
                   account_id: str = None,
                   bill_date: str = None,
                   service_type: str = 'electricity',) -> tuple:
    """
    Compute the bill for the customer
    :param member_id: (str)
    :param account_id: (str) 'electricity', or 'gas'
    :param service_type: (str)
    :param bill_date: (str) 'YYYY-MM'
    :return: (tuple)
    """
    """
    if (member_id == 'member-123' and
        account_id == 'ALL' and
            bill_date == '2017-08-31'):
        amount = 27.57
        kwh = 167
    else:
        amount = 0.
        kwh = 0
    return amount, kwh
    """
    # TODO REFACTOR ME :)

    service_tariff = BULB_TARIFF[service_type]

    bill_year, bill_month = bill_date.split('-')[0], bill_date.split('-')[1]

    data = get_readings()
    # Read the nested data
    if account_id == 'ALL':
        service_data = []
        for account in data[member_id][0].keys():
            for register in data[member_id][0][account][0][service_type]:
                service_data.append(register)
    else:
        member_data = data[member_id][0][account_id][0]
        service_data = member_data[service_type]

    df = pd.DataFrame.from_dict(service_data)
    df['readingDate'] = pd.to_datetime(df['readingDate'])

    # Get the average month and day values before filter the df
    month_avg, day_avg = calculate_avg(df)

    # Get interested data
    filtered_df = clean_df(df, bill_year, bill_month)

    if len(filtered_df) == 1:
        first_month = True
    else:
        first_month = False
        day_avg = None

    pre_df = pre_calculus(df=filtered_df, first_month=first_month, day_avg=day_avg)

    pre_df['consum_pence'] = pre_df['month_consum'] * service_tariff['unit_rate']
    pre_df['days_pence'] = pre_df['daysinmonth'] * service_tariff['standing_charge']
    pre_df['pence_month_bill'] = pre_df['consum_pence'] + pre_df['days_pence']
    pre_df['pound_month_bill'] = round(pre_df['pence_month_bill'] / 100, 2)

    amount, kwh = pre_df['pound_month_bill'].iloc[-1], pre_df['month_consum'].iloc[-1]
    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
