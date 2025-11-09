import subprocess
import requests
import time
import psutil
import os
import json
import socket
import threading
from flask import Flask, jsonify, render_template, make_response


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
