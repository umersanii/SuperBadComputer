# Learning Resources

This document provides resources to help you understand and extend the Pi Monitor project.

## 🎓 Core Concepts

### 1. Next.js & React
- **Official Next.js Tutorial**: https://nextjs.org/learn
- **React Documentation**: https://react.dev/learn
- **Next.js App Router**: https://nextjs.org/docs/app
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/

**Key Concepts to Learn:**
- React Components and Props
- React Hooks (useState, useEffect)
- Next.js App Router
- Client vs Server Components
- TypeScript basics

### 2. Firebase Realtime Database
- **Get Started Guide**: https://firebase.google.com/docs/database/web/start
- **Structure Data**: https://firebase.google.com/docs/database/web/structure-data
- **Read and Write Data**: https://firebase.google.com/docs/database/web/read-and-write
- **Work with Lists**: https://firebase.google.com/docs/database/web/lists-of-data

**Key Concepts to Learn:**
- Real-time listeners
- Database structure design
- Security rules
- Read/Write operations
- Firebase Admin SDK (Python)

### 3. Flask (Python)
- **Flask Quickstart**: https://flask.palletsprojects.com/en/3.0.x/quickstart/
- **Flask Tutorial**: https://flask.palletsprojects.com/en/3.0.x/tutorial/
- **REST API with Flask**: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

**Key Concepts to Learn:**
- Flask routes and views
- Flask configuration
- Flask-CORS for cross-origin requests
- Background threading in Flask

### 4. System Monitoring (psutil)
- **psutil Documentation**: https://psutil.readthedocs.io/
- **Examples**: https://github.com/giampaolo/psutil/tree/master/scripts

**Key Concepts to Learn:**
- CPU monitoring
- Memory monitoring
- Disk usage
- Process management

### 5. Linux & Raspberry Pi
- **SystemD Services**: https://www.freedesktop.org/software/systemd/man/systemd.service.html
- **Raspberry Pi Documentation**: https://www.raspberrypi.org/documentation/
- **Linux Command Line Basics**: https://ubuntu.com/tutorials/command-line-for-beginners

**Key Concepts to Learn:**
- Creating SystemD services
- Managing services (systemctl)
- File permissions
- Environment variables

### 6. Tailwind CSS
- **Tailwind Documentation**: https://tailwindcss.com/docs
- **Tailwind with Next.js**: https://tailwindcss.com/docs/guides/nextjs

**Key Concepts to Learn:**
- Utility-first CSS
- Responsive design
- Dark mode
- Custom configurations

## 🛠️ Project-Specific Learning Paths

### Path 1: Frontend Developer
1. Learn React basics and hooks
2. Understand Next.js App Router
3. Learn Firebase client SDK
4. Study Tailwind CSS
5. Deploy to Vercel

**Practice Projects:**
- Build a todo app with Firebase
- Create a dashboard with real-time data
- Build a weather app with API

### Path 2: Backend Developer
1. Learn Python basics
2. Understand Flask framework
3. Learn Firebase Admin SDK
4. Study system monitoring with psutil
5. Learn Linux service management

**Practice Projects:**
- Build a REST API with Flask
- Create a system monitor CLI tool
- Build a task scheduler service

### Path 3: Full-Stack IoT Developer
1. Complete both paths above
2. Learn real-time communication patterns
3. Understand IoT architecture
4. Study security best practices
5. Learn deployment strategies

**Practice Projects:**
- This project! (You're already doing it)
- Add authentication
- Add data visualization
- Control GPIO pins

## 📚 Recommended Books

### Web Development
- "Learning React" by Alex Banks & Eve Porcello
- "Next.js Quick Start Guide" by Kirill Konshin
- "Flask Web Development" by Miguel Grinberg

### Python
- "Python Crash Course" by Eric Matthes
- "Automate the Boring Stuff with Python" by Al Sweigart

### IoT & Raspberry Pi
- "Raspberry Pi Cookbook" by Simon Monk
- "Internet of Things with Python" by Gaston Hillar

## 🎥 Video Tutorials

### Next.js
- Net Ninja Next.js Tutorial: https://www.youtube.com/playlist?list=PL4cUxeGkcC9g9gP2onazU5-2M-AzA8eBw
- Fireship Next.js in 100 Seconds: https://www.youtube.com/watch?v=Sklc_fQBmcs

### Flask
- Corey Schafer Flask Tutorial: https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
- Tech With Tim Flask Tutorial: https://www.youtube.com/watch?v=mqhxxeeTbu0

### Firebase
- Fireship Firebase Tutorial: https://www.youtube.com/watch?v=9kRgVxULbag
- Firebase Official Channel: https://www.youtube.com/c/Firebase

### Raspberry Pi
- Raspberry Pi Foundation: https://www.youtube.com/c/raspberrypi
- NetworkChuck Pi Projects: https://www.youtube.com/c/NetworkChuck

## 🔍 Deep Dive Topics

### Real-time Communication
- WebSockets vs Long Polling
- Server-Sent Events (SSE)
- Firebase Realtime Database architecture
- Pub/Sub patterns

### Security
- Firebase Security Rules
- Environment variables
- API authentication
- HTTPS/TLS
- CORS policies

### Deployment
- Vercel deployment
- Continuous Integration/Deployment
- Environment management
- Domain configuration

### Performance
- React optimization (memo, useMemo, useCallback)
- Next.js optimization (Image, Link)
- Database query optimization
- Caching strategies

## 💡 Extension Ideas & Learning Projects

### Beginner Extensions
1. **Add Charts**: Use Chart.js or Recharts to visualize data
2. **Add Alerts**: Email/SMS when CPU > 90%
3. **Theme Toggle**: Add light/dark mode switch
4. **More Metrics**: Network speed, running processes

### Intermediate Extensions
1. **User Authentication**: Add Firebase Auth
2. **Historical Data**: Store and display past 24 hours
3. **Multiple Devices**: Monitor multiple Pis
4. **GPIO Control**: Control LED/relay from dashboard
5. **Camera Stream**: Add Pi camera feed

### Advanced Extensions
1. **Mobile App**: React Native version
2. **Docker Containers**: Containerize the services
3. **Kubernetes**: Deploy at scale
4. **Machine Learning**: Predict failures
5. **Custom Alerts**: Complex alert rules engine

## 🤝 Community & Help

### Forums & Communities
- Stack Overflow: https://stackoverflow.com/
- Reddit /r/nextjs: https://reddit.com/r/nextjs
- Reddit /r/flask: https://reddit.com/r/flask
- Reddit /r/raspberry_pi: https://reddit.com/r/raspberry_pi
- Dev.to: https://dev.to/

### Official Discords
- Next.js Discord: https://nextjs.org/discord
- Reactiflux: https://www.reactiflux.com/

## 📝 Project Exercises

### Exercise 1: Add New Metric
Add "Uptime" metric that shows how long the Pi has been running.

**Steps:**
1. Use `psutil.boot_time()` in backend
2. Calculate uptime in seconds
3. Display in frontend (format as days:hours:minutes)

### Exercise 2: Command Confirmation
Add confirmation dialog before shutdown command.

**Steps:**
1. Use browser `confirm()` or create modal
2. Only send command if user confirms
3. Add loading state during execution

### Exercise 3: Historical Chart
Display CPU usage over last 10 data points.

**Steps:**
1. Store last 10 readings in component state
2. Install Chart.js or Recharts
3. Create line chart component
4. Update chart on new data

### Exercise 4: Email Alerts
Send email when CPU exceeds threshold.

**Steps:**
1. Install SendGrid or similar in backend
2. Check CPU in monitoring loop
3. Send email if threshold exceeded
4. Add cooldown to prevent spam

## 🎯 Learning Checklist

Use this to track your learning progress:

### Frontend
- [ ] Created a React component
- [ ] Used useState and useEffect hooks
- [ ] Connected to Firebase from web app
- [ ] Styled with Tailwind CSS
- [ ] Deployed to Vercel
- [ ] Added environment variables
- [ ] Handled loading states
- [ ] Implemented error handling

### Backend
- [ ] Created a Flask route
- [ ] Connected to Firebase Admin SDK
- [ ] Used psutil for system monitoring
- [ ] Implemented background threading
- [ ] Created a SystemD service
- [ ] Handled exceptions properly
- [ ] Set up logging
- [ ] Managed environment variables

### DevOps
- [ ] Used Git for version control
- [ ] Created .gitignore file
- [ ] Set up continuous deployment
- [ ] Managed secrets securely
- [ ] Configured domain (optional)
- [ ] Set up monitoring/logging

## 📖 Glossary

- **IoT**: Internet of Things - network of physical devices
- **Real-time Database**: Database that syncs data instantly
- **API**: Application Programming Interface
- **REST**: Representational State Transfer
- **CORS**: Cross-Origin Resource Sharing
- **SystemD**: Linux system and service manager
- **Virtual Environment**: Isolated Python environment
- **SSR**: Server-Side Rendering
- **CSR**: Client-Side Rendering
- **WebSocket**: Protocol for real-time communication

## 🚀 Next Steps

1. **Build the Project**: Follow the setup instructions
2. **Experiment**: Break things and fix them
3. **Add Features**: Pick an extension idea and implement it
4. **Share**: Deploy and show your friends
5. **Learn More**: Pick a deep dive topic
6. **Contribute**: Help others with similar projects

Remember: The best way to learn is by building! Don't be afraid to experiment and make mistakes.
