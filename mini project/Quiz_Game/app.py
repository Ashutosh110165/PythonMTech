import random
from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)

app.secret_key = "mtech_python_lab_project"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    player = request.form["name"].strip()

    session["player"] = player
    session["score"] = 0
    session["current"] = 0

    question_order = list(range(len(questions)))
    random.shuffle(question_order)
    session["question_order"] = question_order

    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    if "player" not in session:
        return redirect(url_for("home"))

    current = session["current"]

    if current >= len(questions):
        return redirect(url_for("result"))

    question_index = session["question_order"][current]

    progress = ((current + 1) / len(questions)) * 100

    return render_template(
        "quiz.html",
        player=session["player"],
        question=questions[question_index],
        question_number=current + 1,
        total_questions=len(questions),
        progress=progress
    )


@app.route("/submit", methods=["POST"])
def submit():
    if "player" not in session:
        return redirect(url_for("home"))

    selected_answer = request.form.get("answer")

    current = session["current"]
    question_index = session["question_order"][current]

    if selected_answer == questions[question_index]["answer"]:
        session["score"] += 1

    session["current"] += 1

    return redirect(url_for("quiz"))


@app.route("/result")
def result():
    if "player" not in session:
        return redirect(url_for("home"))

    score = session["score"]
    total = len(questions)
    percentage = round((score / total) * 100)

    correct = score
    incorrect = total - score

    if percentage >= 80:
        message = "🏆 Excellent!"
    elif percentage >= 60:
        message = "🎉 Good Job!"
    elif percentage >= 40:
        message = "👍 Keep Practicing!"
    else:
        message = "📚 Better Luck Next Time!"

    with open("scores.txt", "a") as file:
        file.write(f"{session['player']} - {score}/{total} ({percentage}%)\n")

    return render_template(
        "result.html",
        player=session["player"],
        score=score,
        total=total,
        percentage=percentage,
        correct=correct,
        incorrect=incorrect,
        message=message
    )


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)