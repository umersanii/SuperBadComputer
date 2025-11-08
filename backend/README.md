# Backend - Pi Monitor Service

Flask service that runs on Raspberry Pi to collect system stats and communicate with Firebase.

## Tech Stack

- **Framework**: Flask
- **Language**: Python 3.8+
- **Real-time Database**: Firebase Admin SDK
- **System Monitoring**: psutil

## Getting Started

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install packages
pip install -r requirements.txt
```

### 2. Configure Firebase

1. Download your Firebase Admin SDK credentials from Firebase Console:
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"

2. Save the JSON file as `config/firebase-credentials.json`

3. Update the database URL in `app/main.py`:
   ```python
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://YOUR-PROJECT-ID-default-rtdb.firebaseio.com'
   })
   ```

### 3. Run the Service

```bash
python app/main.py
```

The service will:
- Start collecting system stats
- Update Firebase every 5 seconds
- Listen for commands from Firebase
- Run Flask API on port 5000

## Running as System Service

### On Raspberry Pi (SystemD)

1. Edit the service file with correct paths:
   ```bash
   nano pi-monitor.service
   ```

2. Copy to systemd:
   ```bash
   sudo cp pi-monitor.service /etc/systemd/system/
   ```

3. Enable and start:
   ```bash
   sudo systemctl enable pi-monitor.service
   sudo systemctl start pi-monitor.service
   ```

4. Check status:
   ```bash
   sudo systemctl status pi-monitor.service
   ```

5. View logs:
   ```bash
   sudo journalctl -u pi-monitor -f
   ```

### Service Management Commands

```bash
sudo systemctl start pi-monitor      # Start service
sudo systemctl stop pi-monitor       # Stop service
sudo systemctl restart pi-monitor    # Restart service
sudo systemctl status pi-monitor     # Check status
sudo systemctl enable pi-monitor     # Enable on boot
sudo systemctl disable pi-monitor    # Disable on boot
```

## Features

### System Monitoring
Collects and reports:
- CPU usage percentage
- Memory usage percentage
- Disk usage percentage
- CPU temperature (Raspberry Pi thermal sensor)
- Timestamp of last update
- Online status

### Command Handling
Listens for these commands via Firebase:
- `restart` - Restart the service
- `update_status` - Force immediate status update
- `clear_cache` - Clear system cache
- `shutdown` - Shutdown the Pi (requires sudo permissions)

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service status |
| `/health` | GET | Health check |
| `/stats` | GET | Current system statistics |

## File Structure

```
backend/
├── app/
│   └── main.py                          # Main application
├── config/
│   ├── firebase-credentials.json        # Your credentials (not in git)
│   └── firebase-credentials.json.example # Template
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment template
└── pi-monitor.service                   # SystemD service file
```

## Configuration

### Environment Variables (Optional)

Create `.env` file:
```env
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com
FLASK_ENV=production
FLASK_DEBUG=False
```

### Customizing Update Interval

In `app/main.py`, modify the sleep time:
```python
time.sleep(5)  # Update every 5 seconds
```

## Adding Custom Commands

1. Add command handling in `handle_command()` function:
   ```python
   elif command == 'your_command':
       print("Executing your command...")
       # Your logic here
   ```

2. Add button in frontend `ControlPanel.tsx`

## Troubleshooting

**Import Error: No module named 'firebase_admin'**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**Permission Denied: firebase-credentials.json**
- Check file exists in `config/` directory
- Verify file permissions: `chmod 600 config/firebase-credentials.json`

**Temperature shows 0**
- Normal on non-Raspberry Pi devices
- On Pi, check: `cat /sys/class/thermal/thermal_zone0/temp`

**Service won't start**
- Check logs: `sudo journalctl -u pi-monitor -f`
- Verify paths in service file
- Ensure virtual environment exists
- Check Firebase credentials

**Firebase connection errors**
- Verify database URL is correct
- Check internet connectivity
- Ensure credentials file is valid JSON
- Verify Firebase project has Realtime Database enabled

## Security Considerations

⚠️ **Important for Production:**

1. **Credentials**: Never commit `firebase-credentials.json` to Git
2. **Permissions**: Run service with limited user permissions
3. **Commands**: Add authentication before executing system commands
4. **Network**: Use firewall rules to restrict access
5. **Updates**: Keep dependencies updated: `pip install --upgrade -r requirements.txt`

## Dependencies

| Package | Purpose |
|---------|---------|
| `Flask` | Web framework |
| `flask-cors` | Enable CORS for API |
| `firebase-admin` | Firebase Admin SDK |
| `psutil` | System monitoring |
| `python-dotenv` | Environment variables |

## Extending the Service

### Add New Metrics

```python
def get_system_stats():
    # Add your custom metrics
    network = psutil.net_io_counters()
    
    return {
        # ... existing stats
        'network_sent': network.bytes_sent,
        'network_recv': network.bytes_recv,
    }
```

### Add Scheduled Tasks

```python
import schedule

def scheduled_task():
    print("Running scheduled task...")

schedule.every().hour.do(scheduled_task)
```

## Testing

### Manual Testing

```bash
# Test Flask endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/stats

# Test Firebase connection
python -c "from app.main import get_system_stats; print(get_system_stats())"
```

### Monitor in Real-time

```bash
# Watch logs
sudo journalctl -u pi-monitor -f

# Watch Firebase data
# Use Firebase Console or add logging
```

## Performance

- **CPU Impact**: ~1-2% average
- **Memory Usage**: ~50-100 MB
- **Network**: Minimal (updates every 5 seconds)
- **Disk I/O**: Negligible

## Learn More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [SystemD Service Tutorial](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
