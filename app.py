from flask import Flask, render_template, request
import imageio.v3 as iio

app = Flask(__name__)

def predict(image):
    # This function makes predictions given an image.
    # Note that the image will be in RGB, unlike OpenCV.
    return {
        "predictions": [("dog1", 0.2), ("dog2", 0.7), ("dog3", 0.1)]
    }


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api", methods=["POST"])
def api():
    try:
        image = request.files["image"]
        image = iio.imread(image)
    except:
        return { "error": "Invalid image" }, 400
    return predict(image)