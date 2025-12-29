# AutoPay Tracker 🚀

[![Django](https://img.shields.io/badge/Django-6.0-blue)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-green)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-CD-yellow)](https://github.com/features/actions)
[![Chrome Extension](https://img.shields.io/badge/Chrome_Extension-orange)](https://developer.chrome.com/docs/extensions/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-brightgreen)](https://autopay-tracker.onrender.com)

**Real-time subscription tracker that captures payments AT CHECKOUT** - before you forget them.

## 🎯 How It Works (Complete User Flow)

```
TWO WAYS TO ADD SUBSCRIPTIONS:

1. MANUAL ENTRY (Dashboard Forms)
   Dashboard → "Add Card" → "Add Subscription" → Instant save

2. AUTO CAPTURE (Chrome Extension)  
   Netflix Checkout → Type "4242 4242..." → Extension scrapes → Instant dashboard
```

```
┌────────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MANUAL ENTRY      │───▶│ Django REST API  │───▶│ PostgreSQL DB   │
│ Dashboard Forms     │    │ /api/cards/add/  │    │ cards table     │
│ (user types data)   │    │ /api/subs/add/   │    │ subs table      │
└────────────────────┘    └──────────────────┘    └─────────────────┘
                              ▲
                              │ Same API endpoints
                              │
                    ┌────────────────────┐
                    │   AUTO ENTRY       │
                    │ Chrome Extension   │
                    │ (scrapes checkout) │
                    └────────────────────┘
```

## 📱 Live Demo

**[Try it live → https://autopay-tracker.onrender.com](https://autopay-tracker.onrender.com)**

1. **Sign up** → Dashboard loads
2. **Manual**: Fill "Add Card" / "Add Subscription" forms
3. **Auto**: Install extension → Visit checkout demo → Watch magic!

## 🛠 Tech Stack

```
Frontend:     HTML/CSS/JS, Chrome Extension (Manifest V3)
Backend:      Django 6.0, Django REST Framework, PostgreSQL 16
DevOps:       Docker, docker-compose, GitHub Actions CI/CD
Deployment:   Render (auto-deploys on push to main)
```

## 🏗 Project Structure

```
autopay_tracker/
├── autopay_extension/                    # AUTO CAPTURE
│   ├── manifest.json                     # Targets: *://*/*checkout*
│   └── content.js                        # 20+ selectors (Stripe/forms)
├── payments/                             # Django app (MANUAL + AUTO)
│   ├── models.py                         # Card(last4, issuer, user), Subscription
│   ├── views.py                          # REST APIs: api_add_card(), api_add_subscription()
│   ├── templates/payments/dashboard.html # MANUAL forms + extension button
│   └── urls.py                           # /api/cards/add/, /extension/install/
├── config/                               # Django settings
├── Dockerfile                            # Python 3.13-slim
├── docker-compose.yml                    # web + db (Postgres 16)
├── .github/workflows/ci.yml              # Tests + Postgres service on push/PR
└── requirements.txt
```

## 🔍 Core Innovation: Dual Input System

### 1. **Manual Entry** (Dashboard)
```
POST /api/cards/add/
{ "name": "Primary Card", "last4": "4242", "issuer": "VISA" }

POST /api/subscriptions/add/
{ "service_name": "Netflix", "amount": 15.99, "frequency": "monthly" }
```

### 2. **Auto Capture** (Extension - content.js)
```javascript
// Runs ONLY on checkout pages
if (isCheckoutPage() && cardInput.value.length >= 13) {
  // Scrapes filled card field
  const card = {
    last4: cardInput.value.slice(-4),     // "4242"
    issuer: cardInput.value[0] === '4' ? 'VISA' : 'MC'
  };

  // SAME API endpoints as manual!
  fetch('/api/cards/add/', { body: JSON.stringify(card) });
  fetch('/api/subscriptions/add/', { 
    body: JSON.stringify({ service_name: document.title })
  });
}
```

**Extension permissions**: `["activeTab"]` only - reads DOM on checkout pages.

## 🧪 Quick Start

### Docker (Recommended - 2 min)
```bash
git clone <your-repo> && cd autopay_tracker
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
# Visit: http://localhost:8000
```

### Manual
```bash
python -m venv venv && source venv/bin/activate  # venv\Scripts\activate (Win)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Extension**: `chrome://extensions/` → Developer mode → Load unpacked → `autopay_extension/`

## 🚀 Why Different From Market?

| Feature | AutoPay Tracker | Rocket Money | TrackMySubs |
|---------|----------------|--------------|-------------|
| **Manual Entry** | ✅ Dashboard forms | ❌ Bank sync only | ✅ Manual |
| **Auto Capture** | ✅ Checkout (instant) | ❌ 45 days late | ❌ None |
| **Privacy** | ✅ Self-hosted | ❌ Bank login | ☁️ Cloud |
| **Cards** | ✅ `••••4242 VISA` | ❌ None | ❌ None |
| **Cost** | ✅ Free | ❌ $99/year | ❌ $10/mo |

## 🔮 Roadmap

- [x] Manual card/subscription forms
- [x] Auto checkout capture (20+ selectors)
- [x] Docker + CI/CD pipeline
- [ ] Email reminders (4 days before charge)
- [ ] AI savings advisor (OpenAI GPT-4o-mini)

## 🙌 Contributing

1. Fork → Clone
2. `docker-compose up` (full stack)
3. Tests: `docker-compose exec web python manage.py test`
4. Extension: Reload in `chrome://extensions/`
5. PR to `main`

## 📄 License

[MIT License](LICENSE) © 2025 **Bhavaraju Pavana Venkata Hari Naga Sai**

---

