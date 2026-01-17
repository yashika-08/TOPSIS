from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def run_topsis(input_file, weights, impacts, output_file):
    df = pd.read_csv(input_file)
    data = df.iloc[:, 1:].astype(float)

    normalized = data / np.sqrt((data ** 2).sum())
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)


def send_email(receiver_email, file_path):
    sender_email = "yashikagarg1508@gmail.com"
    sender_password = "qrnz fjkc syrz pnpq"

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find the attached TOPSIS result file.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=os.path.basename(file_path),
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        weights = list(map(float, request.form["weights"].split(",")))
        impacts = request.form["impacts"].split(",")
        email = request.form["email"]

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(RESULT_FOLDER, "result.csv")

        file.save(input_path)

        run_topsis(input_path, weights, impacts, output_path)
        send_email(email, output_path)

        return render_template("success.html")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
