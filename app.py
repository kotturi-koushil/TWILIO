from flask import Flask, render_template, request
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

import joblib

clf = joblib.load("nayamodel.pkl")


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        s = request.form["nm"]
        ans = clf.predict([s])
        if ans == [1] or [2]:
            import os
            from twilio.rest import Client

            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            account_sid = "AC588b7164ba94dd303fbc3d00d5976808"
            auth_token = "0cce0bb438b8bb6ad55ab126669b87e1"
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=s, from_="+13208533216", to="+916303620068"
            )

            print(message.sid)

            from twilio.rest import Client

            # Your Twilio Account SID and Auth Token
            account_sid = "AC588b7164ba94dd303fbc3d00d5976808"
            auth_token = "0cce0bb438b8bb6ad55ab126669b87e1"

            # Create a Twilio client
            client = Client(account_sid, auth_token)

            # The phone number you want to call
            to_number = "+916303620068"  # Replace with the recipient's number

            # The Twilio phone number making the call
            from_number = "+1 320 853 3216"  # Replace with your Twilio phone number

            # The message you want to say during the call
            message = s

            # Make the call
            call = client.calls.create(
                to=to_number,
                from_=from_number,
                twiml=f"<Response><Say>{message}</Say></Response>",
            )

            print(f"Call SID: {call.sid}")

            print(f"Call SID: {call.sid}")

        return render_template("index.html", score=ans)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
