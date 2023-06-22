#!/usr/bin/env python3

import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

frage1 = ("Mehrmals am Tag",
          "Einmal am Tag",
          "Einmal pro Woche",
          "Seltener als einmal pro Woche",
          "Ich nutze Instagram nicht",
          )
frage2 = (
        "mehr als 2 Stunden täglich",
        "30 Minuten bis 2 Stunden",
        "15 bis 20 Minuten",
        "Weniger als 15 Minuten"
          )
frage3 = ("häufig",
          "regelmäßig",
          "selten",
          "nie"
          )

frage4 = frage3

frage5 = (
    "Ja, positiv",
    "Ja, negativ",
    "Nein, es hat keinen Einfluss",
)
frage6 = (
    "Mehrmals pro Woche",
    "Einmal pro Woche",
    "Einmal pro Monat",
    "Selten bis nie"
)
frage7 = frage6

frage8 = frage5

frage9 = frage6

frage10 = (
    "Ja, häufig",
    "Ja, manchmal",
    "Nein, nie"
)

frage11 = frage6
frage12 = frage6
frage13 = frage6
frage14 = frage6

frage15 = (
    "Signifikant verbessert",
    "Leicht verbessert",
    "Leicht verschlechtert",
    "Signifikant verschlechtert"
)

frage16 = (
    "Signifikant beeinflusst",
    "Leicht beeinflusst",
    "Kaum beeinflusst",
    "Nicht beeinflusst",
)
fragen = [frage1, frage2, frage3, frage4, frage5, frage6,
          frage7, frage8, frage9, frage10, frage11, frage12,
          frage13, frage14, frage15, frage16]


def output(arr, questionNum, total):
    count = 0
    text = ""
    for i in arr:
        text += str(fragen[questionNum][count]) + " →  [" + str(i) + "] > "
        text += " Prozent:  " + format((i/total)*100, ".2f") + "%\n"
        count += 1

    return text


def checkIfUse(string, num):
    tup = fragen[num]
    arrSol = []
    for i in tup:
        if string.strip().lower() == i.strip().lower():
            arrSol.append(1)
        else:
            arrSol.append(0)

    return arrSol


def add(questionNum, colToCheck, row, use):
    if questionNum >= 0:
        temp = checkIfUse(row[colToCheck], questionNum)
        for i in range(0, len(temp)):
            use[i] += temp[i]


def onClick(window, layout, labels, text):
    with open("umfrage.csv", newline='') as file:
        reader = csv.reader(file, delimiter=",")
        count = 0
        masc, fem, div = 0, 0, 0
        mascUse, femUse, divUse = [], [], []
        questionNum = int(text) - 1
        if questionNum > 15 or questionNum < 0:

            labels[0].setText("Kein Richtiger Input")
            labels[1].setText("")
            labels[2].setText("")
            labels[3].setText("")
            return
        colToCheck = questionNum + 4
        for i in fragen[questionNum]:
            mascUse.append(0)
            femUse.append(0)
            divUse.append(0)
        for row in reader:
            if count == 0:
                count = 1
                labels[0].setText(row[colToCheck])
            else:
                text = row[3]
                if text.startswith("M"):
                    masc += 1
                    add(questionNum, colToCheck, row, mascUse)

                elif text.startswith("W"):
                    fem += 1
                    add(questionNum, colToCheck, row, femUse)

                elif text.startswith("D"):
                    div += 1
                    add(questionNum, colToCheck, row, divUse)

    # Männlich:
    textM = "------------------------------------------------\n"
    textM += "Gesamte Anzahl männlicher Befragter: " + str(masc) + "\n"
    textM += "------------------------------------------------\n"
    textM += output(mascUse, questionNum, masc)
    textM += "------------------------------------------------"
    # Weiblich
    textF = "------------------------------------------------\n"
    textF += "Gesamte Anzahl weiblicher Befragter: " + str(fem) + "\n"
    textF += "------------------------------------------------\n"
    textF += output(femUse, questionNum, fem)
    textF += "------------------------------------------------"
    # Divers
    textD = "------------------------------------------------\n"
    textD += "Gesamte Anzahl diverser Befragter: " + str(div) + "\n"
    textD += "------------------------------------------------\n"
    textD += output(divUse, questionNum, div)
    labels += "------------------------------------------------"
    labels[1].setText(textM)
    labels[2].setText(textF)
    labels[3].setText(textD)


def main():
    app = QApplication([])
    window = QWidget()
    labels = []

    layout = QVBoxLayout()
    label = QLabel(window)
    label.setText("Welche Frage Willst du nach Geschlecht Analysieren")

    label.setFont(QFont("Calibri", 16))
    inputBox = QLineEdit()
    for i in labels:
        layout.removeWidget(i)
        i.deleteLater()
    labels = []
    button = QPushButton("Start")
    labelQuestion = QLabel(window)
    label1 = QLabel(window)
    label2 = QLabel(window)
    label3 = QLabel(window)
    labelQuestion.setFont(QFont("Calibri", 14))
    label1.setFont(QFont("Calibri", 12))
    label2.setFont(QFont("Calibri", 12))
    label3.setFont(QFont("Calibri", 12))
    labels.append(labelQuestion)
    labels.append(label1)
    labels.append(label2)
    labels.append(label3)

    button.clicked.connect(lambda: onClick(window, layout, labels, inputBox.text()))

    for i in labels:
        layout.addWidget(i)

    layout.addWidget(label)
    layout.addWidget(inputBox)
    layout.addWidget(button)
    window.setLayout(layout)

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
