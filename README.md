---
title: AgroVision AI
emoji: 🌱
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 7860
pinned: false
---

# 🌱 AgroVision AI

**AI-Powered Smart Agriculture Platform for Uzbekistan**

AgroVision AI is a full-stack platform that uses computer vision and deep learning to help Uzbekistan's farmers identify plants, detect diseases, and get smart crop recommendations.

![Tech Stack](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-blue?logo=tailwindcss)

---

## 🚀 Features

### 🌿 Plant Detection
Upload a plant image → YOLOv8 AI identifies the species with confidence score, growing info, and suitable Uzbekistan regions.

### 🦠 Disease Analysis
Upload a leaf/fruit image → EfficientNet classifies diseases with severity level, causes, treatment recommendations, and prevention tips.

### 🏔️ Land Analysis
Upload a land image → OpenCV analyzes soil conditions and recommends optimal crops, irrigation strategies, and farming suggestions.

### 🗺️ Region Intelligence
Interactive data for all 14 Uzbekistan regions with climate info, soil types, main crops, and agricultural statistics.

### 🛡️ Admin Panel
Monitor AI performance, manage analysis logs, track uploaded images, and oversee user activity.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, TailwindCSS v4, Framer Motion |
| Backend | FastAPI, Python 3.12+ |
| AI Models | YOLOv8, EfficientNet, OpenCV |
| Database | Supabase PostgreSQL |
| Image CDN | Cloudinary |
| Weather | OpenWeather API |
| Maps | Leaflet.js |

---

## 📁 Project Structure

```
agro-vision-ai/
├── frontend/          # Next.js 15 (App Router)
│   └── src/
│       ├── app/       # Pages (landing, dashboard, disease, land, regions, admin)
│       ├── components/ # Reusable UI components
│       ├── lib/       # API client, utilities
│       └── types/     # TypeScript definitions
├── backend/           # FastAPI
│   └── app/
│       ├── api/v1/    # API endpoints
│       ├── core/      # Config, security
│       └── services/  # AI & business logic
├── database/          # SQL schema
└── .gitignore
```

---

## 🛠️ Getting Started

### Prerequisites
- Node.js 20+
- Python 3.12+
- npm

### Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/plant/detect` | POST | Plant detection from image |
| `/api/v1/disease/analyze` | POST | Disease classification from image |
| `/api/v1/recommend/crops` | POST | Crop recommendations from land image |
| `/api/v1/weather/{region}` | GET | Weather data for region |
| `/api/v1/regions` | GET | All Uzbekistan regions |
| `/api/v1/admin/stats` | GET | Platform statistics |
| `/api/v1/admin/logs` | GET | AI analysis logs |
| `/api/v1/admin/users` | GET | User management |
| `/api/v1/upload/image` | POST | Image upload (Cloudinary) |

---

## 🎨 Design Philosophy

- **Eco-tech dark theme** with green glow accents (#00FF88)
- **Glassmorphism** UI with backdrop blur effects
- **Framer Motion** animations throughout
- **Mobile-first** responsive design
- Inspired by Tesla + NVIDIA + modern AI SaaS aesthetics

---

## 📄 License

MIT License — Built with ❤️ for Uzbekistan's agricultural future.
