from flask import Flask, request, jsonify
from model import predict
from flask_cors import CORS, cross_origin

app = Flask(__name__)


@app.route('/', methods=['POST'])
def getQuery():
    if request.method == "POST":
        flag = 1

        # query = request.form['query']
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
        else:
            return 'Content-Type not supported!'

        query = json["query"]
        metric = predict(query)
        # print(metric)
        max_match = max(zip(metric.values(), metric.keys()))[1]

        for i in metric:
            print(metric[i])
            if metric[i] < 0.5:
                flag = 0
                break
        response = jsonify({"ans": max_match, "authenticity": flag})
        # response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
