/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls



Rectangle {
    width: 1200
    height: 700

    color: "#EAEAEA"

    property string companyName: "-"
    property string companyIndustry: "-"
    property string companyAssets: "-"

    property var selectedCik: null

    Text {
        width: 377
        height: 80
        x: 117
        y: 20
        text: qsTr("Hello Interface")
        font.pointSize: 60
        font.family: Qt.font({family: Qt.application.font.family, pixelSize: Qt.application.font.pixelSize})
    }

    Connections {
        target: CompanyReceiver

        function onAnalysisReady(name, industry, assets) {
            console.log("🟢 Analysis received:", name, industry, assets)
            companyName = name
            companyIndustry = industry
            companyAssets = assets
        }
    }

     ListView {
        id: listView
        x: 117
        y: 121
        width: 448
        height: 918
        spacing: 8
        model: cikModel

        delegate: Rectangle {
            width: parent.width
            height: 50
            color: ListView.isCurrentItem ? "#d0eaff" : "#ffffff"
            border.color: "#cccccc"
            border.width: 1
            radius: 6

            Row {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 20

                Text {
                    text: modelData.name
                    font.bold: true
                    font.pointSize: 14
                }

                Text {
                    text: modelData.cik
                    font.pointSize: 12
                    color: "gray"
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    listView.currentIndex = index
                    selectedCik = modelData
                    CompanyReceiver.handleSelection(modelData)
                }
            }
        }
    }

    Rectangle {
        width: 300
        height: 100
        x: 700
        y: 120
        color: "#f9f9f9"
        radius: 6
        border.color: "#bbb"
        border.width: 1

        Column {
            anchors.fill: parent
            spacing: 10

            Text {
                text: companyName.length > 0 ? "Name: " + companyName : "No company selected"
                font.pointSize: 14
            }

            Text {
                text: companyIndustry.length > 0 ? "Industry: " + companyIndustry : "Industry: -"
                font.pointSize: 14
            }

            Text {
                text: companyAssets.length > 0 ? "Value of assets in USD: " + companyAssets : "Value of assets in USD: -"
                font.pointSize: 14
            }
        }
    }

    Text {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        text: selectedCik ? "Selected: " + selectedCik.name + " (" + selectedCik.cik + ")" : "No company selected"
        font.pointSize: 12
        color: "blue"
        padding: 10
    }
}
