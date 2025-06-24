import QtQuick
import QtQuick.Controls


Window {
    width: 1200
    height: 700
    visible: true
    title: "The Hidden Risk Profiler"

    StackView {
        id: appStack
        anchors.fill: parent
        initialItem: StartScreen {}
    }
}

