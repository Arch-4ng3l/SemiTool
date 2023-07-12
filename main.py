# IDK How the fck i Wrote this shit it just happend somehow

import matplotlib.pyplot as plt
import csv
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QLineEdit, QPushButton, QLabel
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

mascUse, femUse, divUse = [], [], []
questionNum = -1
run = 0


def createCompononet(window, gender):
    label = QLabel(window)
    button = QPushButton("Create Graph")
    button.hide()
    button.clicked.connect(lambda: createGraph(gender))
    return (label, button)


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


def createGraph(gender):
    global questionNum
    question = fragen[questionNum]

    use = []

    if gender == "m":
        global mascUse
        use.append(mascUse)
    elif gender == "f":
        global femUse
        use.append(femUse)
    elif gender == "d":
        global divUse
        use.append(divUse)

    plt.clf()
    plt.cla()
    plt.close()
    plt.pie(
            use[0],
            labels=question,
            autopct="%1.1f%%",
    )

    plt.show()


def onClick(window, layout, labels, buttons, text):
    with open("umfrage.csv", newline='') as file:
        reader = csv.reader(file, delimiter=",")
        count = 0
        masc, fem, div = 0, 0, 0
        global mascUse, femUse, divUse
        mascUse, femUse, divUse = [], [], []
        questionNumL = 0
        try:
            questionNumL = int(text) - 1
        except ValueError:
            labels[0].setText("Kein Richtiger Input")
            return

        if questionNumL > 15 or questionNumL < 0:

            labels[0].setText("Kein Richtiger Input")
            labels[1].setText("")
            labels[2].setText("")
            labels[3].setText("")
            for i in buttons:
                i.hide()
            return

        colToCheck = questionNumL + 4
        global questionNum
        questionNum = questionNumL
        for i in fragen[questionNumL]:
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
                    add(questionNumL, colToCheck, row, mascUse)

                elif text.startswith("W"):
                    fem += 1
                    add(questionNumL, colToCheck, row, femUse)

                elif text.startswith("D"):
                    div += 1
                    add(questionNumL, colToCheck, row, divUse)

    # Männlich:
    textM = "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textM += "Gesamte Anzahl männlicher Befragter: " + str(masc) + "\n"
    textM += "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textM += output(mascUse, questionNumL, masc)
    textM += "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    # Weiblich
    textF = "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textF += "Gesamte Anzahl weiblicher Befragter: " + str(fem) + "\n"
    textF += "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textF += output(femUse, questionNumL, fem)
    textF += "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    # Divers
    textD = "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textD += "Gesamte Anzahl diverser Befragter: " + str(div) + "\n"
    textD += "-------------------------------------------------------------------------------------------------------------------------------------------\n"
    textD += output(divUse, questionNumL, div)
    textD += "-------------------------------------------------------------------------------------------------------------------------------------------\n"

    labels[1].setText(textM)
    labels[2].setText(textF)
    labels[3].setText(textD)

    for i in labels:
        i.adjustSize()

    for i in buttons:
        i.show()


def main():
    global run
    run = 0

    app = QApplication([])
    window = QWidget()
    labels = []

    layout = QVBoxLayout()
    label = QLabel(window)
    label.setText("Welche Frage Willst du nach Geschlecht Analysieren")

    label.setFont(QFont("Calibri", 12))
    inputBox = QLineEdit()
    for i in labels:
        layout.removeWidget(i)

        i.deleteLater()

    labels = []
    buttons = []

    button = QPushButton("Start")
    labelQuestion = QLabel(window)
    label1, button1 = createCompononet(window, "m")
    label2, button2 = createCompononet(window, "f")
    label3, button3 = createCompononet(window, "d")

    labelQuestion.setFont(QFont("Calibri", 16))

    label1.setFont(QFont("Calibri", 12))
    label2.setFont(QFont("Calibri", 12))
    label3.setFont(QFont("Calibri", 12))

    labels.append(labelQuestion)

    labels.append(label1)
    labels.append(label2)
    labels.append(label3)

    buttons.append(button1)
    buttons.append(button2)
    buttons.append(button3)

    button.clicked.connect(lambda: onClick(window, layout, labels, buttons, inputBox.text()))

    layout.addWidget(label1)
    layout.addWidget(button1)

    layout.addWidget(label2)
    layout.addWidget(button2)

    layout.addWidget(label3)
    layout.addWidget(button3)

    layout.addWidget(label)
    layout.addWidget(inputBox)
    layout.addWidget(button)

    window.setLayout(layout)

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
