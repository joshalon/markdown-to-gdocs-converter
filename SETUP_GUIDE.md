# Quick Setup Guide for Testing

## Step 1: Create Google Cloud Project & Enable API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **Google Docs API**:
   - Click on "APIs & Services" > "Library"
   - Search for "Google Docs API"
   - Click "Enable"

## Step 2: Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name (e.g., "Markdown Converter Test")
   - Add your email as developer contact
   - Skip scopes section
   - Add your email as test user
   - Submit
4. Back on Credentials page, click "Create Credentials" > "OAuth client ID"
5. Choose "Desktop app" as application type
6. Name it (e.g., "Markdown Converter")
7. Click "Create"
8. **Download the JSON file** (click the download button)
9. Save it as `credentials.json` in the project folder

## Step 3: Run the Test

Once you have `credentials.json`, I'll run the converter for you automatically!

## Quick Commands for You

If you've already downloaded the credentials:

```bash
# Copy your downloaded credentials to the project folder
cp ~/Downloads/client_secret_*.json /Users/newaccount/Desktop/markdown-to-gdocs-converter/credentials.json

# I'll handle the rest!
```
