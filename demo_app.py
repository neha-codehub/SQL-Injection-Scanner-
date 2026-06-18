from flask import Flask, request

app = Flask(__name__)

@app.route("/product")
def product():

    product_id = request.args.get("id", "")

    if "'" in product_id or '"' in product_id:
        return """
        SQL syntax error near ''
        MySQL Warning: You have an error in your SQL syntax
        """

    return f"Product ID: {product_id}"

if __name__ == "__main__":
    app.run(debug=True)