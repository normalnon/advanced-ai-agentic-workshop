---
name: gmail
description: "Search and fetch emails via Gmail API with flexible query options and output formats."
---

# gmail

> **Path within category:** `gmail/SKILL.md`


# Gmail Search Skill

Search and fetch emails via Gmail API with flexible query options and output formats.

## Prerequisites

Credentials must be configured in `~/.gmail_credentials/`. Run `setup` to check status:

```bash
python3 scripts/gmail_search.py setup
```

### Obtaining Gmail API Credentials

#### 1. Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click project dropdown -> "New Project"
3. Name it (e.g., "Gmail Agent Skill") -> Create

#### 2. Enable Gmail API

1. Navigate to "APIs & Services" -> "Library"
2. Search for "Gmail API"
3. Click it and press "Enable"

#### 3. Configure OAuth Consent Screen

1. Go to "OAuth consent screen" (left sidebar)
2. Choose "External" user type
3. Fill in required fields:
   - App name: Gmail Agent Skill
   - User support email: your email
   - Developer email: your email
4. Click "Save and Continue", skip Scopes
5. On "Test users" page, add your Gmail address
6. Complete all steps

#### 4. Publish the Test App

**Important:** Without this step, you'll get "Error 403: access_denied".

1. Go back to "OAuth consent screen"
2. Under "Publishing status", click "Publish App"
3. Confirm the dialog

This keeps the app in test mode (not production) but allows your test users to authenticate. You'll see an "unverified app" warning during login - click "Advanced" -> "Go to Gmail Agent Skill (unsafe)" to proceed.

**Note:** Test tokens expire after 7 days. Production requires Google verification.

#### 5. Create OAuth Credentials

1. Go to "Credentials" (left sidebar)
2. Click "Create Credentials" -> "OAuth client ID"
3. Select "Desktop app" as application type
4. Name it (e.g., "Gmail Agent Client")
5. Click "Create"

#### 6. Get Your Credentials

1. Client ID will be displayed - copy it
2. Client Secret: Click the download icon or view details to get the secret

#### 7. Save Credentials

Create `~/.gmail_credentials/credentials.json`:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["http://localhost"]
  }
}
```

#### 8. Authenticate

```bash
python3 scripts/gmail_search.py auth
```

This opens a browser. Click through the "unverified app" warning ("Advanced" -> "Go to Gmail Agent Skill"), approve access, and you're ready.

## Quick Start

```bash
# Check setup status
python3 scripts/gmail_search.py setup

# Authenticate (opens browser)
python3 scripts/gmail_search.py auth

# Search emails
python3 scripts/gmail_search.py search "meeting notes"

# Search with filters
python3 scripts/gmail_search.py search --from "boss@company.com" --unread
```

## Commands

### Setup

Check configuration status:

```bash
python3 scripts/gmail_search.py setup
python3 scripts/gmail_search.py setup --json
```

### Authenticate

Authenticate with Gmail (opens browser for OAuth):

```bash
python3 scripts/gmail_search.py auth
```

### Scope

View or change API permission scope:

```bash
# View current scope
python3 scripts/gmail_search.py scope

# Change scope (requires re-auth)
python3 scripts/gmail_search.py scope --set readonly
python3 scripts/gmail_search.py scope --set modify
python3 scripts/gmail_search.py scope --set full
```

**Available scopes:**
- `readonly` - Read emails only (default, recommended)
- `modify` - Read + modify labels, mark read/unread
- `full` - Full access including delete

### Search

Search emails with free-text query or filters:

```bash
# Free-text search (uses Gmail search syntax)
python3 scripts/gmail_search.py search "project deadline"
python3 scripts/gmail_search.py search "from:john@example.com subject:invoice"

# Using helper flags
python3 scripts/gmail_search.py search --from "john@example.com"
python3 scripts/gmail_search.py search --to "me@example.com"
python3 scripts/gmail_search.py search --subject "Weekly Report"
python3 scripts/gmail_search.py search --label "INBOX"
python3 scripts/gmail_search.py search --label "work"

# Date filters (YYYY/MM/DD format)
python3 scripts/gmail_search.py search --after 2024/01/01
python3 scripts/gmail_search.py search --before 2024/12/31
python3 scripts/gmail_search.py search --after 2024/01/01 --before 2024/06/30

# Status filters
python3 scripts/gmail_search.py search --unread
python3 scripts/gmail_search.py search --starred
python3 scripts/gmail_search.py search --has-attachment

# Combined filters
python3 scripts/gmail_search.py search "invoice" --from "billing@" --has-attachment --after 2024/01/01

# Limit results
python3 scripts/gmail_search.py search "meeting" --limit 50

# Include full body (default shows snippet only)
python3 scripts/gmail_search.py search "contract" --full

# Include attachment info
python3 scripts/gmail_search.py search --has-attachment --attachments

# JSON output
python3 scripts/gmail_search.py search "project" --json
```

### Download Attachments

Download attachments from a specific message:

```bash
# Download to default location (~/Downloads/gmail_attachments/)
python3 scripts/gmail_search.py download MESSAGE_ID

# Download to custom directory
python3 scripts/gmail_search.py download MESSAGE_ID --output /path/to/folder

# JSON output
python3 scripts/gmail_search.py download MESSAGE_ID --json
```

Get message ID from search results (shown in output).

### Labels

List all available Gmail labels:

```bash
python3 scripts/gmail_search.py labels
python3 scripts/gmail_search.py labels --json
```

## Output Formats

### Markdown (default)

```markdown
# Gmail Search Results (3 messages)

## Weekly Report
**From:** boss@company.com
**To:** me@example.com
**Date:** Mon, 25 Nov 2024 10:00:00 +0000
**ID:** `18abc123def`

> Here's the weekly report summary...
