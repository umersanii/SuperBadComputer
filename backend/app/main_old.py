import subprocess
import requests
import time
import psutil
import os
import json
import socket
import threading
from flask import Flask, jsonify, render_template, make_response
from pyngrok import ngrok
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate("/home/umersani/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

NGROK_URL_FILE = "/home/umersani/BadComputer/ngrok_url.json"

app = Flask(__name__)

def update_link(new_url):
    db.collection("status").document("alive").set({"resourcemonitor_url": new_url})

def check_link():
    doc_ref = db.collection("links").document("current")
    doc = doc_ref.get()
    if doc.exists:
        print(f"URL is: {doc.to_dict()['url']}")
    else:
        print("No document found!")

def save_ngrok_url(url):
    try:
        with open(NGROK_URL_FILE, "w") as f:
            json.dump({"ngrok_url": url}, f)
        update_link(url)
    except Exception as e:
        print(f"Error saving ngrok URL: {e}")

def start_ngrok():
    try:
        tunnel = ngrok.connect(5004, bind_tls=True)
        return tunnel.public_url
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_hostname():
    try:
        return subprocess.check_output(['hostname']).decode().strip()
    except subprocess.CalledProcessError:
        return "Unknown"

def get_mac_address():
    try:
        return open('/sys/class/net/eth0/address').read().strip()
    except Exception:
        return "00:00:00:00:00:00"

def get_top_processes(n=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc_info = proc.info
            if proc_info['cpu_percent'] is not None:
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:n]

def get_temperature():
    try:
        temp = os.popen("vcgencmd measure_temp").readline().strip()
        return float(temp.replace("temp=", "").replace("'C", ""))
    except Exception:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return float(f.read()) / 1000.0
        except Exception:
            return 45.0

def get_uptime():
    return round(time.time() - psutil.boot_time())

def get_system_usage():
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    swap = psutil.swap_memory()

    return {
        "cpu_total": psutil.cpu_percent(interval=1),
        "cpu_per_core": psutil.cpu_percent(percpu=True),
        "cpu_freq": {
            "current": cpu_freq.current if cpu_freq else None,
            "min": cpu_freq.min if cpu_freq else None,
            "max": cpu_freq.max if cpu_freq else None
        },
        "memory": {
            "percent": memory.percent,
            "total": round(memory.total / (1024 ** 2), 2),
            "available": round(memory.available / (1024 ** 2), 2),
            "used": round(memory.used / (1024 ** 2), 2),
            "free": round(memory.free / (1024 ** 2), 2),
            'swap_total': round(swap.total / (1024 ** 2), 1),
            'swap_used': round(swap.used / (1024 ** 2), 1),
            'swap_free': round(swap.free / (1024 ** 2), 1),
            'swap_percent': round(swap.percent, 1)
        },
        "disk": psutil.disk_usage('/').percent,
        "disk_io": {
            "read_mb": round(disk_io.read_bytes / (1024 * 1024), 2),
            "write_mb": round(disk_io.write_bytes / (1024 * 1024), 2)
        },
        "network": {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024 * 1024), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024 * 1024), 2)
        },
        "temperature": get_temperature(),
        "uptime": get_uptime(),
        "data": {'top_processes': get_top_processes()},
        "ip_address": get_ip_address(),
        "hostname": get_hostname(),
        "mac_address": get_mac_address()
    }

@app.route('/api/usage', methods=['GET'])
def usage():
    try:
        return jsonify(get_system_usage())
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve system usage: {str(e)}"}), 500

@app.after_request
def add_skip_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/')
def home():
    try:
        with open(NGROK_URL_FILE, 'r') as f:
            data = json.load(f)
        ngrok_url = data.get("ngrok_url", None)
        return make_response(render_template('index.html', ngrok_url=ngrok_url))
    except Exception as e:
        return jsonify({"error": f"Error loading ngrok URL: {str(e)}"}), 500

def update_last_seen_loop():
    while True:
        db.collection("status").document("alive").set({
            "pi_last_seen": firestore.SERVER_TIMESTAMP
        }, merge=True)
        time.sleep(10)

if __name__ == '__main__':
    print("🚀 Starting Flask App...")
    
    # Start the background task in a separate thread
    threading.Thread(target=update_last_seen_loop, daemon=True).start()

    # Start ngrok and save the URL if available
    ngrok_url = start_ngrok()
    if ngrok_url:
        check_link()
        save_ngrok_url(ngrok_url)
    else:
        print("⚠️ Ngrok URL not available!")

    # Run Flask app
    app.run(host='0.0.0.0', port=5004)
