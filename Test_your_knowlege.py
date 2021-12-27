import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import json
import pandas as pd
import random

#Import the "allquestions" file
f = open("allquestions.json", "r")
data = json.loads(f.read())
df = pd.DataFrame(data["results"])

#initiallize App and set configuration
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Knowledge Test")
window.setFixedWidth(1000)
window.setStyleSheet("background: #1C2833;")

def prepare_questions(i):
    question = df["question"][i]
    correct = df["correct_answer"][i]
    wrong = df["incorrect_answers"][i]

    # correcting bad format in JSON questions
    correcting_questions = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "less than SYMBOL"),
        ("&gt;", "greater than SYMBOL")
    ]

    for format in correcting_questions:
        question = question.replace(format[0], format[1])
        correct = correct.replace(format[0], format[1])

    for format in correcting_questions:
        wrong = [char.replace(format[0], format[1]) for char in wrong]


    variables["question"].append(question)
    variables["correct"].append(correct)

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    variables["answer1"].append(all_answers[0])
    variables["answer2"].append(all_answers[1])
    variables["answer3"].append(all_answers[2])
    variables["answer4"].append(all_answers[3])

    print(all_answers)

variables = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "index": []
}

#Dictionary of widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}

#initialliza grid layout
grid = QGridLayout()

#hide all existing widgets and erase them from the global dictionary
def reset_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def reset_variables():
    for var in variables:
        if variables[var] != []:
            for i in range(0, len(variables[var])):
                variables[var].pop()


    variables["index"].append(random.randint(0, 49))
    variables["score"].append(0)

def start_game():
    reset_widgets()
    reset_variables()
    prepare_questions(variables["index"][-1])
    window2()

def make_buttons(answer, l_margin, r_margin):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+

        "border: 4px solid '#21bf96';" +
        "color: white;" +
        "font-family: 'arial';" +
        "font-size: 16px;" +
        "border-radius: 25px;" +
        "padding: 15px 0;" +
        "margin-top: 20px;}" +

        "*:hover{background: '#21bf96';}"
    )

    print(variables["correct"][-1])
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):
    if btn.text() == variables["correct"][-1]:
        print(btn.text() + " is correct")
        temp_score = variables["score"][-1]
        variables["score"].pop()
        variables["score"].append(temp_score + 10)
        variables["index"].pop()
        variables["index"].append(random.randint(0,49))
        prepare_questions(variables["index"][-1])
        print(variables["correct"][-1])
        widgets["score"][-1].setText(str(variables["score"][-1]))
        widgets["question"][0].setText(variables["question"][-1])
        widgets["answer1"][0].setText(variables["answer1"][-1])
        widgets["answer2"][0].setText(variables["answer2"][-1])
        widgets["answer3"][0].setText(variables["answer3"][-1])
        widgets["answer4"][0].setText(variables["answer4"][-1])
        if variables["score"][-1] == 100:
            reset_widgets()
            window3()
    else:
        reset_widgets()
        window4()


#=============WINDOW 1====================
# Window 1 contains the MCQ logo and "Lets Play" button to start the game

def window1():
    reset_widgets()

    #logo settings
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    #button settings
    button = QPushButton("Let's Play")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#21bf96';" +
        "border-radius: 45px;" +
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 25px 0;" +
        "margin: 100px 350px;}" +
        "*:hover{background: '#21bf96';}"
    )

    button.clicked.connect(start_game)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


#=============WINDOW 2====================
# Window 2 contains score counter that increments 10 points for every correct questions and 4 questions

def window2():
    #score settings
    score = QLabel(str(variables["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(

        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 15px 10px;" +
        "margin: 20px 200px;" +
        "background: '#C00000';" +
        "border: 1px solid '#C00000';" +
        "border-radius: 35px;"

    )
    widgets["score"].append(score)

    #question banner settings
    question = QLabel(variables["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: 'arial';" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"

    )
    widgets["question"].append(question)

    #answer buttons settings
    button1 = make_buttons(variables["answer1"][-1], 85, 5)
    button2 = make_buttons(variables["answer2"][-1], 5, 85)
    button3 = make_buttons(variables["answer3"][-1], 85, 5)
    button4 = make_buttons(variables["answer4"][-1], 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    #logo settings
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 75px; margin-bottom: 30px;")
    widgets["logo"].append(logo)

    #place widget on the grid
    grid.addWidget(widgets["score"][-1], 0, 0)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1,2)

#=============WINDOW 3====================
# Window 3 is called after 100 points score (10 correct questions)

def window3():
    #congradulations banner
    message = QLabel("Congradulations! You\nhave amazing knowledge!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'arial'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score banner
    score = QLabel("100")
    score.setStyleSheet("font-size: 100px; color: #21bf96; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #"Do you want to play again" banner
    message2 = QLabel("Do you want to play again?")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'arial'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #"Play again" button
    button = QPushButton('PLAY AGAIN')
    button.setStyleSheet(
        "*{background:'#21bf96'; padding:25px 0px; border: 1px solid '#21bf96'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#21bf96';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(window1)

    widgets["button"].append(button)

    #logo banner
    pixmap = QPixmap('logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

#=============WINDOW 4====================
# Window for is called after an incorrect answer

def window4():
    #sorry you lost banner
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'arial'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score banner
    score = QLabel(str(variables["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button banner
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{padding: 25px 0px;" +
        "background: '#C00000';" +
        "color: 'white';" +
        "font-family: 'Arial';" +
        "font-size: 35px;" +
        "border-radius: 40px;" +
        "margin: 10px 350px;}" +
        "*:hover{background: '#C00000';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(window1)

    widgets["button"].append(button)

    #logo banner
    pixmap = QPixmap('logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place banner on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)



#start of the app by calling window1
window1()

window.setLayout(grid)

window.show()
sys.exit(app.exec()) #terminate the app