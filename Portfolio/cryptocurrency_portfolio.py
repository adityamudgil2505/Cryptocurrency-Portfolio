import os
import json
import requests
from prettytable import PrettyTable
from datetime import datetime as dt
from colorama import Fore, Back, Style

convert = input('Enter the currency: example USD ')
convert = convert.upper()

linking_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
end_url = '?structure=array&convert='+convert
request = requests.get(linking_url)
result = request.json()
data = result['data']

ticker_url_pair = {}
for currency in data:
    symbol = currency['symbol']
    id = currency['id']
    ticker_url_pair[symbol] = id

print('\nMY PORTFOLIO\n')
portfolio_value = 0.00
total_amount_invested = 0.00
last_updated = 0
table = PrettyTable(['Asset','Unit owned','Price per unit','Amount Invested','Current Price per unit','% changed in 1h','% changed in 24h','% changed in 7d','Current Value','Profit/Loss %'])

def colorCoding(percent_var):
    if percent_var > 0 :
        percent_var = Back.GREEN + str(percent_var)+'%' + Style.RESET_ALL
    elif percent_var == 0:
        percent_var = Back.BLUE + str(percent_var) + '%' + Style.RESET_ALL
    else:
        percent_var = Back.RED + str(percent_var) + '%' + Style.RESET_ALL
    return percent_var

with open('portfolio.txt') as inp:
    for line in inp:
        ticker,unit_owned,at_price = line.split()
        ticker = ticker.upper()
        ticker_url = 'https://api.coinmarketcap.com/v2/ticker/'+ str(ticker_url_pair[ticker]) + end_url

        request = requests.get(ticker_url)
        result = request.json()
#        print(json.dumps(result, sort_keys = True, indent = 4))
        amount_invested = float(unit_owned) * float(at_price)
        currency = result['data'][0]
        name = currency['name']
        symbol = currency['symbol']
        last_updated = currency['last_updated']
        quotes = currency['quotes'][convert]
        current_price = quotes['price']
        percent_1h = quotes['percent_change_1h']
        percent_24h = quotes['percent_change_24h']
        percent_7d = quotes['percent_change_7d']
        current_value = float(unit_owned) * float(current_price)
        profit_loss = (current_value-amount_invested)/amount_invested * 100
        # getting rid of NoneType
        def getting_rid(percent_var):
            try:
                percent_var+=1
            except:
                percent_var = 0
            return percent_var
        percent_1h = getting_rid(percent_1h)
        percent_24h = getting_rid(percent_24h)
        percent_7d = getting_rid(percent_7d)
        # rounding % changed
        percent_1h = round(percent_1h,2)
        percent_24h = round(percent_24h,2)
        percent_7d = round(percent_7d,2)
        profit_loss = round(profit_loss,2)
        # string variable
        at_price_string = round(float(at_price),2)
        at_price_string = '{:,}'.format(at_price_string)
        amount_invested_string = round(float(amount_invested),2)
        amount_invested_string = '{:,}'.format(amount_invested_string)
        current_price_string = round(current_price,2)
        current_price_string = '{:,}'.format(current_price_string)
        current_value_string = round(current_value,2)
        current_value_string = '{:,}'.format(current_value_string)
        # color coding
        percent_1h = colorCoding(percent_1h)
        percent_24h = colorCoding(percent_24h)
        percent_7d = colorCoding(percent_7d)
        profit_loss = colorCoding(profit_loss)

        portfolio_value += current_value
        total_amount_invested += amount_invested
        table.add_row([name+' ({})'.format(symbol), unit_owned, at_price_string, amount_invested_string, current_price_string, str(percent_1h),str(percent_24h),str(percent_7d),current_value_string,profit_loss])

print(table)
last_updated_string = dt.fromtimestamp(last_updated).strftime('%b %d,%Y at %I:%M%p')
overall_profit_loss = (portfolio_value-total_amount_invested)/total_amount_invested * 100
portfolio_value = round(portfolio_value,2)
portfolio_value = '{:,}'.format(portfolio_value)
total_amount_invested = round(total_amount_invested,2)
total_amount_invested = '{:,}'.format(total_amount_invested)
print('Total amount invested : '+str(total_amount_invested))
print('Portfolio Value : '+str(portfolio_value))
overall_profit_loss = round(overall_profit_loss,2)
overall_profit_loss = colorCoding(overall_profit_loss)
print('Overall Profit/Loss : ' + overall_profit_loss)
print('Last updated on '+last_updated_string)
print()
