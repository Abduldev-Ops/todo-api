from flask import Flask, request, jsonify, app, redirect
import random, string, datetime

app = Flask(__name__)

urls = [] #url has short_code, original_url, created_at
 #optional: validate url

def generate_short_url():
    while True:
        characters = string.ascii_lowercase + string.digits
        short_code = "".join(random.choices(characters, k=6))
        if not any(url['short_code'] == short_code for url in urls):
            return short_code


def get_next_id():
    if not urls:
        return 1
    else:
        return urls[-1]["id"]+1

@app.route("/urls", methods=["GET"])
def get_all_urls():
    return jsonify({"urls": urls}), 200

@app.route("/urls", methods=["POST"])
def build_short_code():

    if not request.json:
        return jsonify({"error": "No url in body"}), 400
    short_url = generate_short_url()

    new_url = {
        "id": get_next_id(),
        "short_code": short_url, "original_url": request.json["url"],
        "created_at": datetime.datetime.now().isoformat()
    }

    urls.append(new_url)
    return jsonify(new_url), 201

@app.route("/<short_code>")
def redirect_to_url(short_code):
    for url in urls:
        if url["short_code"] == short_code:
            original_url = url["original_url"]
            return redirect(original_url)

    return jsonify({"error":"URL not found"}), 404

@app.route("/urls/<short_code>", methods=["DELETE"])
def delete_url(short_code):
    to_delete= ""
    for url in urls:
        if url["short_code"] == short_code:
            to_delete = url

    if to_delete is None:
        return jsonify({"error": "Short code not found"}), 404

    urls.remove(to_delete)
    return jsonify({'message': "URL deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5170)