# 🛡️ SpamSniffer – Terminal-Based Phishing Email Detection Tool

**SpamSniffer** is a lightweight, CLI-based phishing email detection tool designed for cybersecurity enthusiasts and digital forensics practitioners. It uses a trained logistic regression model with TF-IDF vectorization to classify emails as *Phishing* or *Legitimate*. The tool supports manual input, file upload, and Gmail inbox scanning – all from a terminal interface (ideal for Kali Linux environments).

---

## 🔍 Features

- 🧠 **Machine Learning–Powered** detection (Logistic Regression + TF-IDF)
- 📝 **Manual Email Input** for on-the-fly inspection
- 📁 **File Upload** support (`.txt`, `.eml`, `.html`)
- 📧 **Gmail Integration** (read and scan inbox emails)
- 🧾 **Logging System** that saves results and timestamps
- ✅ Designed for **Terminal Use** (no GUI bloat)
- 💻 Compatible with **Linux (Kali)** and other Unix-based systems

---

## 🚧 Project Status

> This project is currently **under development**. More features (like improved NLP preprocessing, threat scoring, and real-time alerts) are coming soon!

---

## 📁 Directory Structure

```
SPAMSNIFFER/
│
├── data/                 # Datasets used for training
├── models/               # ML model and vectorizer
├── logs/                 # Classification and email scan logs
├── utils/
│   ├── email_fetcher.py  # Gmail connector
│   └── logger.py         # History logger
├── spam_sniffer.py       # Main CLI tool
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/rosxxna/spamsniffer.git
cd spamsniffer
pip install -r requirements.txt
python3 spam_sniffer.py
```

---

## 📬 Gmail Integration

Make sure to generate an **App Password** in your Google account settings if using 2FA, and enable access to less secure apps (or use OAuth if preferred).

---

## 📄 License

MIT License - free to use, modify, and distribute.
