import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    Rectangle{
        width: 200
        height: 100
        color: "lightblue"
        Text {
            anchors.centerIn: parent
            text: "Hello, World!"
            font.pointSize: 20
        }
    }
}
