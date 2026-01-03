1# System Architecture

## Architecture Overview

**Goal:** Public React frontend (Vercel) + Private Laravel API (Tailscale) + Zero Firebase dependency

**Security Model:**
- 🌐 **Public layer**: Next.js UI hosted on Vercel (accessible to anyone)
- 🔒 **Private layer**: Laravel API on Pi (Tailscale network only)
- 🚫 **No intermediary**: Direct WebSocket connection (no Firebase/cloud proxy)

## Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERNET (Public)                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Vercel Edge Network                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │     Next.js Frontend (PUBLIC)                        │  │ │
│  │  │  • Loads for everyone                                │  │ │
│  │  │  • Health check on mount                             │  │ │
│  │  │  • Shows "Internal Network Only" if unreachable      │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/WSS
                              │ (Only works inside Tailscale)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TAILSCALE NETWORK (Private)                      │
│                      100.x.x.x subnet                            │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Raspberry Pi (100.x.x.x)                      │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Laravel API (PRIVATE - tailscale0 only)            │  │ │
│  │  │                                                       │  │ │
│  │  │  📍 Bound to: tailscale0 interface only             │  │ │
│  │  │  🔐 Auth: Sanctum/JWT token-based                   │  │ │
│  │  │  🔥 Firewall: DROP all except tailscale0            │  │ │
│  │  │                                                       │  │ │
│  │  │  Endpoints:                                          │  │ │
│  │  │  • GET  /health          → Service status           │  │ │
│  │  │  • GET  /api/stats       → System metrics           │  │ │
│  │  │  • POST /api/command     → Execute Pi operations    │  │ │
│  │  │  • WS   /ws              → Real-time WebSocket      │  │ │
│  │  │                                                       │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                              │                              │ │
│  │                              │ System calls                 │ │
│  │                              ▼                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │           Operating System (Linux)                   │  │ │
│  │  │  • CPU/RAM/Disk metrics                             │  │ │
│  │  │  • Temperature sensors                               │  │ │
│  │  │  • systemctl service control                        │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  🔧 Admin Access:                                                │
│  • SSH over Tailscale (full control)                            │
│  • Optional: Cockpit/Netdata (Tailscale-only)                   │
└─────────────────────────────────────────────────────────────────┘
```


## Data Flow

### 1. Initial Load (Network Detection)

```
User opens https://pi-monitor.vercel.app
         │
         ├─ Frontend loads (always succeeds - public Vercel)
         │
         └─> Immediately calls GET https://100.x.x.x/health
                │
                ├─ ✅ SUCCESS (inside Tailscale)
                │   └─> Open WebSocket connection
                │       └─> Show full dashboard
                │
                └─ ❌ FAILURE (outside Tailscale)
                    └─> Show message: "This app requires internal network access"
                    └─> Display offline state
```

### 2. Real-time Metrics (WebSocket)

```
┌──────────────┐                    ┌──────────────┐
│   Frontend   │◄──────────────────►│  Laravel API │
│  (Browser)   │    WebSocket       │   (Pi)       │
└──────────────┘    ws://100.x.x.x  └──────────────┘
                        /ws                 │
                                           │
  Every 3 seconds:                         │ System calls
  ◄─ { cpu: 45.2,                         │
       memory: 62.8,                       ▼
       disk: 34.5,               ┌─────────────────┐
       temp: 52.3,               │   Linux Kernel  │
       timestamp }               │   • CPU stats   │
                                 │   • RAM usage   │
                                 │   • Disk I/O    │
                                 │   • Thermal     │
                                 └─────────────────┘
```

### 3. Command Execution (HTTP POST)

```
┌──────────────┐                    ┌──────────────┐
│   Frontend   │                    │  Laravel API │
│              │                    │              │
│  [Restart]   │───────────────────►│  Validates   │
│   Button     │  POST /api/command │  JWT token   │
│              │  { cmd: "restart", │              │
│              │    token: "..." }  │  Executes    │
│              │                    │  systemctl   │
│              │                    │              │
│              │◄───────────────────│  Returns     │
│  Shows       │  { success: true,  │  response    │
│  feedback    │    message: "..." }│              │
└──────────────┘                    └──────────────┘
```

## Security Layers

### Network Layer
```
iptables rules on Pi:

# Default: DENY ALL
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow Tailscale interface ONLY
iptables -A INPUT -i tailscale0 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# Block everything else
iptables -A INPUT -j DROP
```

### Application Layer (Laravel)
```php
// config/cors.php
'allowed_origins' => [
    'https://*.vercel.app',
    'http://localhost:3000', // Dev only
],

// Middleware stack
Route::middleware(['auth:sanctum', 'throttle:60,1'])->group(function () {
    Route::get('/api/stats', [StatsController::class, 'index']);
    Route::post('/api/command', [CommandController::class, 'execute']);
});

Route::get('/health', [HealthController::class, 'check']); // No auth
```

### Authentication Flow
```
1. Initial Setup (via SSH):
   $ php artisan tinker
   >>> User::factory()->create(['name' => 'admin'])
   >>> $token = $user->createToken('web-client')->plainTextToken
   >>> // Copy this token

2. Frontend stores token:
   localStorage.setItem('pi_token', 'xxx|yyy...')

3. Every request includes:
   Authorization: Bearer xxx|yyy...

4. Laravel validates via Sanctum middleware
```

## Failure Modes & Handling

| Scenario | Frontend Behavior | Backend State |
|----------|------------------|---------------|
| Outside Tailscale | Shows "Internal network only" message | Unreachable (by design) |
| Inside Tailscale, Pi offline | Shows "Pi is offline" | N/A |
| Inside Tailscale, Pi online | Full functionality | Processing requests |
| Invalid/expired token | Shows "Authentication required" | Returns 401 |
| Command fails | Shows error toast | Logs error, returns 500 |
| WebSocket disconnects | Attempts reconnect (3x), then shows disconnected | Closes connection |

## Technology Stack

### Frontend (Public)
- **Framework**: Next.js 14+ (React, TypeScript)
- **Hosting**: Vercel (Edge network, automatic HTTPS)
- **Styling**: Tailwind CSS
- **Real-time**: Native WebSocket API
- **State**: React hooks (useState, useEffect, useRef)
- **Auth**: localStorage for token persistence

### Backend (Tailscale-only)
- **Framework**: Laravel 11+ (PHP 8.2+)
- **API**: RESTful + WebSocket (Laravel Reverb/Soketi)
- **Auth**: Laravel Sanctum (token-based)
- **Database**: SQLite (lightweight, perfect for Pi)
- **Metrics**: PHP system functions + Laravel commands
- **Service**: SystemD unit

### Infrastructure
- **Network**: Tailscale (WireGuard-based VPN)
- **Firewall**: iptables (interface-specific rules)
- **Reverse Proxy**: Nginx (optional, for SSL termination)
- **Process Manager**: SystemD
- **Server**: Raspberry Pi (any model with network)

## Component Structure

### Frontend Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main dashboard with health check
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   ├── PiStatus.tsx          # Real-time metrics display
│   │   ├── ControlPanel.tsx      # Command buttons
│   │   ├── NetworkGuard.tsx      # "Internal only" message
│   │   └── WebSocketProvider.tsx # WebSocket connection manager
│   ├── lib/
│   │   ├── api.ts                # HTTP client (health, commands)
│   │   ├── websocket.ts          # WebSocket connection logic
│   │   └── auth.ts               # Token management
│   └── types/
│       └── index.ts              # TypeScript interfaces
├── .env.local
│   # NEXT_PUBLIC_PI_HOST=100.x.x.x or pi-name.tailnet.ts.net
│   # NEXT_PUBLIC_PI_TOKEN=xxx|yyy...
└── next.config.js
```

### Backend Structure (Laravel)
```
backend/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── HealthController.php      # GET /health
│   │   │   ├── StatsController.php       # GET /api/stats
│   │   │   └── CommandController.php     # POST /api/command
│   │   └── Middleware/
│   │       └── EnsureTailscaleRequest.php # Verify tailscale0 source
│   ├── Services/
│   │   ├── SystemMetricsService.php      # CPU/RAM/Disk/Temp
│   │   └── CommandExecutor.php           # systemctl wrapper
│   └── Broadcasting/
│       └── MetricsChannel.php            # WebSocket /ws channel
├── routes/
│   ├── web.php
│   ├── api.php                           # API routes
│   └── channels.php                      # WebSocket channels
├── config/
│   ├── cors.php                          # Vercel origins
│   ├── sanctum.php                       # Token auth
│   └── reverb.php                        # WebSocket config
├── database/
│   └── database.sqlite                   # Local DB
├── .env
│   # APP_URL=http://100.x.x.x
│   # REVERB_HOST=100.x.x.x
│   # REVERB_PORT=8080
└── artisan                               # CLI tool
```

## Deployment Workflow

### Frontend Deployment
```bash
# 1. Set environment variables in Vercel dashboard
NEXT_PUBLIC_PI_HOST=pi-monitor.tailnet-name.ts.net
NEXT_PUBLIC_PI_TOKEN=<generated-token>

# 2. Push to GitHub (auto-deploys to Vercel)
git push origin master

# 3. Vercel builds and deploys
# Result: https://pi-monitor.vercel.app (public)
```

### Backend Deployment (Pi)
```bash
# 1. Install Laravel on Pi
cd /opt
sudo composer create-project laravel/laravel pi-monitor

# 2. Configure binding to Tailscale IP
# Edit /opt/pi-monitor/.env
APP_URL=http://$(tailscale ip -4)
REVERB_HOST=$(tailscale ip -4)

# 3. Set up SystemD service
sudo nano /etc/systemd/system/pi-monitor.service
# [Service]
# ExecStart=/usr/bin/php /opt/pi-monitor/artisan serve --host=$(tailscale ip -4)

# 4. Start service
sudo systemctl enable pi-monitor
sudo systemctl start pi-monitor

# 5. Configure firewall
sudo iptables -A INPUT -i tailscale0 -j ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -P INPUT DROP
sudo netfilter-persistent save
```

## Learning Objectives (Why This Stack?)

### Laravel Learning Goals
- **MVC Pattern**: Controllers, routes, middleware
- **Authentication**: Sanctum token-based auth
- **Real-time**: WebSocket broadcasting (Reverb)
- **API Development**: RESTful design patterns
- **Deployment**: SystemD, production config

### Tailscale Learning Goals
- **Zero Trust Networking**: Identity-based access
- **Network Interface Binding**: `tailscale0` isolation
- **Firewall Management**: iptables per-interface rules
- **Private Services**: Exposing APIs without public IPs

### Full-stack Integration
- **Public/Private Split**: Vercel (public) + Tailscale (private)
- **Graceful Degradation**: Works outside, disabled outside network
- **WebSocket**: Direct browser-to-server real-time communication
- **Security**: Multiple layers (network, firewall, app auth)

---

*This architecture prioritizes learning Laravel, Tailscale, and WebSocket technologies while maintaining production-grade security through network isolation.*
├────────────────┤
│  TypeScript    │  Type safety
├────────────────┤
│  Tailwind CSS  │  Styling
├────────────────┤
│ Firebase SDK   │  Database client
└────────────────┘
```

### Backend Stack
```
┌────────────────┐
│    Python 3    │  Programming language
├────────────────┤
│     Flask      │  Web framework
├────────────────┤
│ Firebase Admin │  Database server SDK
├────────────────┤
│    psutil      │  System monitoring
├────────────────┤
│    SystemD     │  Service management
└────────────────┘
```

## Security Layers

```
┌────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                              │
│  • HTTPS encryption                                    │
│  • Firebase authentication (optional)                  │
│  • Environment variable protection                     │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│ Layer 2: Application Security                          │
│  • Firebase security rules                             │
│  • Input validation                                    │
│  • CORS policies                                       │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│ Layer 3: System Security                               │
│  • Limited user permissions                            │
│  • File permission controls                            │
│  • SystemD isolation                                   │
└────────────────────────────────────────────────────────┘
```

## Performance Characteristics

- **Frontend Response Time**: < 100ms (local state)
- **Firebase Sync Latency**: 100-500ms (real-time)
- **Backend Update Interval**: 5 seconds (configurable)
- **Command Execution**: Near real-time (< 1 second)
- **Resource Usage (Pi)**: ~1-2% CPU, ~50-100MB RAM
