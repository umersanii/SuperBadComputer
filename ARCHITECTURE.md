# System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S DEVICE                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Web Browser                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │        Next.js Frontend (Vercel)                     │  │ │
│  │  │  - Real-time Dashboard                               │  │ │
│  │  │  - Control Panel                                     │  │ │
│  │  │  - Status Display                                    │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FIREBASE (Cloud)                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Realtime Database                             │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │  pi/                                                 │  │ │
│  │  │    ├── status/     (Written by Pi, Read by Web)     │  │ │
│  │  │    │   ├── cpu: 45.2                                │  │ │
│  │  │    │   ├── memory: 62.8                             │  │ │
│  │  │    │   ├── disk: 34.5                               │  │ │
│  │  │    │   ├── temperature: 52.3                        │  │ │
│  │  │    │   ├── timestamp: 1699401234567                 │  │ │
│  │  │    │   └── online: true                             │  │ │
│  │  │    │                                                 │  │ │
│  │  │    └── commands/   (Written by Web, Read by Pi)     │  │ │
│  │  │        ├── command: "restart"                       │  │ │
│  │  │        └── timestamp: 1699401234567                 │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS (Admin SDK)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RASPBERRY PI (Local)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           Flask Backend Service (SystemD)                  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Background Threads:                                 │  │ │
│  │  │  1. Status Updater (every 5 sec)                     │  │ │
│  │  │     └─> Reads system stats                          │  │ │
│  │  │     └─> Writes to Firebase                          │  │ │
│  │  │                                                       │  │ │
│  │  │  2. Command Listener (real-time)                     │  │ │
│  │  │     └─> Listens to Firebase                         │  │ │
│  │  │     └─> Executes commands                           │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              │ System Calls                      │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                Operating System (Linux)                    │ │
│  │  - CPU metrics (psutil.cpu_percent)                        │ │
│  │  - Memory info (psutil.virtual_memory)                     │ │
│  │  - Disk usage (psutil.disk_usage)                          │ │
│  │  - Temperature (/sys/class/thermal/thermal_zone0/temp)    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Status Updates (Pi → Web)
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Raspberry Pi │────▶│   Firebase   │────▶│   Web App    │
│              │     │   Database   │     │              │
│ Flask Service│     │ (Realtime DB)│     │ Next.js      │
└──────────────┘     └──────────────┘     └──────────────┘
   Every 5 sec          Auto-sync           Live update
   
   Sends:                Stores:             Displays:
   • CPU usage           • Current           • Dashboard
   • Memory              • Status            • Graphs
   • Disk                • Timestamp         • Alerts
   • Temperature
```

### Commands (Web → Pi)
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Web App    │────▶│   Firebase   │────▶│ Raspberry Pi │
│              │     │   Database   │     │              │
│ Next.js      │     │ (Realtime DB)│     │ Flask Service│
└──────────────┘     └──────────────┘     └──────────────┘
  Button click         Write command       Execute action
   
   Sends:               Stores:             Executes:
   • restart            • Command           • Service restart
   • shutdown           • Timestamp         • System shutdown
   • update_status                          • Status update
   • clear_cache                            • Cache clear
```

## Component Interaction

### Frontend Components
```
┌────────────────────────────────────────────────────────┐
│                      page.tsx                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Main Page Component                             │  │
│  │  • Manages Firebase connection                   │  │
│  │  • Handles real-time updates                     │  │
│  │  • Manages application state                     │  │
│  │                                                   │  │
│  │  ┌────────────────────┐  ┌────────────────────┐  │  │
│  │  │   PiStatus.tsx     │  │ ControlPanel.tsx   │  │  │
│  │  │                    │  │                    │  │  │
│  │  │ • Display metrics  │  │ • Send commands    │  │  │
│  │  │ • Format data      │  │ • Handle clicks    │  │  │
│  │  │ • Show timestamp   │  │ • Loading states   │  │  │
│  │  └────────────────────┘  └────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
                          │
                          │ Uses
                          ▼
           ┌────────────────────────────┐
           │    lib/firebase.ts         │
           │  • Firebase initialization │
           │  • Database reference      │
           │  • Auth configuration      │
           └────────────────────────────┘
```

### Backend Components
```
┌────────────────────────────────────────────────────────┐
│                    app/main.py                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Flask Application                               │  │
│  │                                                   │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  Main Thread: Flask Server                 │  │  │
│  │  │  • HTTP endpoints (/health, /stats)        │  │  │
│  │  │  • CORS handling                           │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │                                                   │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  Thread 1: Status Updater                  │  │  │
│  │  │  • get_system_stats()                      │  │  │
│  │  │  • update_status_to_firebase()             │  │  │
│  │  │  • Runs every 5 seconds                    │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │                                                   │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  Thread 2: Command Listener                │  │  │
│  │  │  • listen_for_commands()                   │  │  │
│  │  │  • handle_command()                        │  │  │
│  │  │  • Real-time Firebase listener             │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
                          │
                          │ Uses
                          ▼
           ┌────────────────────────────┐
           │    Firebase Admin SDK      │
           │    psutil Library          │
           │    System APIs             │
           └────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL (Cloud)                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Next.js Application                                   │ │
│  │  • Automatic HTTPS                                     │ │
│  │  • CDN distribution                                    │ │
│  │  • Environment variables                               │ │
│  │  • Git-based deployment                                │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Firebase SDK
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  FIREBASE (Cloud)                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Realtime Database                                     │ │
│  │  • Data synchronization                                │ │
│  │  • Security rules                                      │ │
│  │  • Real-time listeners                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Admin SDK
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              RASPBERRY PI (Home Network)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  SystemD Service                                       │ │
│  │  • Auto-start on boot                                  │ │
│  │  │  Auto-restart on failure                           │ │
│  │  • Runs as background service                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend Stack
```
┌────────────────┐
│    React 18    │  Component library
├────────────────┤
│   Next.js 14   │  React framework
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
