import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
import json
from data_processing import *
from interface_class import CompanyReceiver

with open('cik_list.json', 'r') as f:
    cik_list = json.load(f)

with open("sic_codes.json", "r") as f:
    sic_data = json.load(f)

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

receiver = CompanyReceiver(cik_list)
engine.rootContext().setContextProperty("CompanyReceiver", receiver)
engine.rootContext().setContextProperty("sicModel", sic_data)

# Function of displaying information on the Text Block about the selected company from the list
def on_company_selected(company):
    print("Algorithm triggered for:", company["name"])
    cik = company['cik']
    displayable_data = get_displayable_data(cik, company['name'])
    if displayable_data is None:
        print('CIK is None - Does not work :(')
    else:
        receiver.analysisReady.emit(displayable_data)

receiver.selectionChanged.connect(on_company_selected)

# 🔧 Tell QML where to look for imports (like Constants.qml if needed)
project_dir = os.path.dirname(__file__)
engine.addImportPath(os.path.join(project_dir, "shared", "designer"))

# 🔧 Load the actual app window (your QML)
qml_file = os.path.join(project_dir, "ui", "App.qml")
engine.load(QUrl.fromLocalFile(qml_file))

# Exit if it failed
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
