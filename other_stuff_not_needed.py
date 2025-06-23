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