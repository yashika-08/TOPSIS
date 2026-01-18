from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


def run_topsis(input_file, weights, impacts):
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

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    return df


def send_email(receiver_email, content_csv):
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")

    if not sender_email or not sender_password:
        raise Exception("Email credentials not set")

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find the TOPSIS results attached.")

    msg.add_attachment(
        content_csv.encode(),
        maintype="text",
        subtype="csv",
        filename="result.csv"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["file"]
            weights = list(map(float, request.form["weights"].split(",")))
            impacts = request.form["impacts"].split(",")

            send_email_flag = request.form.get("send_email")
            email = request.form.get("email")

            input_path = "/tmp/input.csv"
            file.save(input_path)

            result_df = run_topsis(input_path, weights, impacts)

            # OPTIONAL EMAIL
            if send_email_flag and email:
                try:
                    send_email(email, result_df.to_csv(index=False))
                except Exception as e:
                    print("Email failed:", e)

            return render_template(
                "result.html",
                tables=[result_df.to_html(classes="table table-bordered", index=False)]
            )

        except Exception as e:
            return f"Error occurred: {str(e)}", 500

    return render_template("index.html")
