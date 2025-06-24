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

    property string companyName: ""
    property string companyIndustry: ""
    property string companyAssets: ""
    property string companyFScore: ""
    property string companyFScoreSign: ""
    property string companySynergy: ""
    property string companySynergySign: ""
    property var cikModel: []

    property var selectedCik: null

    Component.onCompleted: {
        CompanyReceiver.resetFilter()
    }

    Text {
        width: 377
        height: 80
        x: 90
        y: 17
        text: qsTr("Choose Target Company")
        font.pointSize: 52
        font.family: Qt.font({family: Qt.application.font.family, pixelSize: Qt.application.font.pixelSize})
    }

    Connections {
        target: CompanyReceiver
        function onAnalysisReady(displayable_data) {
            console.log("🟢 Analysis received:", displayable_data[0], displayable_data[1], displayable_data[2], displayable_data[3], displayable_data[4])
            companyName = displayable_data[0]
            companyIndustry = displayable_data[1]
            companyAssets = displayable_data[2]
            companyFScore = displayable_data[3]
            companyFScoreSign = displayable_data[4]
            companySynergy = displayable_data[5]
            companySynergySign = displayable_data[6]
        }

        function onFilterChanged(filtered) {
            console.log('Filtered list received: ', filtered.lenght)
            cikModel = filtered
        }
    }

     ListView {
        id: companyList
        x: 117
        y: 120
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
        width: 480
        height: 125
        x: 650
        y: 115
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

            Text {
                text: companyFScore.length > 0 ? companyFScoreSign + "F-score: " + companyFScore + "        " + companySynergySign + "Synergy Scoring: " + companySynergy: "F-score: -              Synergy Scoring: -"
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
        x: 665
        y: 55

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

    Button {
        text: 'Return to the Acquirer Info page'
        onClicked: appStack.replace('StartScreen.qml')
        width: 250
        height: 40
        x: 850
        y: 55

        background: Rectangle {
            color: 'white'
            border.color: 'black'
            border.width: 1
            radius: 4
        }

        contentItem: Text {
            text: qsTr('Return to the Acquirer Info page')
            color: 'black'
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Text {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        text: 'Acquirer SIC code: ' + CompanyReceiver.get_acquirer_sic_code() + "   Acquirer's Total Assets number: " + CompanyReceiver.get_acquirer_assets()
        font.pointSize: 12
        color: "blue"
        padding: 10
    }
}
