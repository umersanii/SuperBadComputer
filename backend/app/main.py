from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import psutil
import time
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK
# Download your service account key from Firebase Console
cred = credentials.Certificate('config/firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id-default-rtdb.firebaseio.com'
})

def get_system_stats():
    """Get current system statistics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get CPU temperature (Raspberry Pi specific)
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000.0
        except:
            temp = 0
        
        return {
            'cpu': round(cpu_percent, 2),
            'memory': round(memory.percent, 2),
            'disk': round(disk.percent, 2),
            'temperature': round(temp, 2),
            'timestamp': int(time.time() * 1000),
            'online': True
        }
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return None

def update_status_to_firebase():
    """Update system status to Firebase in real-time"""
    ref = db.reference('pi/status')
    while True:
        try:
            stats = get_system_stats()
            if stats:
                ref.set(stats)
                print(f"Status updated: CPU={stats['cpu']}%, Memory={stats['memory']}%")
        except Exception as e:
            print(f"Error updating Firebase: {e}")
        
        time.sleep(5)  # Update every 5 seconds

def listen_for_commands():
    """Listen for commands from Firebase"""
    def command_callback(event):
        print(f"Received command: {event.data}")
        if event.data:
            command = event.data.get('command')
            handle_command(command)
    
    ref = db.reference('pi/commands')
    ref.listen(command_callback)

def handle_command(command):
    """Handle incoming commands"""
    print(f"Handling command: {command}")
    
    if command == 'restart':
        print("Restarting service...")
        # Add your restart logic here
        
    elif command == 'update_status':
        print("Forcing status update...")
        stats = get_system_stats()
        if stats:
            db.reference('pi/status').set(stats)
            
    elif command == 'clear_cache':
        print("Clearing cache...")
        # Add your cache clearing logic here
        
    elif command == 'shutdown':
        print("Shutting down...")
        # Add your shutdown logic here
        # os.system('sudo shutdown -h now')
    
    else:
        print(f"Unknown command: {command}")

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
    app.run(host='0.0.0.0', port=5000, debug=False)
