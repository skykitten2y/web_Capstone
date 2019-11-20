import requests
import pandas as pd

yourtoken = 'b58b68b9f156fae188bb48f29c156f7e50714d54'


def DataReader(ticker, d_start, d_end):
    # We are expecting DateTime type for input dates !! (just like original Pandas DataReader)

    # d_end = d_end.strptime('%Y-%m-%d')
    # d_start = d_start.strptime('%Y-%m-%d')
    # print d_start
    # print d_endsd

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + yourtoken
    }
    url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + d_start + "&endDate=" + d_end

    # print url
    requestResponse = requests.get(url, headers=headers)
    json_result = requestResponse.json()

    # df = pd.DataFrame.from_records(json_result)

    # Check for existance of Adj Close column
    # If not, check for existance of Close column
    # If not -> throw error
    # If no Adj Close, but Close, copy Close to Adj close

    # if not 'adjClose' in df.columns:
    #     if 'close' in df.columns:
    #         df['adjClose'] = df['close']
    #     else:
    #         print "Error: No Close information"
    #         return
    #
    # # Convert ISO date format to Pandas DateTime
    # df['date'] = pd.to_datetime(df['date'])
    # # Align Column Names to previous DataReader names
    # df = df.rename(columns={'date': 'Date', 'open': 'Open', 'adjClose': 'Adj Close', 'volume': 'Volume', 'high': 'High',
    #                         'low': 'Low', 'close': 'Close'})
    # a = df.set_index(['Date'])
    # # print a
    return json_result