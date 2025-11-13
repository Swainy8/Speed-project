from flask import Flask, render_template

app = Flask(__name__)

# Hardcoded recipes
recipes = [
    {
        "name": "Spaghetti Bolognese",
        "image": "dish1.jpg",
        "description": "Rich tomato meat sauce over al dente spaghetti."
    },
    {
        "name": "Chicken Stir-Fry",
        "image": "dish2.jpg",
        "description": "Colorful veggies and chicken in a savory soy-garlic sauce."
    },
    {
        "name": "Avocado Toast",
        "image": "dish3.jpg",
        "description": "Crispy sourdough topped with smashed avocado and chili flakes."
    },
]

@app.route("/")
def index():
    # Pass recipes to the template
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)
