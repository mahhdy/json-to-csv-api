
from flask import Flask, request, jsonify
import pandas as pd
import base64
import io

app = Flask(__name__)

@app.route('/convert-json-to-csv', methods=['POST'])
def convert_json_to_csv():
    try:
        json_data = request.get_json(force=True)
        df = pd.DataFrame(json_data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')

        return jsonify({
            "filename": "converted.csv",
            "content_base64": csv_base64,
            "content_type": "text/csv"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
