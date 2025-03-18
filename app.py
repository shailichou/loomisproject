from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_loomis_guidelines(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 3

    # Draw main Loomis circle
    cv2.circle(image, (center_x, center_y - radius // 4), radius, (0, 255, 0), 2)

    # Vertical and horizontal guidelines
    cv2.line(image, (center_x, 0), (center_x, height), (255, 0, 0), 2)
    cv2.line(image, (0, center_y), (width, center_y), (255, 0, 0), 2)

    # Jawline guidelines
    jaw_y = center_y + radius // 2
    cv2.line(image, (center_x - radius, jaw_y), (center_x + radius, jaw_y), (255, 0, 0), 2)

    # Hairline guideline
    hairline_y = center_y - radius // 2
    cv2.line(image, (center_x - radius, hairline_y), (center_x + radius, hairline_y), (255, 0, 0), 2)

    # Eyeline
    eye_y = center_y - radius // 6
    cv2.line(image, (center_x - radius, eye_y), (center_x + radius, eye_y), (255, 0, 0), 2)

    # Nose base line
    nose_y = center_y + radius // 6
    cv2.line(image, (center_x - radius, nose_y), (center_x + radius, nose_y), (255, 0, 0), 2)

    processed_path = os.path.join(UPLOAD_FOLDER, "processed_" + os.path.basename(image_path))
    cv2.imwrite(processed_path, image)
    return processed_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return render_template("index.html", error="No file uploaded!")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        processed_image_path = generate_loomis_guidelines(file_path)
        return render_template("result.html", original=file.filename, processed=os.path.basename(processed_image_path))

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

