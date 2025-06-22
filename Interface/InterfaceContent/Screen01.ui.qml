/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import Interface

property string companyName: "-"
property string companyIndustry: "-"
property real companyAssets: '0'

Rectangle {
    id: rectangle
    width: 1000
    height: Constants.height

    color: Constants.backgroundColor

    Text {
        width: 377
        height: 80
        text: qsTr("Hello Interface")
        font.pointSize: 60
        anchors.verticalCenterOffset: -465
        anchors.horizontalCenterOffset: -619
        anchors.centerIn: parent
        font.family: Constants.font.family
    }

    Connections {
        target: CompanyReceiver

        function onAnalysisReady(name, industry, assets) {
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

    Rectangle {
        width: parent.width * 0.45
        height: parent.height
        color: "#f9f9f9"
        radius: 6
        border.color: "#bbb"
        border.width: 1
        padding: 20

        Column {
            anchors.fill: parent
            spacing: 10

            Text {
                text: companyName.length > 0 ? "Name: " + companyName : "No company selected"
                font.pointSize: 14
            }

            Text {
                text: "Industry: " + companyIndustry
                font.pointSize: 14
            }

            Text {
                text: "Assets: $" + (companyAssets > 0 ? companyAssets.toFixed(2) : "—")
                font.pointSize: 14
            }
        }
    }
}
