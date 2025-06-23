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
    property var cikModel: []

    property var selectedCik: null

    Text {
        width: 377
        height: 80
        x: 101
        y: 17
        text: qsTr("The Hidden Risk Profiler")
        font.pointSize: 52
        font.family: Qt.font({family: Qt.application.font.family, pixelSize: Qt.application.font.pixelSize})
    }

    Connections {
        target: CompanyReceiver
        function onAnalysisReady(displayable_data) {
            console.log("🟢 Analysis received:", displayable_data[0], displayable_data[1], displayable_data[2])
            companyName = displayable_data[0]
            companyIndustry = displayable_data[1]
            companyAssets = displayable_data[2]
        }

        function onFilterChanged(filtered) {
            console.log('Filtered list received: ', filtered.lenght)
            cikModel = filtered
        }
    }

     ListView {
        id: companyList
        x: 117
        y: 121
        width: 448
        height: 525
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
                    companyList.currentIndex = index
                    selectedCik = modelData
                    CompanyReceiver.handleSelection(modelData)
                }
            }
        }
    }

    Rectangle {
        width: 400
        height: 100
        x: 675
        y: 120
        color: "#f9f9f9"
        radius: 6
        border.color: "#bbb"
        border.width: 1

        Column {
            anchors.fill: parent
            anchors.margins: 10
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

    ListView {
        id: sicList
        x: 650
        y: 250
        width: parent.width * 0.4
        height: 450
        model: sicModel
        spacing: 6
        clip: true

        delegate: Rectangle {
            width: parent.width
            height: 40
            color: ListView.isCurrentItem ? "#cceeff" : "#ffffff"
            border.color: "#bbb"
            border.width: 1
            radius: 4

            Row {
                anchors.centerIn: parent
                spacing: 10

                Text { text: modelData.sic_code; font.bold: true }
                Text { text: modelData.industry; font.pointSize: 12 }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    sicList.currentIndex = index
                    console.log("Selected SIC:", modelData.sic_code)
                    CompanyReceiver.filterCompaniesBySIC(modelData.sic_code)
                }
            }
        }
    }

    Button {
        text: 'Reset Filter'
        onClicked: CompanyReceiver.resetFilter()
        width: 150
        height: 40
        x: 775
        y: 60

        background: Rectangle {
            color: 'white'
            border.color: 'black'
            border.width: 1
            radius: 4
        }

        contentItem: Text {
            text: qsTr('Reset Filter')
            color: 'black'
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
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
