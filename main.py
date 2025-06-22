import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

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
