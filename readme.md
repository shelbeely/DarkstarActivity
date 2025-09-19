# Darkstar Activity Monitor

This package provides background monitoring and reporting of workstation activity to the Darkstar system.
It integrates **ActivityWatcher** (for app/window usage) with a **keyboard & mouse listener** for local activity tracking.

---

## 📋 Prerequisites

1. **Install Python (3.9 or newer)**

   * Download from [python.org/downloads](https://www.python.org/downloads/)
   * During installation, check:

     * ✅ *Add Python to PATH*

2. **Install ActivityWatcher**

   * Download the latest release: [https://activitywatch.net/downloads/](https://activitywatch.net/downloads/)
   * Extract or install it, then start `ActivityWatch` so the local API is running on port `5600`.
   * Verify it’s active by visiting: [http://localhost:5600/api/0/buckets](http://localhost:5600/api/0/buckets)
     You should see JSON output with your buckets.

---

## 📦 Setup

1. Clone or download this repository into a folder, for example:

   C:\Darkstar\ActivityWatcher\\

2. Run the included **installer**:

   install.bat

This will:

* Create a Python virtual environment (`venv/`)
* Install required packages:

  * `requests`
  * `mysql-connector-python`
  * `pynput`
* Prompt you for your **Darkstar API Key**

> 🔑 **Where do I find my API key?**
> Log in to your Darkstar account and go to your **Settings page** on the Darkstar website.
> Copy the API key shown there and paste it when the installer asks. <//Not yet exposed.
> It will be saved into `api_key.txt` under the install root.

---

## ▶️ Usage

### Standard Mode (visible windows)

Launch both monitors in separate windows (one for `KMActivity`, one for `extract_activity`):

run.bat

You will see:

* **KMActivity** → “Listening for activity... Press Ctrl+C to stop.”
* **ExtractActivity** → Cycle logs of fetched events and API submissions.

Close both windows to stop monitoring.

---

### Silent Mode (background, no windows)

Run the monitors silently in the background:

run\_silent.bat

* Processes run with `pythonw.exe` (no console windows, no taskbar entries).
* Optionally logs can be enabled inside `run_silent.bat` to capture output into:

  * `KMActivity.log`
  * `ExtractActivity.log`

To stop, end the processes in **Task Manager** or reboot.

---

## ⚙️ Configuration

* **Install Root**
  By default, scripts assume they live under `C:\Darkstar\ActivityWatcher\`.
  You can override this by:

  * Passing a custom install path as the first argument:
    python extract\_activity.py "D:\CustomPath"
  * Or setting an environment variable:
    setx DARKSTAR\_INSTALL "D:\CustomPath"

* **API Key**
  The installer will ask for your Darkstar API key and save it in:
  api\_key.txt
  under the install root.

  If you need to reset it later, delete the file and rerun `install.bat`.

* **Log Cleanup**
  Extractor automatically deletes logs older than **24 hours** from:
  Logs\Activity\\

---

## ✅ Verification

1. Start `run.bat`

2. Move your mouse or press a key → `activity_timestamp.txt` updates

3. Watch extractor console for:

   🕒 Cycle started...
   🔍 Filtered X events.
   ✅ Sent X activity logs to Darkstar API.

4. Confirm API accepted events (HTTP 200).

---

## 🛑 Troubleshooting

* **No events sent**

  * Make sure ActivityWatcher is running and buckets appear at:
    [http://localhost:5600/api/0/buckets](http://localhost:5600/api/0/buckets)

* **API key errors**

  * Delete `api_key.txt` and rerun `install.bat` → it will prompt for a new key.

* **Silent mode does nothing**

  * Check `KMActivity.log` and `ExtractActivity.log` if logging is enabled in `run_silent.bat`.

---

## 📂 File Overview

* `install.bat` → Sets up Python venv, installs dependencies, and asks for API key
* `run.bat` → Starts monitors with console windows visible
* `run_silent.bat` → Starts monitors hidden in the background
* `KMActivity.py` → Keyboard/mouse listener, updates `activity_timestamp.txt`
* `extract_activity.py` → Fetches ActivityWatcher events, sends them to Darkstar API, cleans up logs
* `README.md` → This guide

---
