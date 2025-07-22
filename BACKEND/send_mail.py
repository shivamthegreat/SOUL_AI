import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==== Email Sender Credentials ====
SENDER_EMAIL = "soulai7771@gmail.com"         # Replace with your email
SENDER_PASSWORD = "xaejuqjmsgqtfrwu"    # Use App Password (not Gmail password)

# ==== Global Email State ====
email_state = {
    "awaiting": None,
    "email": "",
    "subject": "",
    "body": ""
}


# ==== Function: Send Mail ====
def send_mail(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False

# ==== Function: Handle Email Conversation ====
def handle_email_conversation(text):
    global email_state

    if "send a mail" in text.lower():
        email_state = {
            "awaiting": "email",
            "email": "",
            "subject": "",
            "body": ""
        }
        return "📧 Please tell me the receiver's email ID."

    elif email_state["awaiting"] == "email":
        email_state["email"] = text.strip()
        email_state["awaiting"] = "subject"
        return "📝 What should be the subject of the email?"

    elif email_state["awaiting"] == "subject":
        email_state["subject"] = text.strip()
        email_state["awaiting"] = "body"
        return "💬 What should I write in the body of the email?"

    elif email_state["awaiting"] == "body":
        email_state["body"] = text.strip()
        email_state["awaiting"] = None

        success = send_mail(
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_PASSWORD,
            recipient_email=email_state["email"],
            subject=email_state["subject"],
            body=email_state["body"]
        )

        if success:
            return "✅ Email sent successfully!"
        else:
            return "❌ Failed to send email."

    else:
        return "I didn't understand that. Please say 'send a mail' to begin."
