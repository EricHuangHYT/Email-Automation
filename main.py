"""
E-Commerce Email Automation Engine
===================================
Demo project showcasing abandoned cart + order follow-up automation.
Plug in your SendGrid API key and point at a real customer list to go live.
"""

import schedule
import time
from datetime import datetime
from mock_data import get_abandoned_carts, get_recent_orders
from sequences import AbandonedCartSequence, OrderFollowUpSequence
from sender import EmailSender
from dotenv import load_dotenv
import os

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL       = os.getenv("FROM_EMAIL")
FROM_NAME        = os.getenv("FROM_NAME")
DEMO_MODE        = os.getenv("DEMO_MODE", "False") == "True"

def run_abandoned_cart_check():
    """
    Fires every hour. Finds carts abandoned > 1 hour ago and
    hasn't received an email yet, then kicks off the sequence.
    """
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛒  Checking for abandoned carts...")

    sender   = EmailSender(SENDGRID_API_KEY, FROM_EMAIL, FROM_NAME, demo=DEMO_MODE)
    sequence = AbandonedCartSequence(sender)
    carts    = get_abandoned_carts()

    triggered = 0
    for cart in carts:
        if sequence.should_trigger(cart):
            sequence.enqueue(cart)
            triggered += 1

    print(f"    → {triggered} cart(s) entered the sequence.")


def run_order_followup_check():
    """
    Fires every hour. Sends post-purchase follow-ups at
    day 1, day 3, and day 7 after an order is placed.
    """
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📦  Checking for order follow-ups...")

    sender   = EmailSender(SENDGRID_API_KEY, FROM_EMAIL, FROM_NAME, demo=DEMO_MODE)
    sequence = OrderFollowUpSequence(sender)
    orders   = get_recent_orders()

    triggered = 0
    for order in orders:
        step = sequence.get_due_step(order)
        if step:
            sequence.send_step(order, step)
            triggered += 1

    print(f"    → {triggered} follow-up(s) sent.")


def main():
    print("=" * 55)
    print("  📧  E-Commerce Email Automation Engine  ")
    print(f"  Mode: {'DEMO (no emails sent)' if DEMO_MODE else '🔴 LIVE'}")
    print("=" * 55)

    # Run immediately on startup so you see output right away
    run_abandoned_cart_check()
    run_order_followup_check()

    # Then schedule recurring checks
    schedule.every(1).hour.do(run_abandoned_cart_check)
    schedule.every(1).hour.do(run_order_followup_check)

    print("\n⏰  Scheduler running. Checks fire every hour.")
    print("    Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
