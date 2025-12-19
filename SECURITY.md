# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it by:
1. **DO NOT** open a public GitHub issue
2. Email the repository maintainer privately
3. Include details about the vulnerability and steps to reproduce

## Security Best Practices for Users

### Protecting Your API Key

1. **Never commit `api_key.txt` to version control**
   - The `.gitignore` file is configured to exclude this file
   - Always verify before pushing commits: `git status`

2. **Restrict file permissions (Unix/Linux/Mac)**
   ```bash
   chmod 600 api_key.txt
   ```
   This ensures only your user can read/write the file.

3. **Keep your API key confidential**
   - Don't share your API key in screenshots, logs, or documentation
   - Don't paste it in public forums or chat applications
   - Rotate your API key if you suspect it has been compromised

4. **Use environment variables for additional security**
   ```bash
   # Set custom install location
   export DARKSTAR_INSTALL="/secure/path"
   
   # Set custom API endpoint (if needed)
   export DARKSTAR_API_URL="https://your-custom-endpoint.com/api"
   ```

### System Security

1. **Run with appropriate privileges**
   - Don't run the scripts with elevated privileges (sudo/administrator) unless necessary
   - The scripts only need access to monitor keyboard/mouse and make network requests

2. **Monitor network activity**
   - The application sends data to:
     - `http://localhost:5600` (ActivityWatch - local only)
     - `https://DarkstarDestinations.com/Activity` (Darkstar API - via HTTPS)
   - All external communication uses encrypted HTTPS

3. **Review logs regularly**
   - Activity logs are stored in `Logs/Activity/`
   - Logs are automatically cleaned up after 24 hours
   - Review logs to ensure no sensitive information is being captured

4. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Data Privacy

This application monitors:
- ✅ Application names you use
- ✅ Window titles
- ✅ Keyboard and mouse activity timestamps (timing only, not content)

This application does NOT capture:
- ❌ Actual keystrokes or text you type
- ❌ Mouse coordinates or click locations (only timestamps)
- ❌ Screen contents or screenshots
- ❌ File contents or clipboard data

### Secure Installation

1. **Verify source code before running**
   - Review the Python scripts to understand what they do
   - Check the `.gitignore` to ensure sensitive files are excluded

2. **Use a virtual environment**
   - The installer creates a virtual environment (`venv/`)
   - This isolates dependencies from your system Python

3. **Install from official sources**
   - Only install dependencies from PyPI via pip
   - Review `requirements.txt` for the list of dependencies

### Multi-User Systems

If using this on a shared computer:

1. **Use separate install directories per user**
   ```bash
   python extract_activity_v3.py "$HOME/darkstar"
   ```

2. **Ensure your API key file is not readable by other users**
   ```bash
   chmod 600 api_key.txt
   ```

3. **Consider using user-specific configuration**
   - Each user should have their own API key
   - Use environment variables to separate installations

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| Older   | :x:                |

Always use the latest version from the main branch for the most up-to-date security patches.

## Security Features

- ✅ API keys stored in separate files (not in code)
- ✅ Sensitive files excluded from version control
- ✅ HTTPS used for external API communication
- ✅ Automatic log cleanup (24-hour retention)
- ✅ File permission restrictions on Unix-like systems
- ✅ No hardcoded credentials in source code
- ✅ Configurable endpoints via environment variables

## Known Limitations

1. **Windows file permissions** - File permission restrictions are not automatically set on Windows systems
2. **Local ActivityWatch API** - The local ActivityWatch API uses HTTP (not HTTPS), but this is only local traffic
3. **Log contents** - Activity logs may contain window titles that could include sensitive information (e.g., document names)

## Compliance

This tool is designed for legitimate employee monitoring and productivity tracking. Users are responsible for:
- Complying with local privacy and employment laws
- Informing monitored users as required by law
- Obtaining necessary consents
- Protecting collected data according to applicable regulations (GDPR, CCPA, etc.)

---

**Last Updated:** 2025-12-19
