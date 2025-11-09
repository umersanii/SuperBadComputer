from firebase_admin import db
import psutil
import time
from datetime import datetime

from utils.utils import get_system_usage

def update_status_to_firebase():
    """Background thread to update system status to Firebase"""
    while True:
        try:
            stats = get_system_usage()
            ref = db.reference('system_status')
            ref.set(stats)
            time.sleep(5)  # Update every 5 seconds
        except Exception as e:
            print(f"Error updating Firebase: {e}")
            time.sleep(5)

def listen_for_commands():
    """Background thread to listen for commands from Firebase"""
    def command_callback(event):
        try:
            command = event.data
            if command:
                print(f"Received command: {command}")
                # Handle command here
        except Exception as e:
            print(f"Error processing command: {e}")
    
    ref = db.reference('commands')
    ref.listen(command_callback)