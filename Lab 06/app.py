from flask import Flask, render_template, request, jsonify
import os
import base64
from face_detect import analyze_face

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():

    profile = None

    if request.method == "POST":

        file = request.files["image"]

        if file.filename != "":
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            profile = analyze_face(filepath)

    return render_template("index.html", profile=profile)


# Webcam Capture Route
@app.route("/capture", methods=["POST"])
def capture():

    data = request.json["image"]

    encoded_data = data.split(",")[1]

    image_data = base64.b64decode(encoded_data)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "webcam_capture.png")

    with open(filepath, "wb") as f:
        f.write(image_data)

    profile = analyze_face(filepath)

    return jsonify(profile)


if __name__ == "__main__":
    app.run(debug=True)