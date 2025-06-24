'''
# The initial solution of getting dataset from the file from EDGAR downloaded
try:
    with open('/Users/snow/Downloads/companyfacts/' + file_name, 'r') as file:
        data = json.load(file)
        print('Name of company -', data['entityName'], '\nValue of assets in USD -', data['facts']['us-gaap']['Assets']['units']['USD'][len(data['facts']['us-gaap']['Assets']['units']['USD']) - 1]['val'])
except:
    print('No such file')
'''

# Better to check on SIC {6021, 6022, 6331, 6029}
# SIC only few to show {3674, 2834}

import data_processing

print(data_processing.get_posts('0000320193')['facts']['us-gaap'].keys())
#print(data_processing.get_posts('0000320193')['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
'''
import json
new_dict = {}
with open('company_tickers.json', 'r') as f:
    ticker_exhange_file = json.load(f)
for key in ticker_exhange_file:
    one_ticker_arr = ticker_exhange_file[key]
    cik = one_ticker_arr['cik_str']
    new_dict[cik] = [one_ticker_arr['ticker'], one_ticker_arr['title']]

with open('cik_to_ticker.json', 'w') as file:
    json.dump(new_dict, file)

print(ticker_exhange_file['0'].keys())
'''

'''
# Working Capital calculation
            current_assets = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD']; current_assets = current_assets[len(current_assets)-1]['val']
            current_liabilities = posts['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD']; current_liabilities = current_liabilities[len(current_liabilities)-1]['val']
            working_capital = current_assets - current_liabilities
# Retained Earnings calculation
            retained_earnings = posts['facts']['us-gaap']['RetainedEarningsAccumulatedDeficit']['units']['USD']; retained_earnings = retained_earnings[len(retained_earnings)-1]['val']
# Market value of Equity to Book calculation
            shares_outstanding = posts['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']; shares_outstanding = shares_outstanding[len(shares_outstanding)-1]['val']
            # Getting current share_price form Yahoo Finance API
            try:
                with open('cik_to_ticker.json', 'r') as f:
                    ticker_exhange_file = json.load(f)
                ticker = ticker_exhange_file[cik][0]
                shares_price = yf.Ticker(ticker).info.get('currentPrice')
            except:
                return None

            MVoE = shares_outstanding * shares_price
            MVoE_to_book = MVoE / total_assets

            # AT calculation
            sales = posts['facts']['us-gaap']['SalesRevenueNet']['units']['shares']; sales = sales[len(sales)-1]['val']
            AT = sales / total_assets

            Z_score = (1.2 * working_capital) + (1.4 * retained_earnings) + (3.3 * ROA) + (0.6 * MVoE_to_book) + (0.999 * AT)
            return Z_score
'''