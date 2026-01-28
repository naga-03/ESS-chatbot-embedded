import os
import json
import smtplib
from typing import Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMPLOYEE_DATA_PATH = "data/employees.json"

# Admin-specific context (per admin session)
_ADMIN_EMAIL_CONTEXT: Dict[str, Dict] = {}


def handle_admin_email_feature(user: Dict, entities: Dict) -> str:
    """Admin email flow (fully safe + reset clean)."""

    if not user or user.get("role") != "ADMIN":
        return "❌ You are not authorized to send emails."

    admin_id = user["employee_id"]
    employees = _load_employees()

    admin = _find_employee_by_id(admin_id, employees)
    if not admin or not admin.get("email"):
        return "❌ Admin email configuration missing."

    raw_text = entities.get("raw_text", "").strip()

    # --------------------------------------------------
    # STEP 2: SEND EMAIL
    # --------------------------------------------------
    if admin_id in _ADMIN_EMAIL_CONTEXT:
        context = _ADMIN_EMAIL_CONTEXT.pop(admin_id)

        if not raw_text:
            return "❌ Please provide the message to send."

        _send_email(
            from_email=admin["email"],
            to_email=context["to_employee"]["email"],
            to_name=context["to_employee"]["name"],
            admin_name=admin["name"],
            message=raw_text
        )

        return f"✅ Email sent successfully to {context['to_employee']['name']}."

    # --------------------------------------------------
    # STEP 1: DETECT EMPLOYEE
    # --------------------------------------------------
    employee_name = entities.get("employee_name") or _match_employee_name(raw_text, employees)

    if not employee_name:
        return "❌ Please specify the employee name."

    employee = _find_employee_by_name(employee_name, employees)
    if not employee:
        return f"❌ Employee '{employee_name}' not found."

    if not employee.get("email"):
        return f"❌ Email not available for {employee['name']}."

    _ADMIN_EMAIL_CONTEXT[admin_id] = {"to_employee": employee}

    return f"📩 What message would you like to send to {employee['name']}?"


# =====================================================
# HELPERS
# =====================================================
def _load_employees() -> list:
    with open(EMPLOYEE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["employees"]


def _find_employee_by_name(name: str, employees: list) -> Optional[Dict]:
    name = name.lower()
    return next((e for e in employees if e["name"].lower() == name), None)


def _find_employee_by_id(emp_id: str, employees: list) -> Optional[Dict]:
    return next((e for e in employees if e["employee_id"] == emp_id), None)


def _match_employee_name(text: str, employees: list) -> Optional[str]:
    text = text.lower()
    for emp in employees:
        if emp["name"].lower() in text:
            return emp["name"]
    return None


def _send_email(from_email: str, to_email: str, to_name: str, admin_name: str, message: str) -> None:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials missing")

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Official Communication – TechCorp"

    html = f"""
    <html>
      <body style="font-family: Arial;">
        <p>Hello <b>{to_name}</b>,</p>
        <p>{message}</p>
        <br>
        <p>
          Regards,<br>
          <b>{admin_name}</b><br>
          TechCorp HR
        </p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(from_email, to_email, msg.as_string())
