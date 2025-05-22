import csv
from datetime import datetime
import os

LOG_FILE = "spam_sniffer_log.csv"

def log_classification(source, label, confidence):
    log_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["Timestamp", "Source", "Label", "Confidence (%)"])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, source, label, f"{confidence:.2f}"])
