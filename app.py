
from flask import Flask, request, redirect, render_template_string
import database

app = Flask(__name__)

database.initialize_database()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Inventory Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            background: #f2f4f8;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 12px;
        }
        h1 { color: #263b64; text-align: center; }
        input, button {
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
        }
        input { border: 1px solid #ccc; }
        button {
            background: #263b64;
            color: white;
            border: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th { background: #263b64; color: white; }
    </style>
</head>
<body>
<div class="container">

<h1>Inventory Management System</h1>
<p>Manage your products and stock easily.</p>

<h3>Add Product</h3>
<form action="/add" method="POST">
    <input name="pid" placeholder="Product ID" required>
    <input name="name" placeholder="Product Name" required>
    <input name="qty" type="number" min="0"
           placeholder="Quantity" required>
    <button type="submit">Add Product</button>
</form>

<h3>Search Product</h3>
<form action="/" method="GET">
    <input name="search" placeholder="Enter Product ID">
    <button type="submit">Search</button>
    <a href="/">View All</a>
</form>

<h3>Product List</h3>
<table>
<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Quantity</th>
    <th>Action</th>
</tr>
{% for p in products %}
<tr>
    <td>{{ p[0] }}</td>
    <td>{{ p[1] }}</td>
    <td>{{ p[2] }}</td>
    <td>
        <form action="/update" method="POST">
            <input type="hidden" name="pid" value="{{ p[0] }}">
            <input type="number" name="qty" min="0"
                   placeholder="New Qty" required>
            <button>Update</button>
        </form>

        <form action="/delete" method="POST">
            <input type="hidden" name="pid" value="{{ p[0] }}">
            <button>Delete</button>
        </form>
    </td>
</tr>
{% endfor %}
</table>

</div>
</body>
</html>
"""


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    if search:
        product = database.search_product(search)
        products = [product] if product else []
    else:
        products = database.get_all_products()

    return render_template_string(HTML, products=products)


@app.route("/add", methods=["POST"])
def add():
    try:
        pid = request.form["pid"].strip()
        name = request.form["name"].strip()
        qty = int(request.form["qty"])

        if not pid or not name or qty < 0:
            return "Invalid product details", 400

        database.add_product(pid, name, qty)

    except ValueError:
        return "Please enter a valid quantity", 400

    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    try:
        pid = request.form["pid"]
        qty = int(request.form["qty"])

        if qty < 0:
            return "Quantity cannot be negative", 400

        database.update_product(pid, qty)

    except ValueError:
        return "Invalid quantity", 400

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    pid = request.form["pid"]
    database.delete_product(pid)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
