# src/admin_email_feature.py

import os
import json
import smtplib
import logging
from typing import Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMPLOYEE_DATA_PATH = "data/employees.json"

# --------------------------------------------------
# In-memory context (per admin)
# --------------------------------------------------

_ADMIN_EMAIL_CONTEXT: Dict[str, Dict] = {}

# --------------------------------------------------
# Public Entry Point
# --------------------------------------------------

def handle_admin_email_feature(user: Dict, entities: Dict) -> str:
    """
    Robust admin email flow with fallback name detection.
    """

    if user.get("role") != "ADMIN":
        return " You are not authorized to send emails."

    admin_id = user.get("employee_id")
    employees = _load_employees()

    admin = _find_employee_by_id(admin_id, employees)
    if not admin or not admin.get("email"):
        return " Admin email configuration missing."

    # --------------------------------------------------
    # STEP 2: If context exists → treat input as message
    # --------------------------------------------------
    if admin_id in _ADMIN_EMAIL_CONTEXT:
        message = entities.get("message")

        # Fallback: treat entire input as message
        if not message:
            message = entities.get("raw_text")

        if not message:
            return " Please provide the message to send."

        context = _ADMIN_EMAIL_CONTEXT.pop(admin_id)

        _send_email(
            from_email=admin["email"],
            to_email=context["to_employee"]["email"],
            to_name=context["to_employee"]["name"],
            admin_name=admin["name"],
            message=message
        )

        return f" Email sent successfully to {context['to_employee']['name']}."

    # --------------------------------------------------
    # STEP 1: No context → detect employee
    # --------------------------------------------------

    employee_name = entities.get("employee_name")

    # Fallback: try raw text match
    if not employee_name:
        employee_name = _match_employee_name(
            entities.get("raw_text", ""),
            employees
        )

    if not employee_name:
        return " Please specify the employee name."

    employee = _find_employee_by_name(employee_name, employees)
    if not employee:
        return f" Employee '{employee_name}' not found."

    if not employee.get("email"):
        return f" Email not available for {employee['name']}."

    _ADMIN_EMAIL_CONTEXT[admin_id] = {
        "to_employee": employee
    }

    return f" What message would you like to send to {employee['name']}?"

# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _load_employees() -> list:
    with open(EMPLOYEE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["employees"]


def _find_employee_by_name(name: str, employees: list) -> Optional[Dict]:
    name = name.lower()
    return next(
        (e for e in employees if e["name"].lower() == name),
        None
    )


def _find_employee_by_id(emp_id: str, employees: list) -> Optional[Dict]:
    return next(
        (e for e in employees if e["employee_id"] == emp_id),
        None
    )


def _match_employee_name(text: str, employees: list) -> Optional[str]:
    text = text.lower()
    for emp in employees:
        if emp["name"].lower() in text:
            return emp["name"]
    return None

def _send_email(
    from_email: str,
    to_email: str,
    to_name: str,
    admin_name: str,
    message: str
) -> None:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials are missing")

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Official Communication – TechCorp"

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
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

    #  CORRECT SMTP FLOW FOR MAILTRAP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        server.ehlo()                 # 1️Identify client
        server.starttls()             # 2️ Upgrade to TLS
        server.ehlo()                 # 3️ Re-identify after TLS
        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )                             # 4️ Authenticate
        server.sendmail(
            from_email,
            to_email,
            msg.as_string()
        )                             # 5️ Send email
