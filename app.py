from flask import Flask, request, jsonify
import pandas as pd
import csv
import base64
import io
import re

app = Flask(__name__)


@app.route("/convert-json-to-csv", methods=["POST"])
def convert_json_to_csv():
    try:
        # Get JSON data from request
        json_data = request.get_json(force=True)        
        payload = json_data.get('body', json_data)

        headers_raw = payload['header']
        data_rows = payload['data']

        # Extract text inside square brackets from headers
        headers_clean = [
            re.search(r"\[(.*?)\]", h).group(1) if re.search(r"\[(.*?)\]", h) else h
            for h in headers_raw
        ]

        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers_clean)

        # Convert DataFrame to CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Encode CSV to Base64
        csv_base64 = base64.b64encode(csv_bytes).decode("utf-8")

        return jsonify(
            {
                "filename": "converted.csv",
                "content_base64": csv_base64,
                "content_type": "text/csv",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/convert", methods=["POST"])
def convert_to_csv_base64():
    try:
        # Parse JSON input
        t_data = request.get_json(force=True)
        body = t_data.get('body', t_data)
        if not body or "data" not in body:
            return (
                jsonify(
                    {"error": "Invalid input format. Expecting { 'data': { ... } }"}
                ),
                400,
            )
        headers_raw = body.get("header", [])
        rows = body.get("data", [])

        # Extract header names between [ and ]
        headers = [
            re.search(r"\[(.*?)\]", h).group(1) if re.search(r"\[(.*?)\]", h) else h
            for h in headers_raw
        ]

        # Create CSV content in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)

        # Convert CSV string to Base64
        csv_bytes = output.getvalue().encode("utf-8")
        csv_base64 = base64.b64encode(csv_bytes).decode("utf-8")

        # Return Base64 string in JSON
        return jsonify({"file_name": "output.csv", "file_base64": csv_base64})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
