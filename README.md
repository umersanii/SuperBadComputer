# Pi Monitor & Control System

A full-stack IoT application for monitoring and controlling a Raspberry Pi remotely through a web interface, using Tailscale for private network access.

## 🏗️ Architecture

- **Frontend**: Next.js 14 (React + TypeScript) hosted on Vercel (public)
- **Backend**: Laravel 11 (PHP) running on Raspberry Pi (Tailscale-only)
- **Network**: Tailscale VPN for secure private access
- **Real-time**: WebSocket connection for live metrics
- **Auth**: Laravel Sanctum token-based authentication

**Security Model:**
- Frontend is publicly accessible (loads for everyone)
- Backend is private (only accessible within Tailscale network)
- Outside Tailscale: UI loads but shows "Internal network required"
- Inside Tailscale: Full functionality with real-time updates

## 📁 Project Structure

```
SuperBadComputer/
├── frontend/               # Next.js web application (Vercel)
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   │   ├── PiStatus.tsx
│   │   │   ├── ControlPanel.tsx
│   │   │   ├── NetworkGuard.tsx
│   │   │   └── WebSocketProvider.tsx
│   │   ├── lib/           # API client, WebSocket, auth
│   │   └── types/         # TypeScript definitions
│   ├── .env.local
│   └── package.json
│
└── backend/               # Laravel API (Raspberry Pi)
    ├── app/
    │   ├── Http/
    │   │   ├── Controllers/
    │   │   │   ├── HealthController.php
    │   │   │   ├── StatsController.php
    │   │   │   └── CommandController.php
    │   │   └── Middleware/
    │   │       └── EnsureTailscaleRequest.php
    │   ├── Services/
    │   │   ├── SystemMetricsService.php
    │   │   └── CommandExecutor.php
    │   └── Broadcasting/
    │       └── MetricsChannel.php
    ├── routes/
    │   ├── api.php
    │   └── channels.php
    ├── config/
    │   ├── cors.php
    │   ├── sanctum.php
    │   └── reverb.php
    ├── .env
    └── artisan
```

## 🚀 Features

### Frontend (Web Dashboard)
- Real-time system monitoring via WebSocket
- Network detection (shows status based on Tailscale access)
- Remote control panel for Pi operations
- Token-based authentication
- Responsive design with Tailwind CSS

### Backend (Pi Service)
- Laravel API bound to Tailscale interface only
- Real-time WebSocket broadcasting (Laravel Reverb)
- System metrics collection (CPU, RAM, disk, temperature)
- Command execution with proper authorization
- Firewall-protected (tailscale0 interface only)

## 📋 Prerequisites

### For Frontend Development
- Node.js 18+ and npm
- Vercel account (for deployment)
- Access to Tailscale network (for testing)

### For Raspberry Pi Setup
- Raspberry Pi (any model with network connectivity)
- PHP 8.2+ and Composer
- Tailscale installed and configured
- SQLite3

## 🔧 Setup Instructions

### 1. Tailscale Setup

#### On Raspberry Pi:
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate and connect
sudo tailscale up

# Get your Tailscale IP
tailscale ip -4
# Example output: 100.101.102.103

# Optional: Set a hostname for easier access
# Go to Tailscale admin console → Machines → Set machine name
# Example: pi-monitor.tailnet-name.ts.net
```

#### On Your Development Machine:
```bash
# Install Tailscale
# Visit: https://tailscale.com/download

# Connect to same tailnet
tailscale up

# Verify connectivity
ping 100.101.102.103  # Use your Pi's Tailscale IP
```

### 2. Backend Setup (On Raspberry Pi)

```bash
# Install PHP and dependencies
sudo apt update
sudo apt install -y php8.2 php8.2-cli php8.2-mbstring php8.2-xml php8.2-curl \
                    php8.2-sqlite3 composer

# Create project directory
cd /opt
sudo mkdir pi-monitor
sudo chown $USER:$USER pi-monitor
cd pi-monitor

# Install Laravel
composer create-project laravel/laravel .

# Install additional packages
composer require laravel/sanctum
composer require laravel/reverb

# Set up environment
cp .env.example .env
php artisan key:generate

# Configure Tailscale binding
TAILSCALE_IP=$(tailscale ip -4)
echo "APP_URL=http://$TAILSCALE_IP" >> .env
echo "REVERB_HOST=$TAILSCALE_IP" >> .env
echo "REVERB_PORT=8080" >> .env

# Set up database
touch database/database.sqlite
php artisan migrate

# Install Sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate

# Generate API token (save this for frontend)
php artisan tinker
# In tinker:
# $user = User::factory()->create(['name' => 'admin', 'email' => 'admin@pi.local']);
# $token = $user->createToken('web-client')->plainTextToken;
# echo $token;
# exit
```

### 3. Configure CORS (Backend)

Edit `config/cors.php`:
```php
'paths' => ['api/*', 'sanctum/csrf-cookie', 'health', 'ws'],

'allowed_origins' => [
    'https://*.vercel.app',
    'http://localhost:3000', // Development
],

'supports_credentials' => true,
```

### 4. Set Up Firewall (Raspberry Pi)

```bash
# Install iptables-persistent
sudo apt install iptables-persistent

# Configure firewall rules
sudo iptables -F  # Clear existing rules

# Allow Tailscale interface
sudo iptables -A INPUT -i tailscale0 -j ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Drop everything else
sudo iptables -P INPUT DROP

# Save rules
sudo netfilter-persistent save

# Verify rules
sudo iptables -L -v
```

### 5. Create SystemD Service (Backend)

Create `/etc/systemd/system/pi-monitor.service`:
```ini
[Unit]
Description=Pi Monitor Laravel Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/pi-monitor
ExecStart=/usr/bin/php /opt/pi-monitor/artisan serve --host=100.x.x.x --port=8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable pi-monitor
sudo systemctl start pi-monitor

# Check status
sudo systemctl status pi-monitor
```

### 6. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local
nano .env.local
```

Add to `.env.local`:
```env
NEXT_PUBLIC_PI_HOST=pi-monitor.tailnet-name.ts.net
# OR use IP: NEXT_PUBLIC_PI_HOST=100.101.102.103:8000
NEXT_PUBLIC_PI_TOKEN=<token-from-backend-setup>
```

```bash
# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 7. Deploy Frontend to Vercel

```bash
# Push to GitHub
git add .
git commit -m "Initial commit"
git push origin master

# In Vercel dashboard:
# 1. Import repository
# 2. Add environment variables:
#    NEXT_PUBLIC_PI_HOST=pi-monitor.tailnet-name.ts.net
#    NEXT_PUBLIC_PI_TOKEN=<your-token>
# 3. Deploy
```

## 🧪 Testing the Setup

### Test 1: Health Check (Inside Tailscale)
```bash
# From your dev machine (connected to Tailscale)
curl http://100.x.x.x:8000/health
# Expected: {"status":"healthy"}
```

### Test 2: Health Check (Outside Tailscale)
```bash
# Disconnect from Tailscale
tailscale down

# Try health check
curl http://100.x.x.x:8000/health
# Expected: Connection timeout/refused (this is correct!)
```

### Test 3: Frontend Access
1. Open `https://your-app.vercel.app` (works for everyone)
2. Without Tailscale: See "Internal network required" message
3. With Tailscale: See full dashboard with live metrics

## 🔐 Security Features

### Network Layer
- **Firewall**: Only Tailscale interface allowed
- **No public IP exposure**: Backend is completely private
- **VPN-based access**: WireGuard encryption via Tailscale

### Application Layer
- **Token authentication**: Laravel Sanctum
- **CORS protection**: Only Vercel origins allowed
- **Rate limiting**: 60 requests/minute per token
- **Input validation**: All command inputs sanitized

### Deployment Layer
- **HTTPS everywhere**: Vercel provides automatic SSL
- **Environment variables**: Secrets never in code
- **Minimal attack surface**: Only health endpoint is unauthenticated
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


## 📚 Learning Resources

### Laravel Concepts Used
- **MVC Architecture**: Controllers for logic, Models for data
- **Middleware**: Request filtering and authentication
- **Service Container**: Dependency injection for clean code
- **Sanctum**: API token authentication
- **Broadcasting**: WebSocket events with Reverb
- **Artisan Commands**: CLI tools for maintenance

### Tailscale Concepts
- **WireGuard VPN**: Modern, fast VPN protocol
- **Mesh Network**: Direct peer-to-peer connections
- **MagicDNS**: Automatic hostname resolution
- **Interface Binding**: Restricting services to specific network interfaces
- **Zero Trust**: No implicit trust, even on private network

### Next Steps for Learning
1. **Add more commands**: Implement system updates, service restarts
2. **Database logging**: Store command history in SQLite
3. **User management**: Multiple users with different permissions
4. **Notifications**: Alert on high CPU/temp via WebSocket
5. **Charts**: Historical data visualization with Chart.js
6. **Mobile app**: Use same Laravel API with React Native

## 🐛 Troubleshooting

### Backend not accessible from Tailscale
```bash
# Check if Laravel is running
sudo systemctl status pi-monitor

# Check if it's bound to correct IP
sudo netstat -tlnp | grep 8000

# Verify Tailscale IP
tailscale ip -4

# Check firewall
sudo iptables -L -v
```

### WebSocket connection fails
```bash
# Ensure Reverb is running
php artisan reverb:start

# Check REVERB_HOST in .env matches Tailscale IP
grep REVERB .env

# Test WebSocket endpoint
wscat -c ws://100.x.x.x:8080/ws
```

### Frontend shows "Internal network only" when on Tailscale
```bash
# Verify you're connected
tailscale status

# Test health endpoint directly
curl http://100.x.x.x:8000/health

# Check browser console for CORS errors
# May need to update CORS config in Laravel
```

### Token authentication fails
```bash
# Regenerate token on Pi
php artisan tinker
# $user = User::first();
# $token = $user->createToken('new-token')->plainTextToken;
# echo $token;

# Update frontend .env.local with new token
# Redeploy to Vercel if needed
```

## 🎯 Why This Architecture?

### Learning Goals
- **Laravel ecosystem**: MVC, Eloquent, Sanctum, Reverb
- **Network security**: Tailscale VPN, firewall config, interface binding
- **Real-time communication**: WebSocket vs polling trade-offs
- **Full-stack separation**: Public UI + private API patterns
- **Zero-dependency deployment**: No cloud intermediary needed

### Production Benefits
- **No cloud costs**: No Firebase/AWS bills for data transfer
- **True privacy**: Data never leaves your network
- **No API limits**: Your own Pi, your own rules
- **Learning by doing**: Real infrastructure management

## 📄 License

MIT

## 🙏 Acknowledgments

- **Laravel**: Elegant PHP framework
- **Tailscale**: Zero-config VPN
- **Next.js**: React framework for production
- **Vercel**: Seamless deployment platform

---

*Built for learning Laravel, Tailscale, and modern web architecture. 🚀*
