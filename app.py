from flask import Flask, render_template, jsonify, request, make_response

app = Flask(__name__)

stock = {
    "fruit": {
    "apple": 30,
    "banana": 70,
    "cherry": 40
    }
}


@app.route("/get_text")
def get_text():
    return "some text"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/qs")
def qs():
    if request.args:
        req = request.args
        return " ".join(f"{k}:{v}" for k, v in req.items())

    return "No query"


@app.route("/get_stock", methods=["GET"])
def get_stock():
    res = make_response(jsonify(stock))
    return res


@app.route("/stock/<collection>")
def get_collection(collection):
    if collection in stock:
        res = make_response(jsonify(stock[collection]), 200)
        return res
    res = res = make_response(jsonify({"error": "Item not faund"}), 400)
    return res


@app.route("/stock/<collection>/<member>")
def get_member(collection, member):
    if collection in stock:
        member = stock[collection].get(member)
        if member:
            res = make_response(jsonify(member), 200)
            return res
        res = make_response(jsonify({"error": "unknoun member"}), 400)
        return res

    res = res = make_response(jsonify({"error": "collection not faund"}), 400)
    return res


@app.route("/add_collection", methods=["GET", "POST"])
def add_collection():
    if request.method == "POST":

        req = request.form

        collection = req.get("collection")
        member = req.get("member")
        qty = req.get("qty")

        if collection in stock:
            message = "message already exists"
            return render_template("add_collection.html", stock=stock, message=message)

        stock[collection] = {member: qty}
        message = "collection created"
        return render_template("add_collection.html", stock=stock, message=message)

    return render_template("add_collection.html", stock=stock)


@app.route("/stock/<collection>", methods=["POST"])
def create_collection(collection):
    req = request.get_json()

    if collection in stock:
        res = make_response(jsonify({"error": "collection olready exist"}), 400)
        return res

    stock.update({collection: req})
    res = make_response(jsonify({"message": "collection created"}), 200)
    return res


@app.route("/stock/<collection>", methods=["PUT"])
def put_collection(collection):
    req = request.get_json()
    stock[collection] = req

    res = make_response(jsonify({"message": "collection replaced"}), 200)
    return res


@app.route("/stock/<collection>", methods=["PATCH"])
def patch_collection(collection):
    req = request.get_json()

    if collection in stock:
        for k, v in req.items():
            stock[collection][k] = v

        res = make_response(jsonify({"message": "collection update"}), 200)
        return res

    stock[collection] = req
    res = make_response(jsonify({"message": "collection created"}), 200)
    return res


@app.route("/stock/<collection>/<member>", methods=["PATCH"])
def patch_member(collection, member):
    req = request.get_json()

    if collection in stock:
        for k, v in req.items():
            if member in stock[collection]:
                stock[collection][member] = v

                res = make_response(jsonify({"message": "collection update"}), 200)
                return res

            stock[collection][member] = req
            res = make_response(jsonify({"message": "collection created"}), 200)
            return res
    res = make_response(jsonify({"message": "collection not found"}), 400)
    return res


@app.route("/stock/<collection>", methods=["DELETE"])
def delete_collection(collection):

    if collection in stock:
        del stock[collection]
        res = make_response(jsonify({}), 204)
        return res

    res = make_response(jsonify({"error": "collection not found"}), 400)
    return res


@app.route("/stock/<collection>/<member>", methods=["DELETE"])
def delete_member(collection, member):
    if collection in stock:
        if member in stock[collection]:
            del stock[collection][member]
            res = make_response(jsonify({}), 204)
            return res

        res = make_response(jsonify({"error": "member not found"}), 400)
        return res

    res = make_response(jsonify({"error": "collection not found"}), 400)
    return res


if __name__ == "__main__":
    app.run(debug=True)
