import imaplib
import email
from email.header import decode_header

def fetch_emails_from_gmail(email_user, email_pass, mailbox="INBOX", num_emails=5):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select(mailbox)

    status, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    latest_email_ids = email_ids[-num_emails:]

    emails = []

    for e_id in reversed(latest_email_ids):
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        if status != 'OK':
            continue
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdisp = str(part.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in cdisp:
                            try:
                                body = part.get_payload(decode=True).decode()
                                break
                            except:
                                body = ""
                else:
                    if msg.get_content_type() == "text/plain":
                        body = msg.get_payload(decode=True).decode()

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    try:
                        subject = subject.decode(encoding if encoding else "utf-8")
                    except:
                        subject = subject.decode('utf-8', errors='ignore')

                full_text = f"Subject: {subject}\n\n{body}"
                emails.append(full_text.strip())
    mail.logout()
    return emails
