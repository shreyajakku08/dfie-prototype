import os
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from breach_check import check_breaches
from username_scan import scan_username
from risk_score import calculate_risk_score
from exif_tools import extract_exif_data

app = Flask(__name__)

# Basic config for file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    """Render the main dashboard UI."""
    return render_template('index.html')

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
        "platforms": [],
        "risk_score": 0,
        "risk_category": "Low"
    }
    
    if scan_type == 'email':
        # Step 2: HIBP Breach Checker
        results['breaches'] = check_breaches(identifier)
        # We can extract a username from the email for the scanner
        username_guess = identifier.split('@')[0]
        results['platforms'] = scan_username(username_guess)
        
    elif scan_type == 'username':
        # Step 3: Username scanner
        results['platforms'] = scan_username(identifier)
    
    # Step 4: Calculate Risk Score
    risk_data = calculate_risk_score(results['breaches'], results['platforms'])
    results['risk_score'] = risk_data['score']
    results['risk_category'] = risk_data['category']
        
    return jsonify({"status": "success", "data": results}), 200

@app.route('/scan-image', methods=['POST'])
def scan_image():
    """
    Secondary API route to upload an image and extract EXIF forensics.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No image file provided."}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract Intelligence (Step 7)
        metadata = extract_exif_data(filepath)
        
        # Cleanup the uploaded file so we don't spam the disk space
        try:
            os.remove(filepath)
        except Exception:
            pass
            
        if "error" in metadata:
            return jsonify({"status": "error", "message": metadata["error"]}), 400
            
        return jsonify({"status": "success", "data": metadata}), 200

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
