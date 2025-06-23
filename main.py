import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
import json
from data_processing import get_industry_from_cik, get_posts

with open('cik_list.json', 'r') as f:
    cik_list = json.load(f)

class CompanyReceiver(QObject):
        selectionChanged = Signal(dict)
        analysisReady = Signal(str, str, str)
        filterChanged = Signal('QVariant')

        def __init__(self, cik_list):
            super().__init__()
            self.selected_company = None
            self.full_company_list = cik_list
            self.filtered_list = []
            QTimer.singleShot(0, lambda: self.filterChanged.emit(self.full_company_list))

        @Slot(dict)
        def handleSelection(self, company):
            print("Selected in QML:", company)
            self.selected_company = company  # ← Save for access later
            self.selectionChanged.emit(company)

        def get_selected_cik(self):
            return self.selected_company["cik"] if self.selected_company else None

        def get_selected_name(self):
            return self.selected_company["name"] if self.selected_company else None

        @Slot(str)
        def filterCompaniesBySIC(self, sic_code):
            print("📌 Filter companies with SIC:", sic_code)
            # Apply your filtering logic here
            filtered_list = []
            checked_num = 0
            for c in cik_list:
                sic_gotten = get_industry_from_cik(c['cik'])['sic']
                if sic_gotten is not None and sic_gotten == sic_code:
                    filtered_list.append(c)
                    print(f'{len(filtered_list)} companies were found')
                else:
                    checked_num += 1
                if len(filtered_list) == 3:
                    break
                elif checked_num == 100 and len(filtered_list) > 0:
                    print('TOO MUCH companies were checked, but there is some')
                    break
                elif checked_num == 100 and len(filtered_list) == 0:
                    filtered_list = filtered_list
                    print('Filtered companies were checked, but there is none')
                    break
            self.filtered_list = filtered_list
            self.filterChanged.emit(self.filtered_list)

        def get_filtered_companies(self):
            return self.filtered_list

        @Slot()
        def resetFilter(self):
            print('Reset filter button was pressed!')
            self.filterChanged.emit(self.full_company_list)


app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

receiver = CompanyReceiver(cik_list)
engine.rootContext().setContextProperty("CompanyReceiver", receiver)

def on_company_selected(company):
    print("Algorithm triggered for:", company["name"])
    cik = company['cik']
    print(cik)
    if cik is not None:
        posts = get_posts(cik)
        if posts is None:
            receiver.analysisReady.emit(company['name'], 'No Information', 'No Information')
        else:
            posts_ind = get_industry_from_cik(cik)
            company_name = posts['entityName']
            company_industry = posts_ind['industry']
            company_filter = posts_ind['filter']
            try:
                company_value_of_assets = str(posts['facts']['us-gaap']['Assets']['units']['USD'][len(posts['facts']['us-gaap']['Assets']['units']['USD']) - 1]['val'])
                company_value_of_assets = f"{int(company_value_of_assets):,}"
            except:
                company_value_of_assets = 'No Information'
            # sic_info = get_sic_from_cik(company_number)
            if posts and company_industry is not None:
                print(f'Name of company - {company_name}\nIndustry - {company_industry}\nValue of assets in USD - {company_value_of_assets}')
                receiver.analysisReady.emit(company_name, company_industry, company_value_of_assets)
            else:
                receiver.analysisReady.emit(company['name'], 'No Information', 'No Information')
    else:
        print('CIK is None - Does not work :(')

receiver.selectionChanged.connect(on_company_selected)

# 🔧 Tell QML where to look for imports (like Constants.qml if needed)
project_dir = os.path.dirname(__file__)
engine.addImportPath(os.path.join(project_dir, "shared", "designer"))

# Make the data available to QML
#engine.rootContext().setContextProperty("cikModel", cik_list)

with open("sic_codes.json", "r") as f:
    sic_data = json.load(f)

engine.rootContext().setContextProperty("sicModel", sic_data)


# 🔧 Load the actual app window (your QML)
qml_file = os.path.join(project_dir, "ui", "App.qml")
engine.load(QUrl.fromLocalFile(qml_file))

# Exit if it failed
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
