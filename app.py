import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder where uploaded images will be saved
UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Hardcoded starting recipes
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

        # Basic validation
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

        # Save file
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Add new recipe to the list
        recipes.append(
            {
                "name": name,
                "image": filename,
                "description": "User-added recipe.",
            }
        )

        # Go back to the main page with updated carousel
        return redirect(url_for("index"))

    # GET request -> show form
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
