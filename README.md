# 📦 Webhook Notify SGE

Sistema de notificação em tempo real para eventos de saída de produtos, integrado com WhatsApp.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)

---

## 📋 Sobre

**Webhook Notify SGE** é uma API REST que recebe webhooks de sistemas de gestão empresarial (SGE) e envia notificações instantâneas via WhatsApp sempre que uma saída de produto é registrada. O sistema calcula automaticamente o valor total da venda e o lucro gerado.

### ✨ Recursos Principais

- 🔔 **Notificações WhatsApp em tempo real** via CallMeBot API
- 📊 **Cálculo automático** de valor de venda e lucro
- 💾 **Registro de eventos** em banco de dados para auditoria
- 🔐 **Autenticação JWT** para segurança da API
- ⚙️ **Configuração via variáveis de ambiente** para deploy flexível

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- Conta CallMeBot configurada ([instruções](https://www.callmebot.com/blog/free-api-whatsapp-messages/))
- Banco de dados (PostgreSQL recomendado)

### 1. Clone e configure

```bash
git clone https://github.com/seu-usuario/webhook_notify_sge.git
cd webhook_notify_sge
```

### 2. Ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### 3. Dependências

```bash
pip install -r requirements.txt
```

### 4. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/webhook_notify_sge

# CallMeBot (WhatsApp)
CALLMEBOT_API_URL=https://api.callmebot.com/whatsapp.php
CALLMEBOT_PHONE_NUMBER=5511999999999
CALLMEBOT_API_KEY=sua-api-key

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_ADMIN_RECEIVER=admin@empresa.com
```

### 5. Banco de dados

```bash
python manage.py migrate
python manage.py createsuperuser  # opcional
```

### 6. Executar

```bash
python manage.py runserver 0.0.0.0:8001
```

---

## 📡 API

### Endpoint Principal

```
POST /api/v1/webhooks/order/
```

### Request Body

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `event_type` | string | Tipo do evento (ex: `"outflow"`) |
| `system` | string | Nome do sistema origem (ex: `"SGE"`) |
| `product` | string | Nome do produto |
| `quantity` | number | Quantidade vendida |
| `product_selling_price` | number | Preço de venda unitário |
| `product_cost_price` | number | Preço de custo unitário |

### Exemplo de Request

```json
{
  "event_type": "outflow",
  "system": "SGE Loja 01",
  "product": "Camiseta Básica",
  "quantity": 3,
  "product_selling_price": 59.90,
  "product_cost_price": 25.00
}
```

### Exemplo via cURL

```bash
curl -X POST http://localhost:8001/api/v1/webhooks/order/ \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "outflow",
    "system": "SGE Loja 01",
    "product": "Camiseta Básica",
    "quantity": 3,
    "product_selling_price": 59.90,
    "product_cost_price": 25.00
  }'
```

### Notificação WhatsApp

A mensagem enviada segue o formato:

```
*Olá, uma nova saída foi registrada no SGE Loja 01*

Produto: *Camiseta Básica*
Quantidade: *3*
Valor da venda: *R$ 179.70*
Lucro da venda: *R$ 104.70*
```

---

## 📁 Estrutura do Projeto

```
webhook_notify_sge/
├── app/                    # Configurações Django
│   ├── settings.py         # Configurações principais
│   ├── urls.py             # URLs raiz
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── webhooks/               # App principal
│   ├── models.py           # Modelo Webhook
│   ├── views.py            # WebhookOrderView
│   ├── urls.py             # Rotas da API
│   └── messages.py         # Templates de mensagens
├── services/               # Integrações externas
│   └── callmebot.py        # Cliente CallMeBot API
├── http/                   # Testes HTTP
│   └── test.http           # Requests de teste (REST Client)
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `SECRET_KEY` | Chave secreta Django | ✅ |
| `DEBUG` | Modo debug | ✅ |
| `ALLOWED_HOSTS` | Hosts permitidos (CSV) | ✅ |
| `DATABASE_URL` | URL de conexão do banco | ✅ |
| `CALLMEBOT_API_URL` | URL da API CallMeBot | ✅ |
| `CALLMEBOT_PHONE_NUMBER` | Número WhatsApp destino | ✅ |
| `CALLMEBOT_API_KEY` | API Key CallMeBot | ✅ |
| `EMAIL_HOST` | Servidor SMTP | ❌ |
| `EMAIL_PORT` | Porta SMTP | ❌ |
| `EMAIL_HOST_USER` | Usuário SMTP | ❌ |
| `EMAIL_HOST_PASSWORD` | Senha SMTP | ❌ |
| `EMAIL_USE_TLS` | Usar TLS | ❌ |
| `EMAIL_USE_SSL` | Usar SSL | ❌ |
| `EMAIL_ADMIN_RECEIVER` | Email do admin | ❌ |

### CallMeBot Setup

1. Acesse [CallMeBot WhatsApp API](https://www.callmebot.com/blog/free-api-whatsapp-messages/)
2. Adicione o número do CallMeBot aos contatos: `+34 644 71 89 05`
3. Envie a mensagem: `I allow callmebot to send me messages`
4. Você receberá sua API Key
5. Configure as variáveis no `.env`

---

## 🧪 Testes

### Teste via REST Client (VS Code)

Use o arquivo `http/test.http` com a extensão REST Client:

```http
POST http://127.0.0.1:8001/api/v1/webhooks/order/
Content-Type: application/json

{
    "event_type": "outflow",
    "system": "SGE Teste",
    "product": "Produto Teste",
    "quantity": 1,
    "product_selling_price": 100.00,
    "product_cost_price": 50.00
}
```

---

## 🛠️ Tecnologias

- **[Django 5.1](https://www.djangoproject.com/)** - Framework web
- **[Django REST Framework](https://www.django-rest-framework.org/)** - API REST
- **[djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)** - Autenticação JWT
- **[python-decouple](https://github.com/HBNetwork/python-decouple)** - Variáveis de ambiente
- **[dj-database-url](https://github.com/jazzband/dj-database-url)** - Configuração de banco
- **[CallMeBot API](https://www.callmebot.com/)** - Notificações WhatsApp

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

Desenvolvido por **Patrese**

---

<p align="center">
  <sub>Feito com ❤️ para automatizar notificações de vendas</sub>
</p>
