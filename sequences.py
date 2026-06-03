"""
sequences.py — Email sequence logic using HTML templates.

Abandoned Cart:
  Step 1 → 1hr   — Gentle reminder + cart items
  Step 2 → 24hr  — Social proof + urgency
  Step 3 → 72hr  — 10% discount offer

Order Follow-Up:
  Day 1 → 24hr   — Order confirmation + tracking
  Day 3 → 3 days — Check-in + support
  Day 7 → 7 days — Review request + loyalty reward
"""

from datetime import datetime
from templates import (
    cart_step1, cart_step2, cart_step3,
    order_day1, order_day3, order_day7
)

# ── Brand Config — update per client ─────────────────────────────────────────
BRAND_NAME       = "Your Store"
BRAND_COLOR      = "#111111"       # swap to client's brand colour e.g. "#E63946"
UNSUBSCRIBE_URL  = "https://yourstore.com/unsubscribe"
REVIEW_BASE_URL  = "https://yourstore.com/review"
# ─────────────────────────────────────────────────────────────────────────────


# ── Abandoned Cart ─────────────────────────────────────────────────────────────

class AbandonedCartSequence:
    STEPS = [
        {"id": "step_1", "delay_hours": 1,  "subject": "you left something behind"},
        {"id": "step_2", "delay_hours": 24, "subject": "still thinking it over?"},
        {"id": "step_3", "delay_hours": 72, "subject": "here's 10% off — just for you"},
    ]

    def __init__(self, sender):
        self.sender = sender

    def should_trigger(self, cart):
        return self._get_next_step(cart) is not None

    def enqueue(self, cart):
        step = self._get_next_step(cart)
        if not step:
            return

        html = self._build_html(cart, step)

        self.sender.send(
            to_email  = cart["customer_email"],
            to_name   = cart["customer_name"],
            subject   = step["subject"],
            html_body = html,
            metadata  = {"cart_id": cart["cart_id"], "step": step["id"]},
        )
        cart["emails_sent"].append(step["id"])

    def _get_next_step(self, cart):
        hours_abandoned = (datetime.now() - cart["abandoned_at"]).total_seconds() / 3600
        for step in self.STEPS:
            if step["id"] not in cart["emails_sent"] and hours_abandoned >= step["delay_hours"]:
                return step
        return None

    def _build_html(self, cart, step):
        kwargs = dict(
            brand_name      = BRAND_NAME,
            brand_color     = BRAND_COLOR,
            customer_name   = cart["customer_name"],
            items           = cart["items"],
            cart_value      = cart["cart_value"],
            cart_url        = cart["cart_url"],
            unsubscribe_url = UNSUBSCRIBE_URL,
        )
        if step["id"] == "step_1":
            return cart_step1(**kwargs)
        elif step["id"] == "step_2":
            return cart_step2(**kwargs)
        elif step["id"] == "step_3":
            return cart_step3(**kwargs)


# ── Order Follow-Up ────────────────────────────────────────────────────────────

class OrderFollowUpSequence:
    STEPS = [
        {"id": "day_1", "delay_days": 1, "subject": "your order is confirmed!"},
        {"id": "day_3", "delay_days": 3, "subject": "how's everything going?"},
        {"id": "day_7", "delay_days": 7, "subject": "we'd love your review ⭐"},
    ]

    def __init__(self, sender):
        self.sender = sender

    def get_due_step(self, order):
        days_since = (datetime.now() - order["ordered_at"]).days
        for step in self.STEPS:
            if step["id"] not in order["emails_sent"] and days_since >= step["delay_days"]:
                return step
        return None

    def send_step(self, order, step):
        html = self._build_html(order, step)
        self.sender.send(
            to_email  = order["customer_email"],
            to_name   = order["customer_name"],
            subject   = step["subject"],
            html_body = html,
            metadata  = {"order_id": order["order_id"], "step": step["id"]},
        )
        order["emails_sent"].append(step["id"])

    def _build_html(self, order, step):
        if step["id"] == "day_1":
            return order_day1(
                brand_name      = BRAND_NAME,
                brand_color     = BRAND_COLOR,
                customer_name   = order["customer_name"],
                order_id        = order["order_id"],
                items           = order["items"],
                total           = order["total"],
                tracking_url    = order["tracking_url"],
                unsubscribe_url = UNSUBSCRIBE_URL,
            )
        elif step["id"] == "day_3":
            return order_day3(
                brand_name      = BRAND_NAME,
                brand_color     = BRAND_COLOR,
                customer_name   = order["customer_name"],
                tracking_url    = order["tracking_url"],
                unsubscribe_url = UNSUBSCRIBE_URL,
            )
        elif step["id"] == "day_7":
            return order_day7(
                brand_name      = BRAND_NAME,
                brand_color     = BRAND_COLOR,
                customer_name   = order["customer_name"],
                order_id        = order["order_id"],
                review_url      = f"{REVIEW_BASE_URL}/{order['order_id']}",
                unsubscribe_url = UNSUBSCRIBE_URL,
            )
