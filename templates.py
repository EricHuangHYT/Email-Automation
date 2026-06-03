"""
templates.py — HTML email templates for all 6 sequences.
Clean, branded, mobile-responsive, with CTA buttons and unsubscribe footer.
"""


def base_template(brand_name, brand_color, header_text, body_content, cta_text, cta_url, unsubscribe_url):
    """
    Master HTML wrapper used by every email.
    Swap brand_name, brand_color, and body_content per client.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{header_text}</title>
  <style>
    body {{ margin:0; padding:0; background:#f4f4f5; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; }}
    .wrapper {{ width:100%; background:#f4f4f5; padding:32px 0; }}
    .container {{ max-width:560px; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.08); }}
    .header {{ background:{brand_color}; padding:28px 40px; text-align:center; }}
    .header h1 {{ margin:0; color:#ffffff; font-size:20px; font-weight:600; letter-spacing:0.5px; }}
    .body {{ padding:36px 40px; }}
    .body h2 {{ font-size:22px; font-weight:600; color:#111; margin:0 0 12px; line-height:1.3; }}
    .body p {{ font-size:15px; color:#444; line-height:1.7; margin:0 0 20px; }}
    .items-box {{ background:#f9f9f9; border-radius:6px; padding:16px 20px; margin:0 0 24px; }}
    .item-row {{ display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #ececec; }}
    .item-row:last-child {{ border-bottom:none; }}
    .item-name {{ font-size:14px; color:#333; }}
    .item-price {{ font-size:14px; color:#111; font-weight:500; }}
    .cart-total {{ display:flex; justify-content:space-between; padding:12px 0 0; }}
    .cart-total span {{ font-size:15px; font-weight:600; color:#111; }}
    .cta-wrap {{ text-align:center; margin:28px 0; }}
    .cta-btn {{ display:inline-block; background:{brand_color}; color:#ffffff !important; text-decoration:none; font-size:15px; font-weight:600; padding:14px 36px; border-radius:6px; letter-spacing:0.3px; }}
    .discount-box {{ background:#fff8ec; border:1px solid #ffd97d; border-radius:6px; padding:14px 20px; text-align:center; margin:0 0 24px; }}
    .discount-code {{ font-size:22px; font-weight:700; color:#b45309; letter-spacing:2px; }}
    .discount-label {{ font-size:13px; color:#92400e; margin-top:4px; }}
    .divider {{ height:1px; background:#f0f0f0; margin:24px 0; }}
    .footer {{ background:#f9f9f9; padding:24px 40px; text-align:center; }}
    .footer p {{ font-size:12px; color:#999; margin:0 0 6px; line-height:1.6; }}
    .footer a {{ color:#999; text-decoration:underline; }}
    @media(max-width:600px){{
      .body {{ padding:24px 20px; }}
      .header {{ padding:20px; }}
      .footer {{ padding:20px; }}
    }}
  </style>
</head>
<body>
<div class="wrapper">
  <div class="container">
    <div class="header">
      <h1>{brand_name}</h1>
    </div>
    <div class="body">
      {body_content}
      <div class="cta-wrap">
        <a href="{cta_url}" class="cta-btn">{cta_text}</a>
      </div>
    </div>
    <div class="footer">
      <p>You're receiving this because you shopped at {brand_name}.</p>
      <p><a href="{unsubscribe_url}">Unsubscribe</a> &nbsp;·&nbsp; {brand_name}</p>
    </div>
  </div>
</div>
</body>
</html>"""


def items_html(items, cart_value):
    """Renders a product list inside the email."""
    rows = ""
    for item in items:
        rows += f"""
        <div class="item-row">
          <span class="item-name">{item['name']} &times; {item.get('qty', 1)}</span>
          <span class="item-price">${float(item['price']):.2f}</span>
        </div>"""
    return f"""
    <div class="items-box">
      {rows}
      <div class="cart-total">
        <span>Total</span>
        <span>${float(cart_value):.2f}</span>
      </div>
    </div>"""


# ── Abandoned Cart Templates ───────────────────────────────────────────────────

def cart_step1(brand_name, brand_color, customer_name, items, cart_value, cart_url, unsubscribe_url):
    body = f"""
      <h2>You left something behind, {customer_name}</h2>
      <p>No worries — your cart is saved and ready whenever you are.
         Here's what's waiting for you:</p>
      {items_html(items, cart_value)}
      <p style="font-size:14px;color:#888;">Stock is limited — we can't hold your cart forever.</p>"""
    return base_template(brand_name, brand_color,
        f"You left something behind",
        body, "Complete My Order →", cart_url, unsubscribe_url)


def cart_step2(brand_name, brand_color, customer_name, items, cart_value, cart_url, unsubscribe_url):
    body = f"""
      <h2>Still thinking it over?</h2>
      <p>Hi {customer_name}, your cart is still saved — but you're not the only one
         eyeing these items. Here's what others have been saying:</p>
      <div style="background:#f9f9f9;border-radius:6px;padding:16px 20px;margin:0 0 20px;">
        <p style="margin:0 0 10px;font-size:14px;color:#555;">⭐⭐⭐⭐⭐ &nbsp;<em>"Absolutely love it — shipping was fast and quality exceeded my expectations."</em></p>
        <p style="margin:0;font-size:14px;color:#555;">⭐⭐⭐⭐⭐ &nbsp;<em>"Bought this last month and already recommended it to three friends."</em></p>
      </div>
      {items_html(items, cart_value)}"""
    return base_template(brand_name, brand_color,
        "Still thinking it over?",
        body, "Go Back to My Cart →", cart_url, unsubscribe_url)


def cart_step3(brand_name, brand_color, customer_name, items, cart_value, cart_url, unsubscribe_url):
    discounted = cart_value * 0.9
    body = f"""
      <h2>A little something for you, {customer_name}</h2>
      <p>We'd hate for you to miss out. Here's an exclusive 10% discount
         on your cart — just for you:</p>
      <div class="discount-box">
        <div class="discount-code">COMEBACK10</div>
        <div class="discount-label">10% off your order · Expires in 24 hours</div>
      </div>
      {items_html(items, cart_value)}
      <p style="text-align:center;font-size:14px;color:#888;">
        Your total after discount: <strong>${discounted:.2f}</strong>
      </p>"""
    return base_template(brand_name, brand_color,
        "Here's 10% off — just for you",
        body, "Claim My Discount →", cart_url, unsubscribe_url)


# ── Order Follow-Up Templates ──────────────────────────────────────────────────

def order_day1(brand_name, brand_color, customer_name, order_id, items, total, tracking_url, unsubscribe_url):
    rows = "".join(f"<li style='padding:4px 0;font-size:14px;color:#444;'>{i['name']} &times; {i.get('qty',1)}</li>" for i in items)
    body = f"""
      <h2>Your order is confirmed! 🎉</h2>
      <p>Hi {customer_name}, thank you for your order. We're getting it
         packed up and ready to ship.</p>
      <div class="items-box">
        <p style="margin:0 0 10px;font-size:13px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:.05em;">Order #{order_id}</p>
        <ul style="margin:0;padding:0 0 0 16px;">{rows}</ul>
        <div class="cart-total"><span>Total</span><span>${float(total):.2f}</span></div>
      </div>
      <p>We'll send you tracking info as soon as your order ships.
         In the meantime, <a href="{tracking_url}" style="color:#333;">track your order here</a>.</p>
      <p style="font-size:14px;color:#888;">Questions? Just reply to this email — we're here to help.</p>"""
    return base_template(brand_name, brand_color,
        "Your order is confirmed!",
        body, "Track My Order →", tracking_url, unsubscribe_url)


def order_day3(brand_name, brand_color, customer_name, tracking_url, unsubscribe_url):
    body = f"""
      <h2>How's everything going, {customer_name}?</h2>
      <p>Your order should be arriving very soon (if it hasn't already).
         We hope you love it!</p>
      <div class="items-box" style="text-align:center;padding:20px;">
        <p style="margin:0;font-size:15px;color:#555;">Need to check on your delivery?</p>
      </div>
      <p>If anything isn't right with your order, just reply to this email
         and we'll make it right — no questions asked.</p>"""
    return base_template(brand_name, brand_color,
        "How's everything going?",
        body, "Track My Delivery →", tracking_url, unsubscribe_url)


def order_day7(brand_name, brand_color, customer_name, order_id, review_url, unsubscribe_url):
    body = f"""
      <h2>Loving it so far, {customer_name}?</h2>
      <p>It's been a week since your order arrived. We hope you're
         enjoying it! If you have 60 seconds, we'd love to hear what
         you think:</p>
      <div class="items-box" style="text-align:center;padding:24px 20px;">
        <p style="margin:0 0 6px;font-size:24px;">⭐⭐⭐⭐⭐</p>
        <p style="margin:0;font-size:14px;color:#666;">Your honest review helps other shoppers<br/>and means the world to us.</p>
      </div>
      <p style="text-align:center;font-size:14px;color:#888;">
        As a thank-you, we'll send you <strong>10% off your next order</strong>
        once your review goes live.
      </p>"""
    return base_template(brand_name, brand_color,
        "We'd love your review ⭐",
        body, "Leave a Review →", review_url, unsubscribe_url)
