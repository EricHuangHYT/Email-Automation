# 📧 E-Commerce Email Automation Engine

A Python-based email automation system for e-commerce stores.
Handles abandoned cart recovery and post-purchase follow-up sequences.

---

## ✨ What It Does

### Abandoned Cart Sequence
| Step   | Trigger              | Email                              |
|--------|----------------------|------------------------------------|
| Step 1 | 1 hr after abandon   | Gentle reminder with cart items    |
| Step 2 | 24 hrs after abandon | Social proof + urgency             |
| Step 3 | 72 hrs after abandon | 10% discount offer                 |

### Order Follow-Up Sequence
| Step  | Trigger          | Email                              |
|-------|------------------|------------------------------------|
| Day 1 | 24 hrs after buy | Order confirmation + tracking      |
| Day 3 | 3 days after buy | Check-in + support offer           |
| Day 7 | 7 days after buy | Review request + loyalty discount  |

---

## 🚀 Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run in demo mode (no emails sent — just previews)
python main.py

# 3. To go live, open main.py and set:
#    SENDGRID_API_KEY = "your_real_key"
#    DEMO_MODE = False
```

---

## 📁 Project Structure

```
email_automation/
├── main.py          # Orchestrator + scheduler
├── sequences.py     # Sequence logic & email copy
├── sender.py        # SendGrid integration
├── mock_data.py     # Fake data for demo/testing
├── requirements.txt
└── README.md
```

---

## 🔌 Going Live

1. Sign up for a free [SendGrid](https://sendgrid.com) account (100 emails/day free)
2. Create an API key in SendGrid dashboard
3. Set `SENDGRID_API_KEY` in `main.py`
4. Replace `mock_data.py` functions with real DB/API queries
5. Set `DEMO_MODE = False`
6. Deploy to a server (Railway, Render, or a $5 DigitalOcean droplet)

---

## 💰 Monetization

This system is the foundation of a freelance service you can offer to:
- Shopify store owners
- WooCommerce stores
- Any e-commerce business with an email list

**Typical project pricing:**
- Setup + sequences: $500–$1,500
- Monthly retainer (monitoring + optimization): $300–$800/mo
