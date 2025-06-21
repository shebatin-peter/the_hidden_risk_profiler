import json
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Your Name (your@email.com)"  # replace with your info
}

def get_industry_from_cik(cik):
    cik_number = cik[3:]
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

def get_sic_from_cik(cik):
    cik_number = cik[3:]  # SEC CIKs are padded to 10 digits
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


def get_posts(cik):
    url = 'https://data.sec.gov/api/xbrl/companyfacts/' + cik + '.json'
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


def main():
    cik = 'CIK0000001800'
    posts = get_posts(cik)
    posts_ind = get_industry_from_cik(cik)
    company_name = posts['entityName']
    company_industry = posts_ind['industry']
    company_value_of_assets = posts['facts']['us-gaap']['Assets']['units']['USD'][len(posts['facts']['us-gaap']['Assets']['units']['USD']) - 1]['val']
    #sic_info = get_sic_from_cik(company_number)
    if posts and company_industry is not None:
        print(f'Name of company - {company_name}\nIndustry - {company_industry}\nValue of assets in USD - {company_value_of_assets}')

    else:
        print('Failed to fetch posts from API.')

if __name__ == '__main__':
    main()