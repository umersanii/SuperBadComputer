# Pi Monitor & Control System

A full-stack IoT application for monitoring and controlling a Raspberry Pi remotely through a web interface.

## 🏗️ Architecture

- **Frontend**: Next.js 14 (React + TypeScript) hosted on Vercel
- **Backend**: Flask (Python) service running on Raspberry Pi
- **Database**: Firebase Realtime Database for real-time communication

## 📁 Project Structure

```
SuperBadComputer/
├── frontend/               # Next.js web application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities and Firebase config
│   ├── package.json
│   └── tsconfig.json
│
└── backend/               # Flask service for Raspberry Pi
    ├── app/
    │   └── main.py       # Main Flask application
    ├── config/
    │   └── firebase-credentials.json.example
    ├── requirements.txt
    └── pi-monitor.service # SystemD service file
```

## 🚀 Features

### Frontend (Web Dashboard)
- Real-time system monitoring (CPU, Memory, Disk, Temperature)
- Remote control panel for Pi operations
- Live connection status indicator
- Responsive design with Tailwind CSS

### Backend (Pi Service)
- Collects system statistics (CPU, RAM, disk usage, temperature)
- Sends data to Firebase every 5 seconds
- Listens for remote commands from Firebase
- RESTful API endpoints for health checks

## 📋 Prerequisites

### For Frontend Development
- Node.js 18+ and npm
- Firebase project with Realtime Database
- Vercel account (for deployment)

### For Raspberry Pi Setup
- Raspberry Pi (any model with network connectivity)
- Python 3.8+
- Firebase project with Admin SDK credentials

## 🔧 Setup Instructions

### 1. Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Realtime Database
3. Set database rules (for development):
   ```json
   {
     "rules": {
       ".read": true,
       ".write": true
     }
   }
   ```
4. Get your web app configuration (Project Settings > General)
5. Download Admin SDK credentials (Project Settings > Service Accounts)

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local with your Firebase config
nano .env.local

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup (On Raspberry Pi)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create config directory and add Firebase credentials
mkdir -p config
# Copy your firebase-credentials.json to config/

# Update the database URL in app/main.py
nano app/main.py

# Test run
python app/main.py
```

### 4. Setup as System Service (Raspberry Pi)

```bash
# Copy service file
sudo cp pi-monitor.service /etc/systemd/system/

# Edit service file with correct paths
sudo nano /etc/systemd/system/pi-monitor.service

# Enable and start service
sudo systemctl enable pi-monitor.service
sudo systemctl start pi-monitor.service

# Check status
sudo systemctl status pi-monitor.service
```

### 5. Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variables in Vercel dashboard
# (Project Settings > Environment Variables)
```

## 🔒 Security Notes

⚠️ **Important**: This is a learning project with basic security. For production:

1. Implement proper Firebase security rules
2. Add authentication (Firebase Auth)
3. Use environment variables for all credentials
4. Never commit `.env` files or credentials to Git
5. Implement rate limiting on API endpoints
6. Add HTTPS for all communications
7. Validate and sanitize all inputs

## 📊 Firebase Data Structure

```json
{
  "pi": {
    "status": {
      "cpu": 45.2,
      "memory": 62.8,
      "disk": 34.5,
      "temperature": 52.3,
      "timestamp": 1699401234567,
      "online": true
    },
    "commands": {
      "command": "restart",
      "timestamp": 1699401234567
    }
  }
}
```

## 🎯 Learning Objectives

This project demonstrates:
- Real-time data synchronization with Firebase
- Full-stack TypeScript/Python development
- System monitoring and control
- IoT communication patterns
- Modern web deployment (Vercel)
- Linux service management
- RESTful API design

## 🛠️ Commands Reference

### Frontend Commands
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Backend Commands
```bash
python app/main.py                    # Run Flask app
sudo systemctl start pi-monitor       # Start service
sudo systemctl stop pi-monitor        # Stop service
sudo systemctl restart pi-monitor     # Restart service
sudo systemctl status pi-monitor      # Check status
sudo journalctl -u pi-monitor -f      # View logs
```

## 🐛 Troubleshooting

### Frontend Issues
- **Firebase connection error**: Check `.env.local` configuration
- **Build errors**: Run `npm install` to ensure all dependencies are installed
- **CORS errors**: Ensure Firebase rules allow your domain

### Backend Issues
- **Import errors**: Activate virtual environment and reinstall requirements
- **Permission denied**: Run with appropriate user permissions
- **Firebase connection**: Verify credentials file path and database URL
- **Temperature reading fails**: Normal on non-Pi devices; will show 0

## 📝 Next Steps

Ideas to extend this project:
- Add user authentication
- Implement data visualization with charts
- Add more system controls (GPIO pins, processes)
- Create mobile app with React Native
- Add email/SMS alerts for critical events
- Store historical data for analytics
- Add multiple Pi support

## 📄 License

This is a learning project - feel free to use and modify as needed!

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome!
