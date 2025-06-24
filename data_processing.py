import json
import requests
from bs4 import BeautifulSoup

# Function of conducting a Synergy Scoring test for the chosen company given Acquirer info
def conduct_synergy_scoring(sic_chosen, company_ta, total_assets_Ac, sic_Ac, F_score):
    final_synergy = 0
    total_assets_Ac = int(total_assets_Ac)

    # 1. Industry Match - comparing SICs : 40 points out 100
    if (sic_chosen and sic_Ac) is None:
        pass # Nothing
    elif sic_chosen == sic_Ac:
        final_synergy += 40 # Exact industry
    elif sic_chosen[:2] == sic_Ac[:2]:
        final_synergy += 25 # Same broad group industry

    # 2. Asset Size Compatibility - comparing target and Acquirer's assets units : 30 points out 100
    if total_assets_Ac <= 0 or company_ta <= 0:
        pass # Nothing
    elif 0.5 <= company_ta / total_assets_Ac <= 2:
        final_synergy += 30 # Close size
    elif 0.25 <= company_ta / total_assets_Ac < 0.5 or 2 < company_ta / total_assets_Ac <= 4:
        final_synergy += 15 # Significant difference

    # 3. F-score Performance - consider the result of previously conducted F-score test on target company : 30 points out 100
    if F_score is None:
        pass # Nothing
    else:
        final_synergy += int((F_score / 9) * 30) # Scaling the result to the 30 points size

    return final_synergy

# Function of conducting a Piotroski F-score for the chosen company
def conduct_piotroski_scoring(cik):
    if cik is not None:
        posts = get_posts(cik)
        if posts is None:
            return None
        else:
            # 1, 2 Profitability check: ROA > 0 and ROA increased
            successful_tests = 0
            points = 0
            try:
                # ROA calculation this year
                total_assets = posts['facts']['us-gaap']['Assets']['units']['USD']; total_assets = total_assets[len(total_assets)-1]['val']
                current_year = posts['facts']['us-gaap']['Assets']['units']['USD'][-1]['fy']
                try:
                    EBIT = posts['facts']['us-gaap']['OperatingIncomeLoss']['units']['USD']; EBIT = EBIT[len(EBIT)-1]['val']
                except:
                    EBIT = posts['facts']['us-gaap']['NetIncomeLoss']['units']['USD']; EBIT = EBIT[len(EBIT) - 1]['val']
                ROA_current_year = EBIT / total_assets
                successful_tests += 1
                if ROA_current_year > 0:
                    points += 1

                # ROA calculation last year
                total_assets = posts['facts']['us-gaap']['Assets']['units']['USD'];
                l = 1
                while(total_assets[len(total_assets) - l]['fy'] == current_year):
                    l += 1
                total_assets = total_assets[len(total_assets) - l]['val']
                try:
                    EBIT = posts['facts']['us-gaap']['OperatingIncomeLoss']['units']['USD'];
                    EBIT = EBIT[len(EBIT) - l]['val']
                except:
                    EBIT = posts['facts']['us-gaap']['NetIncomeLoss']['units']['USD'];
                    EBIT = EBIT[len(EBIT) - l]['val']
                ROA_last_year = EBIT / total_assets
                successful_tests += 1
                if ROA_current_year > ROA_last_year:
                    points += 1
            except:
                pass

            # 3, 4 Profitability Check: CFO > 0 and CFO > Net Income
            try:
                try:
                    NetCashFlows = posts['facts']['us-gaap']['NetCashProvidedByUsedInOperatingActivitiesContinuingOperations']['units']['USD']; NetCashFlows = NetCashFlows[len(NetCashFlows)-1]['val']
                except:
                    NetCashFlows = posts['facts']['us-gaap']['NetCashProvidedByUsedInOperatingActivities']['units']['USD']; NetCashFlows = NetCashFlows[len(NetCashFlows)-1]['val']
                successful_tests += 1
                if NetCashFlows > 0:
                    points += 1

                try:
                    Net_Income = posts['facts']['us-gaap']['NetIncomeLoss']['units']['USD']; Net_Income = Net_Income[len(Net_Income)-1]['val']
                except:
                    Net_Income = posts['facts']['us-gaap']['ProfitLoss']['units']['USD']; Net_Income = Net_Income[len(Net_Income) - 1]['val']
                successful_tests += 1
                if Net_Income > Net_Income:
                    points += 1
            except:
                pass

            # 5 Leverage, Liquidity & Source of Funds check: Lower Leverage
            try:
                total_assets_current = posts['facts']['us-gaap']['Assets']['units']['USD']; total_assets = total_assets[len(total_assets) - 1]['val']
                current_year = posts['facts']['us-gaap']['Assets']['units']['USD'][-1]['fy']
                total_assets_previous = posts['facts']['us-gaap']['Assets']['units']['USD'];
                l = 1
                while (total_assets_previous[len(total_assets_previous) - l]['fy'] == current_year):
                    l += 1
                total_assets_previous = total_assets_previous[len(total_assets_previous) - l]['val']

                try:
                    leverage_current = posts['facts']['us-gaap']['LongTermDebtNoncurrent']['units']['USD']; leverage_current = leverage_current[len(leverage_current) - 1]['val'] / total_assets_current
                    leverage_previous = posts['facts']['us-gaap']['LongTermDebtNoncurrent']['units']['USD'];
                    l = 1
                    while (leverage_previous[len(leverage_previous) - l]['fy'] == current_year):
                        l += 1
                    leverage_previous = leverage_previous[len(leverage_previous) - l]['val'] / total_assets_current
                except:
                    leverage_current = posts['facts']['us-gaap']['LongTermDebt']['units']['USD']; leverage_current = leverage_current[len(leverage_current) - 1]['val'] / total_assets_current
                    leverage_previous = posts['facts']['us-gaap']['LongTermDebt']['units']['USD'];
                    l = 1
                    while (leverage_previous[len(leverage_previous) - l]['fy'] == current_year):
                        l += 1
                    leverage_previous = leverage_previous[len(leverage_previous) - l]['val'] / total_assets_current
                successful_tests += 1
                if leverage_current < leverage_previous:
                    points += 1
            except:
                pass

            # 6 Leverage, Liquidity & Source of Funds check: Lower Leverage
            try:
                current_assets_now = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD']; current_assets_now = current_assets_now[len(current_assets_now) - 1]['val']
                current_liabilities_now = posts['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD']; current_liabilities_now = current_liabilities_now[len(current_liabilities_now) - 1]['val']
                current_year = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD'][-1]['fy']
                current_assets_previous = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD'];
                l = 1
                while (current_assets_previous[len(current_assets_previous) - l]['fy'] == current_year):
                    l += 1
                current_assets_previous = current_assets_previous[len(current_assets_previous) - l]['val']
                current_liabilities_previous = posts['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'];
                l = 1
                while (current_liabilities_previous[len(current_liabilities_previous) - l]['fy'] == current_year):
                    l += 1
                current_liabilities_previous = current_liabilities_previous[len(current_liabilities_previous) - l]['val']
                current_ratio_now = current_assets_now / current_liabilities_now
                current_ratio_previous = current_assets_previous / current_liabilities_previous
                successful_tests += 1
                if current_ratio_now > current_ratio_previous:
                    points += 1
            except:
                pass

            # 7 Leverage, Liquidity & Source of Funds check: No new Equity
            try:
                shares_outstanding_current = posts['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']; shares_outstanding_current = shares_outstanding_current[len(shares_outstanding_current) - 1]['val']
                current_year = posts['facts']['us-gaap']['EntityCommonStockSharesOutstanding']['units']['USD'][-1]['fy']
                shares_outstanding_previous = posts['facts']['us-gaap']['EntityCommonStockSharesOutstanding']['units']['USD'];
                l = 1
                while (shares_outstanding_previous[len(shares_outstanding_previous) - l]['fy'] == current_year):
                    l += 1
                shares_outstanding_previous = shares_outstanding_previous[len(shares_outstanding_previous) - l]['val']
                successful_tests += 1
                if shares_outstanding_current <= shares_outstanding_previous:
                    points += 1
            except:
                pass

            # 8 Operating Efficiency check: Gross Margin improvement
            try:
                gross_profit_current = posts['facts']['dei']['GrossProfit']['units']['shares']; gross_profit_current = gross_profit_current[len(gross_profit_current) - 1]['val']
                current_year = posts['facts']['us-gaap']['GrossProfit']['units']['USD'][-1]['fy']
                gross_profit_previous = posts['facts']['us-gaap']['GrossProfit']['units']['USD'];
                l = 1
                while (gross_profit_previous[len(gross_profit_previous) - l]['fy'] == current_year):
                    l += 1
                gross_profit_previous = gross_profit_previous[len(gross_profit_previous) - l]['val']

                try:
                    revenues_current = posts['facts']['dei']['SalesRevenueNet']['units']['shares']; revenues_current = revenues_current[len(revenues_current) - 1]['val']
                    revenues_previous = posts['facts']['us-gaap']['SalesRevenueNet']['units']['USD'];
                    l = 1
                    while (revenues_previous[len(revenues_previous) - l]['fy'] == current_year):
                        l += 1
                    revenues_previous = revenues_previous[len(revenues_previous) - l]['val']
                except:
                    revenues_current = posts['facts']['dei']['Revenues']['units']['shares']; revenues_current = revenues_current[len(revenues_current) - 1]['val']
                    revenues_previous = posts['facts']['us-gaap']['Revenues']['units']['USD'];
                    l = 1
                    while (revenues_previous[len(revenues_previous) - l]['fy'] == current_year):
                        l += 1
                    revenues_previous = revenues_previous[len(revenues_previous) - l]['val']
                margin_current = gross_profit_current / revenues_current
                margin_previous = gross_profit_previous / revenues_previous
                successful_tests += 1
                if margin_current > margin_previous:
                    points += 1
            except:
                pass

            # 9 Operating Efficiency check: Asset Turnover improvement
            try:
                assets_current = posts['facts']['us-gaap']['Assets']['units']['USD']; assets_current = assets_current[len(assets_current) - 1]['val']
                current_year = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD'][-1]['fy']
                assets_previous = posts['facts']['us-gaap']['AssetsCurrent']['units']['USD'];
                l = 1
                while (assets_previous[len(assets_previous) - l]['fy'] == current_year):
                    l += 1
                assets_previous = assets_previous[len(assets_previous) - l]['val']

                try:
                    revenues_current = posts['facts']['dei']['SalesRevenueNet']['units']['shares']; revenues_current = revenues_current[len(revenues_current) - 1]['val']
                    revenues_previous = posts['facts']['us-gaap']['SalesRevenueNet']['units']['USD'];
                    l = 1
                    while (revenues_previous[len(revenues_previous) - l]['fy'] == current_year):
                        l += 1
                    revenues_previous = revenues_previous[len(revenues_previous) - l]['val']
                except:
                    revenues_current = posts['facts']['dei']['Revenues']['units']['shares']; revenues_current = revenues_current[len(revenues_current) - 1]['val']
                    revenues_previous = posts['facts']['us-gaap']['Revenues']['units']['USD'];
                    l = 1
                    while (revenues_previous[len(revenues_previous) - l]['fy'] == current_year):
                        l += 1
                    revenues_previous = revenues_previous[len(revenues_previous) - l]['val']

                asset_turnover_current = revenues_current / assets_current
                asset_turnover_previous = revenues_previous / assets_previous
                successful_tests += 1
                if asset_turnover_current > asset_turnover_previous:
                    points += 1
            except:
                pass

            # Combining results
            if successful_tests > 0:
                return round((points / successful_tests) * 9, 2)
            else:
                return None
    else:
        return None

# Function of preparing information for future display on the Text Box
def get_displayable_data(cik, company_name, total_assets_Ac, sic_Ac):
    if cik is not None:
        posts = get_posts(cik)

        if posts is None:
            return [company_name, 'No Information', 'No Information', 'Impossible to compute', '⚠️ ', 'No Synergy', '⚠️ ']
        else:
            company_info_deep = get_industry_from_cik(cik)
            company_industry = company_info_deep['industry']
            try:
                company_value_of_assets = str(posts['facts']['us-gaap']['Assets']['units']['USD'][len(posts['facts']['us-gaap']['Assets']['units']['USD']) - 1]['val'])
            except:
                # sic_info = get_sic_from_cik(company_number) # - Only for cases outside EDGAR database and has a limited amount of calls
                company_value_of_assets = None

            # Getting Z_score for this company
            F_score = conduct_piotroski_scoring(cik)
            if (posts and company_industry and F_score and company_value_of_assets) is not None:
                print(f'Name of company - {company_name}\nIndustry - {company_industry}\nValue of assets in USD - {company_value_of_assets}')
                synergy_score = conduct_synergy_scoring(company_info_deep['sic'], int(company_value_of_assets), total_assets_Ac, sic_Ac, F_score)
                company_value_of_assets = f"{int(company_value_of_assets):,}"
                if 9 >= F_score >= 8:
                    sign_f = '🟢 '
                elif F_score >= 6:
                    sign_f = '🟡 '
                elif F_score >= 4:
                    sign_f = '🟠 '
                else:
                    sign_f = '🔴 '

                if 100 >= synergy_score >= 80:
                    sign_s = '        🟢 '
                elif synergy_score >= 50:
                    sign_s = '        🟡 '
                elif synergy_score >= 20:
                    sign_s = '        🟠 '
                else:
                    sign_s = '        🔴 '
                return [company_name, company_industry, company_value_of_assets, F_score, sign_f, str(synergy_score) + '/100', sign_s]
            elif (posts and company_industry) is not None:
                return [company_name, company_industry, 'No Information', 'Impossible to compute', '⚠️ ', 'No Synergy','⚠️ ']
            else:
                return [company_name, 'No Information', 'No Information', 'Impossible to compute', '⚠️ ', 'No Synergy', '⚠️ ']
    else:
        return None

# Function of getting information about the company (industry, SIC code)
def get_industry_from_cik(cik):
    cik_number = cik
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_number}&owner=exclude&count=40"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15 (Company info@company.com)'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        info_block = soup.find("p", class_="identInfo").text
        if "SIC:" in info_block:
            sic_code = info_block.split("SIC:")[1].split("-")[0].strip()
            sic_name = info_block.split("-")[1].strip().split("State location")[0].split('\n')[0]
            return {"cik": cik_number, "sic": sic_code, "industry": sic_name}
        else:
            return {"cik": cik_number, "sic": None, "industry": None}

    except Exception as e:
        return {"cik": cik_number, "sic": None, "industry": None, "error": str(e)}

# Function of getting SIC Code via financial modeling prep - limited usage, for extreme cases only
def get_sic_from_cik(cik):
    cik_number = cik # SEC CIKs are padded to 10 digits
    url = f'https://financialmodelingprep.com/stable/sec-filings-company-search/cik?cik={cik_number}&apikey=FIYp2mJD2gLDSh9NBUJWGN7ZRdSMVdqb'

    with open('sic_info.json', 'r') as file:
        data = json.load(file)

    with open('sic_info.json', 'w') as file:
        in_data = False
        for i in range(len(data)):
            if cik_number == data[i]['cik']:
                sic_info = data[i]
                in_data = True
                break
        if in_data:
            json.dump(data, file)
            return sic_info
        else:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    sic_info = response.json()
                    data.append(sic_info)
                    json.dump(data, file)
                    return sic_info
                else:
                    print('Error:', response.status_code)
                    json.dump(data, file)
                    return None
            except requests.exceptions.RequestException as e:
                print('Error:', e)
                json.dump(data, file)
                return None

# Function of getting information about the financial state of the company - base for finance analysis
def get_posts(cik):
    url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK' + cik + '.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
