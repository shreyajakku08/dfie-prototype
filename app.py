from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def test_route():
    """Test route to ensure the API is running."""
    return jsonify({"status": "success", "message": "DFIE API is running!"}), 200

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
