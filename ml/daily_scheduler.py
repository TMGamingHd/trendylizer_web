
# ml/daily_scheduler.py

import time
import datetime

def run_daily_job(job_fn, interval_sec=86400):
    print("🗓️  Scheduler started. Will run job daily.")
    while True:
        now = datetime.datetime.now()
        print(f"▶️ Running job at {now}")
        job_fn()
        print(f"✅ Job finished at {datetime.datetime.now()}")
        time.sleep(interval_sec)
