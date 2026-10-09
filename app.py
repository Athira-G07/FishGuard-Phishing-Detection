from flask import Flask, render_template, request
from utils.feature_extractor import extract_url_features
import joblib
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "random_forest_phishing_model.pkl"
)

FEATURES_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "feature_columns.pkl"
)

model = joblib.load(MODEL_PATH)
URL_MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "live_url_phishing_model.pkl"
)

url_model = joblib.load(URL_MODEL_PATH)

print("11-feature phishing model loaded successfully!")

print("URL phishing model loaded successfully!")
feature_columns = joblib.load(FEATURES_PATH)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url")
    if not url or not url.startswith(("http://", "https://")):
        return "Please enter a complete URL starting with http:// or https://"

    try:
        features = extract_url_features(url)

        feature_order = ["URLLength", "DomainLength", "IsDomainIP", "NoOfSubDomain", "IsHTTPS", "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL", "NoOfDegitsInURL"]

        input_data = [[features[name] for name in feature_order]]

        prediction = url_model.predict(input_data)[0]

        if prediction == 0:
            result = "Phishing Website"
        else:
            result = "Legitimate Website"

        return render_template("result.html", url=url, result=result, features=features)

    except Exception as e:
        return f"Error: {e}"
if __name__ == "__main__":
    app.run(debug=True)