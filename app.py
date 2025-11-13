import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

recipes = [
    {
        "name": "Spaghetti Bolognese",
        "image": "dish1.jpg",
        "description": "Rich tomato meat sauce over al dente spaghetti.",
    },
    {
        "name": "Chicken Stir-Fry",
        "image": "dish2.jpg",
        "description": "Colorful veggies and chicken in a savory soy-garlic sauce.",
    },
    {
        "name": "Avocado Toast",
        "image": "dish3.jpg",
        "description": "Crispy sourdough topped with smashed avocado and chili flakes.",
    },
]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        name = request.form.get("name")
        file = request.files.get("photo")

        if not name or not file or file.filename == "":
            return render_template(
                "add.html",
                error="Please enter a recipe name and choose a photo.",
            )

        if not allowed_file(file.filename):
            return render_template(
                "add.html",
                error="File type not allowed. Use png, jpg, jpeg, or gif.",
            )

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        recipes.append(
            {
                "name": name,
                "image": filename,
                "description": "User-added recipe.",
            }
        )

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/settings", methods=["GET"])
def settings():
    # Just render the settings page; JS will handle saving to localStorage
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)
