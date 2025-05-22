import joblib
import re
import numpy as np
from bs4 import BeautifulSoup
import imaplib
import email
from email.header import decode_header
from colorama import Fore, Style, init
import pyfiglet
import os
import getpass
from datetime import datetime

init(autoreset=True)

# === Load model and vectorizer ===
model = joblib.load('models/logistic_model.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')

def print_banner():
    ascii_banner = pyfiglet.figlet_format("SPAMSNIFFER")
    print(Fore.RED + ascii_banner + Style.RESET_ALL)
    print(Fore.YELLOW + "        Email Phishing Detector CLI Tool\n" + Style.RESET_ALL)

def clean_email(text):
    text = BeautifulSoup(str(text), 'html.parser').get_text()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def predict_email(text):
    cleaned = clean_email(text)
    vectorized = vectorizer.transform([cleaned])
    proba = model.predict_proba(vectorized)[0]
    prediction = np.argmax(proba)
    confidence = proba[prediction] * 100
    return ("Phishing" if prediction == 1 else "Legitimate", confidence)

def log_classification(input_type, label, confidence, source):
    log_file = "spam_sniffer.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] Type: {input_type}, Label: {label}, Confidence: {confidence:.2f}%, Source: {source}\n")

def classify_manual():
    print("\nEnter the full email content (end with a single '.' on a line):")
    lines = []
    while True:
        line = input()
        if line == '.':
            break
        lines.append(line)
    email_text = "\n".join(lines).strip()
    if not email_text:
        print(Fore.RED + "No input provided. Returning to main menu.")
        return
    label, confidence = predict_email(email_text)
    print(f"\nResult: {Fore.RED if label=='Phishing' else Fore.GREEN}{label} ({confidence:.2f}%)\n")
    log_classification("Manual Input", label, confidence, "N/A")

def fetch_emails_from_gmail():
    print("\nConnect to Gmail via IMAP")
    user = input("Enter Gmail address: ")
    password = getpass.getpass("Enter app-specific password (or your Gmail password): ")

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        imap.login(user, password)
    except imaplib.IMAP4.error:
        print(Fore.RED + "Login failed. Please check your credentials or app password.")
        return

    imap.select("INBOX")
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()
    print(f"Total emails found: {len(email_ids)}")

    # Limit number of emails to process for demo
    max_emails = 5
    for i, email_id in enumerate(email_ids[:max_emails]):
        res, msg = imap.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg_email = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg_email["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                from_ = msg_email.get("From")
                # Get the email body
                body = ""
                if msg_email.is_multipart():
                    for part in msg_email.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                else:
                    try:
                        body = msg_email.get_payload(decode=True).decode()
                    except:
                        body = ""
                combined = subject + "\n" + body
                label, confidence = predict_email(combined)
                print(f"\nEmail {i+1} From: {from_}")
                print(f"Subject: {subject}")
                print(f"Result: {Fore.RED if label=='Phishing' else Fore.GREEN}{label} ({confidence:.2f}%)\n")
                log_classification("Gmail", label, confidence, subject)
    imap.logout()

def main():
    print_banner()
    while True:
        print("Options:")
        print("1. Inspect manually typed email")
        print("2. Connect to Gmail and analyze latest emails")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()
        if choice == '1':
            classify_manual()
        elif choice == '2':
            fetch_emails_from_gmail()
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
