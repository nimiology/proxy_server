from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)


@app.route("/proxy", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            params=request.args,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
