import csv
import os
from datetime import datetime

LOG_FILE = "data/disease_log.csv"

def log_detection(location, crop, disease):

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["date", "location", "crop", "disease"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            location,
            crop,
            disease
        ])