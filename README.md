# 📦 Webhook Notify SGE

> **Real-time WhatsApp notifications for Enterprise Management System (ERP/SGE) product outflow events**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1+-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14+-A30000?style=flat-square)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 📋 About

**Webhook Notify SGE** is a production-ready REST API designed to bridge the gap between Enterprise Management Systems and real-time communication channels. It receives webhook events triggered by inventory movements (product outflows/sales) and instantly notifies stakeholders via WhatsApp, ensuring business owners and managers never miss a sale.

> 🔗 **Built to integrate with** [SGE Django Master](https://github.com/patresio/sge-django-master) - A complete Enterprise Management System built with Django.

### The Problem It Solves

In retail and inventory management, business owners often struggle to stay informed about sales activities in real-time. Traditional ERP/SGE systems provide reports, but lack instant notification capabilities. This gap leads to delayed decision-making and missed opportunities for timely business interventions.

### The Solution

This API acts as a **middleware notification layer** between your ERP system and communication channels:

1. **Receives webhooks** from any SGE/ERP system whenever a product outflow occurs
2. **Calculates business metrics** (total sale value, profit margins) automatically
3. **Sends instant WhatsApp notifications** to configured recipients
4. **Logs all events** for audit trails and business analytics

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔔 **Real-time WhatsApp Alerts** | Instant notifications via CallMeBot API integration |
| 📊 **Automatic Profit Calculation** | Computes sale value and profit margins from cost/selling prices |
| 💾 **Event Audit Logging** | Full persistence of all webhook events for compliance and analytics |
| 🔐 **JWT Authentication Ready** | Built-in support for secure API access with SimpleJWT |
| ⚙️ **12-Factor App Compliant** | Environment-based configuration for cloud-native deployments |
| 🗄️ **Database Agnostic** | Works with PostgreSQL, MySQL, SQLite via `dj-database-url` |

---

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph External Systems
        SGE[("🏢 ERP/SGE\nSystem")]
    end

    subgraph Webhook Notify SGE
        API["🌐 REST API\n(Django REST Framework)"]
        DB[("🗄️ Database\n(PostgreSQL)")]
        SVC["⚙️ CallMeBot\nService"]
    end

    subgraph Notifications
        WA["📱 WhatsApp"]
    end

    SGE -->|"POST /api/v1/webhooks/order/"| API
    API -->|"Store Event"| DB
    API -->|"Trigger"| SVC
    SVC -->|"Send Message"| WA
```

### Component Overview

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **API Layer** | Django REST Framework | Request validation, routing, response formatting |
| **Business Logic** | Python Services | Profit calculation, message templating |
| **Persistence** | Django ORM | Webhook event storage with UUID primary keys |
| **External Integration** | CallMeBot API | WhatsApp message delivery |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (recommended) or any supported database
- [CallMeBot API Key](https://www.callmebot.com/blog/free-api-whatsapp-messages/) for WhatsApp integration

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/webhook_notify_sge.git
cd webhook_notify_sge

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (see Configuration section)
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver 0.0.0.0:8001
```

### Your First API Call

```bash
curl -X POST http://localhost:8001/api/v1/webhooks/order/ \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "outflow",
    "system": "Store HQ",
    "product": "Premium T-Shirt",
    "quantity": 3,
    "product_selling_price": 59.90,
    "product_cost_price": 25.00
  }'
```

**Result:** A WhatsApp message is sent instantly with sale details and profit information!

---

## 📡 API Reference

### Webhook Order Endpoint

Receives product outflow events and triggers WhatsApp notifications.

```
POST /api/v1/webhooks/order/
Content-Type: application/json
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_type` | `string` | ✅ | Event type identifier (e.g., `"outflow"`) |
| `system` | `string` | ✅ | Source system name (e.g., `"Store HQ"`) |
| `product` | `string` | ✅ | Product name or SKU |
| `quantity` | `number` | ✅ | Quantity sold |
| `product_selling_price` | `number` | ✅ | Unit selling price |
| `product_cost_price` | `number` | ✅ | Unit cost price |

#### Request Example

```json
{
  "event_type": "outflow",
  "system": "Store HQ",
  "product": "Premium T-Shirt",
  "quantity": 3,
  "product_selling_price": 59.90,
  "product_cost_price": 25.00
}
```

#### Response

```json
{
  "event_type": "outflow",
  "system": "Store HQ",
  "product": "Premium T-Shirt",
  "quantity": 3,
  "product_selling_price": 59.90,
  "product_cost_price": 25.00
}
```

**Status Codes:**
- `200 OK` - Event processed successfully
- `400 Bad Request` - Invalid request payload

#### WhatsApp Notification Format

```
*Hello, a new outflow was registered at Store HQ*

Product: *Premium T-Shirt*
Quantity: *3*
Sale Value: *R$ 179.70*
Profit: *R$ 104.70*
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Core
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgres://user:password@localhost:5432/webhook_notify_sge

# CallMeBot WhatsApp Integration (Required)
CALLMEBOT_API_URL=https://api.callmebot.com/whatsapp.php
CALLMEBOT_PHONE_NUMBER=5511999999999
CALLMEBOT_API_KEY=your-callmebot-api-key

# Email Notifications (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_ADMIN_RECEIVER=admin@company.com
```

### Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key for cryptographic signing |
| `DEBUG` | ✅ | Enable debug mode (`True`/`False`) |
| `ALLOWED_HOSTS` | ✅ | Comma-separated list of allowed hostnames |
| `DATABASE_URL` | ✅ | Database connection URL |
| `CALLMEBOT_API_URL` | ✅ | CallMeBot API endpoint |
| `CALLMEBOT_PHONE_NUMBER` | ✅ | Recipient WhatsApp number |
| `CALLMEBOT_API_KEY` | ✅ | Your CallMeBot API key |
| `EMAIL_*` | ❌ | Optional email notification settings |

### CallMeBot Setup Guide

1. Add the CallMeBot number to your contacts: `+34 644 71 89 05`
2. Send this message via WhatsApp: `I allow callmebot to send me messages`
3. You'll receive your API key in the response
4. Configure the key in your `.env` file

📖 [Official CallMeBot Documentation](https://www.callmebot.com/blog/free-api-whatsapp-messages/)

---

## 📁 Project Structure

```
webhook_notify_sge/
├── app/                        # Django project configuration
│   ├── settings.py             # Application settings (12-factor compliant)
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point (async support)
├── webhooks/                   # Main application module
│   ├── models.py               # Webhook event model (UUID-based)
│   ├── views.py                # API views (WebhookOrderView)
│   ├── urls.py                 # API routing
│   ├── messages.py             # Notification message templates
│   ├── admin.py                # Django admin configuration
│   └── migrations/             # Database migrations
├── services/                   # External service integrations
│   └── callmebot.py            # CallMeBot API client
├── http/                       # HTTP client test files
│   └── test.http               # REST Client test requests
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🎯 Technical Highlights

> **For Recruiters and Technical Reviewers**

This project demonstrates proficiency in:

### Backend Development
- **Django REST Framework** - Building RESTful APIs with proper request/response handling
- **Class-Based Views** - Clean, reusable view architecture using `APIView`
- **Django ORM** - Database abstraction with UUID primary keys and ordering

### Software Engineering Practices
- **12-Factor App Principles** - Environment-based configuration via `python-decouple`
- **Service Layer Pattern** - External integrations encapsulated in dedicated service classes
- **Clean Architecture** - Separation between views, models, and services

### Integration & APIs
- **Webhook Consumption** - Designed as a webhook receiver for event-driven architectures
- **Third-Party API Integration** - CallMeBot WhatsApp API integration
- **RESTful Design** - Proper HTTP methods, status codes, and JSON payloads

### Production Readiness
- **Database URL Parsing** - Cloud-ready database configuration with `dj-database-url`
- **JWT Authentication Support** - Ready for secured endpoints with `djangorestframework-simplejwt`
- **WSGI/ASGI Support** - Compatible with production servers (Gunicorn, Daphne, etc.)

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Framework** | [Django](https://www.djangoproject.com/) | 5.1+ |
| **API** | [Django REST Framework](https://www.django-rest-framework.org/) | 3.14+ |
| **Authentication** | [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) | Latest |
| **Configuration** | [python-decouple](https://github.com/HBNetwork/python-decouple) | Latest |
| **Database Config** | [dj-database-url](https://github.com/jazzband/dj-database-url) | Latest |
| **HTTP Client** | [requests](https://requests.readthedocs.io/) | Latest |
| **Messaging** | [CallMeBot API](https://www.callmebot.com/) | External |

---

## 🧪 Testing

### Using REST Client (VS Code)

Install the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) and use the provided test file:

```http
# http/test.http
POST http://127.0.0.1:8001/api/v1/webhooks/order/
Content-Type: application/json

{
    "event_type": "outflow",
    "system": "Test Store",
    "product": "Test Product",
    "quantity": 1,
    "product_selling_price": 100.00,
    "product_cost_price": 50.00
}
```

### Using cURL

```bash
curl -X POST http://localhost:8001/api/v1/webhooks/order/ \
  -H "Content-Type: application/json" \
  -d '{"event_type":"outflow","system":"Test","product":"Item","quantity":1,"product_selling_price":100,"product_cost_price":50}'
```

---

## 🔗 Related Projects

| Project | Description |
|---------|-------------|
| [SGE Django Master](https://github.com/patresio/sge-django-master) | Complete Enterprise Management System (ERP) built with Django - the source system that triggers webhooks to this API |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Patrese**

- GitHub: [@patrese](https://github.com/patresio)

---

<p align="center">
  <sub>Built with ❤️ to automate sales notifications and empower real-time business insights</sub>
</p>
