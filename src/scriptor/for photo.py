import requests
yourtoken = 'b58b68b9f156fae188bb48f29c156f7e50714d54'


def DataReader(ticker, d_start, d_end):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + yourtoken
    }
    url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + d_start + "&endDate=" + d_end
    requestResponse = requests.get(url, headers=headers)
    json_result = requestResponse.json()

    return json_result