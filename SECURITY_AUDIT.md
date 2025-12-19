# Security Audit Report - DarkstarActivity

**Audit Date:** 2025-12-19  
**Auditor:** GitHub Copilot Security Agent  
**Repository:** shelbeely/DarkstarActivity

---

## Executive Summary

This security audit was conducted to identify any secrets, sensitive data, or security concerns in the DarkstarActivity codebase. The repository contains a Python-based activity monitoring tool that integrates with ActivityWatch and sends data to a Darkstar API endpoint.

**Overall Status:** ✅ **GOOD** - No hardcoded secrets found in the codebase. Good security practices are mostly followed.

---

## Findings

### ✅ Positive Security Practices

1. **API Key Management**
   - ✅ API keys are stored in a separate file (`api_key.txt`) that is properly excluded from version control
   - ✅ `.gitignore` correctly excludes `api_key.txt`
   - ✅ No API keys are hardcoded in the source code
   - ✅ Git history check confirms `api_key.txt` was never committed

2. **Sensitive Data Handling**
   - ✅ No passwords, tokens, or private keys found in the codebase
   - ✅ No credentials in batch files or configuration files
   - ✅ Virtual environment (`venv/`) is properly excluded from version control

3. **Code Structure**
   - ✅ Clean separation of concerns with API key handling in dedicated functions
   - ✅ User is prompted for API key during installation if not present
   - ✅ Logs directory is properly excluded from version control

### ⚠️ Potential Concerns & Recommendations

1. **Hardcoded API Endpoint (LOW RISK)**
   - **Location:** `extract_activity_v3.py:154`
   - **Issue:** The API endpoint URL `https://DarkstarDestinations.com/Activity` is hardcoded
   - **Risk Level:** LOW - This is a public API endpoint, not a secret
   - **Recommendation:** Consider making this configurable via environment variable for flexibility
   ```python
   api_url = os.environ.get("DARKSTAR_API_URL", "https://DarkstarDestinations.com/Activity")
   ```

2. **ActivityWatch Local Endpoint (NO RISK)**
   - **Location:** `extract_activity_v3.py:77`
   - **Issue:** `http://localhost:5600/api/0/buckets` is hardcoded
   - **Risk Level:** NONE - This is a standard local endpoint
   - **Note:** This is expected behavior for ActivityWatch integration

3. **Dummy Data in Payload (LOW CONCERN)**
   - **Location:** `extract_activity_v3.py:137`
   - **Issue:** `"User": "APIKeyisonlyneededdummydata"` appears in the payload
   - **Risk Level:** LOW - This appears to be a placeholder field
   - **Recommendation:** Consider if this field is actually needed by the API

4. **File Permissions (MEDIUM PRIORITY)**
   - **Issue:** No explicit file permission setting for `api_key.txt`
   - **Risk Level:** MEDIUM on shared systems
   - **Recommendation:** Add file permission restrictions after creating the API key file:
   ```python
   import os
   import stat
   
   # After writing api_key.txt
   os.chmod(API_KEY_FILE, stat.S_IRUSR | stat.S_IWUSR)  # Only user read/write
   ```

5. **Error Messages (LOW RISK)**
   - **Issue:** Error messages might leak file paths
   - **Risk Level:** LOW - Paths are user-controlled install locations
   - **Note:** No sensitive data is exposed in error messages

### 📋 Additional Security Considerations

1. **HTTPS for API Calls**
   - ✅ The main API endpoint uses HTTPS: `https://DarkstarDestinations.com/Activity`
   - This ensures encrypted transmission of activity data

2. **Dependencies**
   - Current dependencies: `requests`, `pynput`
   - **Recommendation:** Consider adding a `requirements.txt` with pinned versions for security
   ```
   requests==2.31.0
   pynput==1.7.6
   ```

3. **Input Validation**
   - API key input validation is minimal (only checks if empty)
   - **Recommendation:** Consider adding format validation for API keys if they follow a specific pattern

4. **Logging Security**
   - ✅ Logs are stored in a separate directory and cleaned up after 24 hours
   - ✅ API keys are not logged in any output statements
   - ✅ No sensitive data appears in log messages

---

## Security Checklist

- [x] No hardcoded passwords
- [x] No hardcoded API keys
- [x] No hardcoded tokens or secrets
- [x] No private keys in repository
- [x] Sensitive files properly excluded in `.gitignore`
- [x] No secrets in git history
- [x] No credentials in configuration files
- [x] HTTPS used for external API calls
- [x] API keys stored separately from code
- [ ] File permissions explicitly set for sensitive files (recommended)
- [ ] Dependencies pinned to specific versions (recommended)

---

## Recommendations Summary

### High Priority
None identified.

### Medium Priority
1. Add explicit file permissions for `api_key.txt` (Unix-like systems)
2. Create `requirements.txt` with pinned dependency versions

### Low Priority
1. Make API endpoint URL configurable via environment variable
2. Review if the dummy "User" field is necessary in the API payload
3. Add API key format validation if applicable

---

## Conclusion

The DarkstarActivity repository demonstrates good security practices overall. **No critical secrets or sensitive data were found in the codebase or git history.** The main API key is properly managed through an external file that is excluded from version control.

The identified concerns are mostly related to best practices and hardening, rather than actual security vulnerabilities. The recommendations provided above would further improve the security posture of the application.

**Risk Level:** ✅ **LOW** - Safe to use with the existing security measures in place.

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
