# Bulb Energy Usage (Python) coding challenge

A small program added to, given a set of meter readings, computes a member’s monthly energy bill.


## Installation

``` bash
$ pip install -r requirements
```

or 

``` bash
$ pip install pandas
```

## Python version
3.7.4 

## Usage
```bash
$ python main.py --member_id <member_id> --bill_date <YYYY-MM-DD>
```

## Examples
```
$ python main.py --member_id 'member-123' --bill_date '2017-03-28'

Hello member-123!
Your bill for ALL on 2017-03-28 is £38.68
based on 260kWh of usage in the last month
```

```
$ python main.py --member_id 'member-123' --bill_date '2017-08-28'

Hello member-123!
Your bill for ALL on 2017-08-28 is £27.57
based on 167kWh of usage in the last month
```

## Test

``` bash
$ python test_bill_member.py 
.
----------------------------------------------------------------------
Ran 1 test in 0.024s

OK

```

## TODO

* [ ] Fix the pandas warning 
`bulb-energy-usage/utils.py:22: UserWarning: Boolean Series key will be reindexed to match DataFrame index.
  filtered_df = df_year[interest_months_filter].copy()`
* [ ] Check edge cases (wrong date format, wrong data, object types in general)
* [ ] Add data, tariff and tests for gas bills.

## Comments

Really fun challenge!

I spent a lot of time thinking something went wrong about Watts/kWatts units, but it was pence vs pounds conversion :(