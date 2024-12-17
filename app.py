from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# Load data from CSV file
file_path = "Panlasang Pinoy Recipes.csv"
data = pd.read_csv(file_path)

# Extract unique categories (course_type)
categories = data['course_type'].dropna().unique()

# HTML templates
main_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recipe Categories</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-10">
        <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Recipe Categories</h1>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {% for category in categories %}
            <a href="/category/{{ category }}" class="block">
                <div class="p-6 bg-white border border-gray-300 rounded-lg shadow-md hover:shadow-lg text-center uppercase font-semibold text-gray-700 hover:bg-gray-50 transition">
                    {{ category }}
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

category_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ category }} Recipes</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-10">
        <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Recipes in {{ category }}</h1>
        <ul class="space-y-4">
            {% for recipe, url in recipes %}
            <li class="text-lg text-blue-600 hover:text-blue-800">
                <a href="{{ url }}" target="_blank">{{ recipe }}</a>
            </li>
            {% endfor %}
        </ul>
        <div class="text-center mt-8">
            <a href="/" class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Back to Categories</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(main_page, categories=categories)

@app.route('/category/<category>')
def show_category(category):
    # Filter recipes for the selected category
    filtered_data = data[data['course_type'] == category][['recipe_name', 'link_url']]
    recipes = list(zip(filtered_data['recipe_name'], filtered_data['link_url']))
    return render_template_string(category_page, category=category, recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
