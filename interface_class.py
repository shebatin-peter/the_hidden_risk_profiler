from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
from data_processing import *

# Main Interface class
class CompanyReceiver(QObject):
        selectionChanged = Signal(dict)
        analysisReady = Signal(list)
        filterChanged = Signal('QVariant')

        def __init__(self, cik_list):
            super().__init__()
            self.cik_list = cik_list
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
            for c in self.cik_list:
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