import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Slot, Signal
import json
from data_processing import get_industry_from_cik, get_posts

class CompanyReceiver(QObject):
        selectionChanged = Signal(dict)
        analysisReady = Signal(str, str, str)

        def __init__(self):
            super().__init__()
            self.selected_company = None

        @Slot(dict)
        def handleSelection(self, company):
            print("Selected in QML:", company)
            self.selected_company = company  # ← Save for access later
            self.selectionChanged.emit(company)

        def get_selected_cik(self):
            return self.selected_company["cik"] if self.selected_company else None

        def get_selected_name(self):
            return self.selected_company["name"] if self.selected_company else None


app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

receiver = CompanyReceiver()
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

with open('cik_list.json', 'r') as f:
    cik_list = json.load(f)

# Make the data available to QML
engine.rootContext().setContextProperty("cikModel", cik_list)

# 🔧 Load the actual app window (your QML)
qml_file = os.path.join(project_dir, "ui", "App.qml")
engine.load(QUrl.fromLocalFile(qml_file))

# Exit if it failed
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
