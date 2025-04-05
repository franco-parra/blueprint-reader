from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import hashlib
import json
from dotenv import load_dotenv


def calculate_file_hash(file_path: str) -> str:
    """Calculate the hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_blueprint_data(file_path: str) -> dict:
    """Load blueprint data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Blueprint data file not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in blueprint data file")

# Load environment variables
load_dotenv()

# Configuration
REFERENCE_PDF_PATH = os.getenv('REFERENCE_PDF_PATH', 'in/bp_1.pdf')
BLUEPRINT_DATA_PATH = os.getenv('BLUEPRINT_DATA_PATH', 'data/blueprint_data.json')
ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(REFERENCE_PDF_PATH), exist_ok=True)
os.makedirs(os.path.dirname(BLUEPRINT_DATA_PATH), exist_ok=True)

# Validate configuration
if not os.path.exists(REFERENCE_PDF_PATH):
    raise FileNotFoundError(f"File not found in {REFERENCE_PDF_PATH}")

if not os.path.exists(BLUEPRINT_DATA_PATH):
    raise FileNotFoundError(f"File not found in {BLUEPRINT_DATA_PATH}")

try:
    REFERENCE_HASH = calculate_file_hash(REFERENCE_PDF_PATH)
    BLUEPRINT_DATA = load_blueprint_data(BLUEPRINT_DATA_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to initialize application: {str(e)}")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Configure CORS with production settings
CORS(app, resources={
    r"/*": {
        "origins": os.getenv('ALLOWED_ORIGINS', '*').split(','),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route("/")
def hello_world():
    return "<p>Blueprint Reader API</p>"


@app.route('/parse-blueprint', methods=['POST'])
def parse_blueprint():
    if 'file' not in request.files:
        return jsonify({'error': 'File not found'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the file temporarily to calculate its hash
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(temp_path)
            
            # Calculate hash of the received file
            received_hash = calculate_file_hash(temp_path)
            
            # Delete the temporary file
            os.remove(temp_path)
            
            # Compare hashes
            if received_hash == REFERENCE_HASH:
                return jsonify({
                    'message': 'Blueprint parsed successfully',
                    'filename': file.filename,
                    'data': BLUEPRINT_DATA
                })
            else:
                return jsonify({
                    'error': 'The hash of the file does not match the reference file',
                    'hash_match': False
                }), 400
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == "__main__":
    # Use production server when not in debug mode
    if os.getenv('FLASK_ENV') != 'development':
        from waitress import serve
        serve(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    else:
        app.run(debug=True)