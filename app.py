from flask import Flask, jsonify, request
from breach_check import check_breaches

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_footprint():
    """
    Main API route to scan digital footprint.
    Expects a JSON payload: {"identifier": "email@example.com", "type": "email"}
    """
    data = request.get_json()
    
    if not data or 'identifier' not in data:
        return jsonify({"error": "Missing 'identifier' in request body"}), 400
        
    identifier = data['identifier']
    scan_type = data.get('type', 'email') # default to email
    
    results = {
        "identifier": identifier,
        "type": scan_type,
        "breaches": [],
        # Risk score and platform data will be added in later steps
    }
    
    if scan_type == 'email':
        # Step 2: HIBP Breach Checker (using mock due to likely no API key)
        results['breaches'] = check_breaches(identifier)
        
    return jsonify({"status": "success", "data": results}), 200

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
