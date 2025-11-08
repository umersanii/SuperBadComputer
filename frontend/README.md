# Frontend - Pi Monitor Dashboard

Next.js web application for monitoring and controlling your Raspberry Pi.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Real-time Database**: Firebase Realtime Database
- **Deployment**: Vercel

## Getting Started

### Install Dependencies
```bash
npm install
```

### Configure Firebase
1. Copy the example environment file:
   ```bash
   cp .env.local.example .env.local
   ```

2. Edit `.env.local` with your Firebase credentials:
   ```env
   NEXT_PUBLIC_FIREBASE_API_KEY=your_key_here
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_domain_here
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id_here
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_bucket_here
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id_here
   NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id_here
   ```

### Run Development Server
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

### Build for Production
```bash
npm run build
npm run start
```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx       # Root layout with metadata
│   ├── page.tsx         # Home page with real-time monitoring
│   └── globals.css      # Global styles
│
├── components/
│   ├── PiStatus.tsx     # System status display component
│   └── ControlPanel.tsx # Control buttons component
│
└── lib/
    └── firebase.ts      # Firebase initialization
```

## Features

### Real-time Monitoring
- CPU usage percentage
- Memory usage percentage
- Disk usage percentage
- CPU temperature (°C)
- Connection status indicator
- Auto-updates every 5 seconds

### Remote Control
- Restart service
- Force status update
- Clear cache
- Shutdown (use with caution!)

## Firebase Integration

The app uses Firebase Realtime Database to:
1. Listen for status updates from the Pi (`pi/status`)
2. Send commands to the Pi (`pi/commands`)

### Data Flow
```
Pi Backend → Firebase → Next.js Frontend (Real-time)
Next.js Frontend → Firebase → Pi Backend (Commands)
```

## Deployment to Vercel

### Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variables when prompted
# Or add them later in Vercel dashboard
```

### Using GitHub Integration
1. Push code to GitHub
2. Import project in Vercel dashboard
3. Add environment variables
4. Deploy automatically on push

## Environment Variables

Add these in Vercel dashboard (Settings → Environment Variables):

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Firebase API Key |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Firebase Auth Domain |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Firebase Project ID |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Firebase Storage Bucket |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Firebase Sender ID |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | Firebase App ID |

## Customization

### Adding New Status Metrics
1. Add data collection in backend (`backend/app/main.py`)
2. Update `PiStatus.tsx` component to display new metrics
3. Update TypeScript interfaces if needed

### Adding New Commands
1. Add button in `ControlPanel.tsx`
2. Implement handler in backend (`backend/app/main.py`)

### Styling
The app uses Tailwind CSS. Modify classes in components or extend in `tailwind.config.ts`.

## Troubleshooting

**Page shows "Waiting for data..."**
- Check if backend service is running on Pi
- Verify Firebase database URL
- Check browser console for errors

**Commands not working**
- Check Firebase database rules
- Verify backend is listening for commands
- Check network connectivity

**Build errors**
- Delete `.next` folder and `node_modules`
- Run `npm install` again
- Check for TypeScript errors

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint for code quality |

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Firebase Realtime Database](https://firebase.google.com/docs/database)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vercel Deployment](https://vercel.com/docs)
