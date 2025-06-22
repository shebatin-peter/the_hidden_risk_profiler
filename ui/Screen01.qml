/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls


Rectangle {
    width: 800
    height: 600

    color: "#EAEAEA"

    Text {
        width: 377
        height: 80
        text: qsTr("Hello Interface")
        font.pointSize: 60
        anchors.verticalCenterOffset: -250
        anchors.horizontalCenterOffset: -150
        anchors.centerIn: parent
        font.family: Qt.font({family: Qt.application.font.family, pixelSize: Qt.application.font.pixelSize})
    }

    ListView {
        id: listView
        x: 117
        y: 121
        width: 448
        height: 918
        model: ListModel {
            ListElement {
                name: "Red"
                colorCode: "red"
            }

            ListElement {
                name: "Green"
                colorCode: "green"
            }

            ListElement {
                name: "Blue"
                colorCode: "blue"
            }

            ListElement {
                name: "White"
                colorCode: "white"
            }
        }
        delegate: Row {
            spacing: 5
            Rectangle {
                width: 100
                height: 20
                color: colorCode
            }

            Text {
                width: 100
                text: name
            }
        }
    }
}
