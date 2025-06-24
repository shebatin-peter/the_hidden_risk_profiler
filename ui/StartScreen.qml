import QtQuick
import QtQuick.Controls


Item {
    property bool chosenSicCode: false
    anchors.fill: parent

    Rectangle {
        color: "#EAEAEA"
        anchors.fill: parent

        Text {
            width: 377
            height: 80
            x: 90
            y: 17
            text: qsTr("Enter Acquirer Info")
            font.pointSize: 52
            font.family: Qt.font({family: Qt.application.font.family, pixelSize: Qt.application.font.pixelSize})
        }

        Column {
            x: 90
            y: 100
            anchors.margins: 10
            spacing: 10

            Text {
                text: "Enter Acquirer's Total Assets number"
                font.pointSize: 14
            }

            TextField {
                id: assetField
                width: 250
                color: 'black'
                background: Rectangle {
                    border.color: 'black'
                    border.width: 1
                    radius: 4
                }
            }

            Text {
                text: assetField.text.match(/^\d+$/) === null && assetField.text !== ""
                        ? "Please enter a valid whole number"
                        : ""
                color: "red"
                font.pointSize: 12
            }
        }

        Column {
            x: 500
            y: 100
            width: parent.width * 0.5
            height: 600
            anchors.margins: 10
            spacing: 10

            Text {
                text: "Select Acquirer's SIC number"
                font.pointSize: 14
            }

            ListView {
                id: sicListStartPage
                width: parent.width
                height: 500
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

                        Text {
                            text: modelData.sic_code; font.bold: true
                        }
                        Text {
                            text: modelData.industry; font.pointSize: 12
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            sicListStartPage.currentIndex = index
                            chosenSicCode = true
                            console.log('Selected index now:', modelData.sic_code)
                        }
                    }
                }
            }
        }

        Button {
            text: 'Continue'
            enabled: assetField.text.match(/^\d+$/) !== null && sicListStartPage.currentIndex >= 0 && chosenSicCode
            onClicked: {
                const selected = sicModel[sicListStartPage.currentIndex]
                CompanyReceiver.setAcquirerInfo(assetField.text, selected['sic_code'])
                appStack.push('Screen01.qml')
            }
            width: 150
            height: 40
            x: 1025
            y: 645

            background: Rectangle {
                color: 'white'
                border.color: 'black'
                border.width: 1
                radius: 4
            }

            contentItem: Text {
                text: qsTr('Continue')
                color: 'black'
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}