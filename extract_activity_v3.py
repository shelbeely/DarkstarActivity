import requests
import json
from datetime import datetime, timedelta, timezone
import time
import traceback
import sys
import os

# ==============================
# 🔹 INSTALL LOCATION HANDLING 🔹
# ==============================
def get_install_root():
    # Priority: command-line arg → ENV var → fallback default
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.environ.get("DARKSTAR_INSTALL", r"C:\Darkstar\ActivityWatcher")

INSTALL_ROOT   = get_install_root()
OUTPUT_DIR     = os.path.join(INSTALL_ROOT, "Logs", "Activity")
API_KEY_FILE   = os.path.join(INSTALL_ROOT, "api_key.txt")
ACTIVITY_FILE  = os.path.join(INSTALL_ROOT, "activity_timestamp.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# 🔹 API KEY HANDLING 🔹
# ==============================
def get_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()

    api_key = input("🔑 Enter your Darkstar API key: ").strip()
    if not api_key:
        print("❌ API key cannot be empty. Exiting.")
        sys.exit(1)

    with open(API_KEY_FILE, "w") as f:
        f.write(api_key)
    print(f"✅ API key saved to {API_KEY_FILE}")
    return api_key

API_KEY = get_api_key()

# ==============================
# 🔹 UTILITY FUNCTIONS 🔹
# ==============================
def _non_null_str(value: str, fallback: str = "") -> str:
    return (value or "").strip() or fallback

def _safe_timestamp(value) -> str:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    if isinstance(value, str) and value:
        return value  # Assume str already ISO formatted
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

# ==============================
# 🔹 LOG CLEANUP (24h) 🔹
# ==============================
def cleanup_logs():
    cutoff = datetime.now() - timedelta(days=1)
    for file in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, file)
        try:
            if os.path.isfile(fpath):
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                if mtime < cutoff:
                    os.remove(fpath)
                    print(f"🧹 Deleted old log: {file}")
        except Exception as e:
            print(f"⚠️ Cleanup failed for {file}: {e}")

# ==============================
# 🔹 ACTIVITYWATCH API ENDPOINT 🔹
# ==============================
AW_URL = "http://localhost:5600/api/0/buckets"

def fetch_logs():
    response = requests.get(AW_URL)
    if response.status_code != 200:
        print("❌ Error fetching buckets.")
        return {}
    buckets = response.json()
    logs = {}
    for bucket_name in buckets.keys():
        bucket_url = f"{AW_URL}/{bucket_name}/events"
        event_response = requests.get(bucket_url)
        if event_response.status_code == 200:
            logs[bucket_name] = event_response.json()
        else:
            logs[bucket_name] = []
    return logs

def filter_events_last_15_minutes(logs):
    cutoff = datetime.now().astimezone() - timedelta(minutes=17)
    filtered = []
    for bucket, events in logs.items():
        for event in events:
            ts = event.get("timestamp")
            if ts:
                try:
                    event_time = datetime.fromisoformat(ts)
                    if event_time >= cutoff:
                        filtered.append(event)
                except Exception as e:
                    print(f"⚠️ Error parsing timestamp {ts}: {e}")
    return filtered

def load_key_mouse_activity(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    return line.strip()
    except Exception as e:
        print(f"⚠️ Failed to load key/mouse activity data: {e}")
    return None

# ==============================
# 🔹 INSERT ACTIVITY LOGS 🔹
# ==============================
def insert_activity_logs(events):
    if not events:
        print("⚠️ No new activity logs to send.")
        return

    activity_timestamp = load_key_mouse_activity(ACTIVITY_FILE) or "0"

    records = []
    for raw in events:
        app_name   = _non_null_str(raw.get("data", {}).get("app"), "Unknown")
        title      = _non_null_str(raw.get("data", {}).get("title"))
        event_time = _safe_timestamp(raw.get("timestamp"))

        records.append({
            "User": "APIKeyisonlyneededdummydata", 
            "AppName": app_name,
            "EventTitle": title,
            "EventTime": event_time,
            "EventCount": "1",
            "KeyMouseActivity": str(activity_timestamp)
        })

    # ✅ Send a raw list, not wrapped in {"data": ...}
    payload = records

    headers = {
        "Content-Type": "application/json",
        "X-Activity-Key": API_KEY
    }

    try:
        api_url = "https://DarkstarDestinations.com/Activity"
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"✅ Sent {len(records)} activity logs to Darkstar API.")
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send activity logs: {e}")

# ==============================
# 🔹 AGGREGATE TOP APPS 🔹
# ==============================
def aggregate_top_apps(events):
    app_counts = {}
    app_events = {}
    for event in events:
        app = event.get("data", {}).get("app", "Unknown")
        app_counts[app] = app_counts.get(app, 0) + 1
        app_events.setdefault(app, []).append(event)
    top_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return top_apps, app_events

# ==============================
# 🔹 GENERATE & SAVE REPORTS 🔹
# ==============================
def save_json_summary(top_apps, app_events):
    summary = {}
    for app, count in top_apps:
        events_list = []
        for event in app_events[app]:
            timestamp = event.get("timestamp", "")
            title = event.get("data", {}).get("title", "").strip() or "(No title provided)"
            events_list.append({"timestamp": timestamp, "title": title})
        summary[app] = {"count": count, "events": events_list}
    
    json_filename = f"top_apps_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    json_path = os.path.join(OUTPUT_DIR, json_filename)
    
    with open(json_path, "w") as file:
        json.dump(summary, file, indent=4)
    return summary, json_filename

def generate_text_report(summary):
    report_lines = []
    report_lines.append("-" * 60)
    for app, details in summary.items():
        report_lines.append(f"App: {app} (Total Events: {details['count']})")
        top_events = sorted(details["events"], key=lambda e: e["timestamp"], reverse=True)[:5]
        for ev in top_events:
            try:
                dt = datetime.fromisoformat(ev["timestamp"])
                ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                ts_str = ev["timestamp"]
            title = ev["title"]
            report_lines.append(f"  • {ts_str} : {title}")
        report_lines.append("")
    report_lines.append("-" * 60)
    report_lines.append("Compliance confirmed. Awaiting further commands.")
    return "\n".join(report_lines)

def save_text_report(report_text):
    report_filename = f"activity_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
    report_path = os.path.join(OUTPUT_DIR, report_filename)
    with open(report_path, "w") as file:
        file.write(report_text)
    return report_filename

# ==============================
# 🔹 EXECUTION STARTS HERE 🔹
# ==============================
if __name__ == "__main__":
    print(f"🔄 Darkstar Activity Monitor initialized at {INSTALL_ROOT}. Executing every 4 minutes.\n")
    sys.stdout.flush()

    while True:
        try:
            start_time = datetime.now()
            print(f"🕒 Cycle started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            sys.stdout.flush()

            # Cleanup old logs once per cycle
            cleanup_logs()

            logs = fetch_logs()
            filtered_events = filter_events_last_15_minutes(logs)
            
            print(f"🔍 Filtered {len(filtered_events)} events.")
            sys.stdout.flush()

            insert_activity_logs(filtered_events)
            
            print("✅ Cycle complete. Sleeping for 4 minutes...\n")
            sys.stdout.flush()

        except Exception as e:
            print("❌ Exception occurred during execution cycle:")
            print(traceback.format_exc())
            sys.stdout.flush()

        time.sleep(240)  # 4 minutes
