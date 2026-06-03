"""
sender.py — Handles email delivery via SendGrid.
Supports HTML emails. Demo mode saves previews as .html files you can open in a browser.
"""

import json
import os
from datetime import datetime

try:
    import sendgrid
    from sendgrid.helpers.mail import Mail, Email, To, Content, MimeType
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


class EmailSender:
    def __init__(self, api_key: str, from_email: str, from_name: str, demo: bool = True):
        self.api_key    = api_key
        self.from_email = from_email
        self.from_name  = from_name
        self.demo       = demo
        self.log        = []

    def send(self, to_email: str, to_name: str, subject: str,
             html_body: str = None, body: str = None, metadata: dict = None):
        """Send an HTML email or plain text fallback."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "to":        f"{to_name} <{to_email}>",
            "subject":   subject,
            "metadata":  metadata or {},
            "status":    None,
        }

        if self.demo:
            self._save_preview(to_name, to_email, subject, html_body or body, metadata)
            record["status"] = "demo"
        else:
            success = self._send_via_sendgrid(to_email, to_name, subject, html_body, body)
            record["status"] = "sent" if success else "failed"

        self.log.append(record)

    def print_summary(self):
        print("\n" + "=" * 55)
        print(f"  📊  Session Summary — {len(self.log)} email(s)")
        print("=" * 55)
        for entry in self.log:
            icon = "✅" if entry["status"] in ("sent", "demo") else "❌"
            print(f"  {icon}  {entry['to']}")
            print(f"      Subject : {entry['subject']}")
            print(f"      Status  : {entry['status']}")
            print()

    # ── Private ───────────────────────────────────────────────────────────────

    def _save_preview(self, to_name, to_email, subject, content, metadata):
        """In demo mode, saves the HTML email as a file you can open in a browser."""
        os.makedirs("previews", exist_ok=True)
        step = metadata.get("step", "email") if metadata else "email"
        filename = f"previews/{step}_{to_name.lower().replace(' ','_')}.html"

        if content and content.strip().startswith("<!DOCTYPE"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  📄  Preview saved → {filename}")
        else:
            border = "─" * 50
            print(f"\n  ┌{border}┐")
            print(f"  │  To      : {to_name} <{to_email}>")
            print(f"  │  Subject : {subject}")
            print(f"  ├{border}┤")
            for line in (content or "").strip().split("\n"):
                print(f"  │  {line}")
            print(f"  └{border}┘")

    def _send_via_sendgrid(self, to_email, to_name, subject, html_body, plain_body):
        if not SENDGRID_AVAILABLE:
            print("  ⚠️  sendgrid not installed. Run: pip install sendgrid")
            return False

        try:
            sg      = sendgrid.SendGridAPIClient(api_key=self.api_key)
            message = Mail(
                from_email = Email(self.from_email, self.from_name),
                to_emails  = To(to_email, to_name),
                subject    = subject,
            )

            if html_body:
                message.content = [
                    Content(MimeType.text, plain_body or "Please view this email in an HTML-compatible client."),
                    Content(MimeType.html, html_body),
                ]
            else:
                message.content = [Content(MimeType.text, plain_body or "")]

            response = sg.client.mail.send.post(request_body=message.get())
            success  = response.status_code in (200, 201, 202)
            print(f"  {'✅' if success else '❌'}  SendGrid → {to_email} [{response.status_code}]")
            return success

        except Exception as e:
            print(f"  ❌  SendGrid error: {e}")
            try:
                print(f"  ❌  Details: {json.loads(e.body)}")
            except:
                pass
            return False
