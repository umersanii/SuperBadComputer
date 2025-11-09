from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import psutil
import time
import threading
from datetime import datetime
import os
from dotenv import load_dotenv

from utils.utils import *
from background_tasks.tasks import *
app = Flask(__name__)
CORS(app)

load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate('config/firebase-credentials.json')
# Make sure this URL matches your Firebase project
db_url = os.getenv('FIREBASE_DATABASE_URL')

print(f"Connecting to Firebase at                                 : {db_url}")  # Add this to debug

firebase_admin.initialize_app(cred, {
    'databaseURL': db_url
})


@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'Pi Monitor Service is running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/stats')
def stats():
    """Get current system stats via HTTP"""
    stats = get_system_stats()
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'Unable to get stats'}), 500

if __name__ == '__main__':
    # Start background thread for updating status
    status_thread = threading.Thread(target=update_status_to_firebase, daemon=True)
    status_thread.start()
    
    # Start listening for commands
    command_thread = threading.Thread(target=listen_for_commands, daemon=True)
    command_thread.start()
    
    print("Starting Pi Monitor Service...")
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
