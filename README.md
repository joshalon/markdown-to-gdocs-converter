# Markdown to Google Docs Converter

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/joshalon/markdown-to-gdocs-converter)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**GitHub Repository:** https://github.com/joshalon/markdown-to-gdocs-converter

A Python script that converts markdown meeting notes into a well-formatted Google Doc with proper styling, headings, bullet points, and checkboxes.

## Demo Documents

✨ **Live Examples:**
- [Technical README Conversion](https://docs.google.com/document/d/1zXOp4au4H1jpzDkvuQA8N3JMev-ZV7Ye46fAaEoTlPg/edit) - Complex document with nested bullets
- [Meeting Notes Conversion](https://docs.google.com/document/d/1EihcbdV3aSlDfmEJkJ1V-hUEctQdW2cVdLwnk6xjHSc/edit) - Checkboxes, @mentions, footer styling

## Features

- Converts markdown to Google Docs with proper formatting
- Supports multiple heading levels (H1, H2, H3)
- Preserves nested bullet point hierarchy
- Converts markdown checkboxes to actual Google Docs checkboxes
- Styles assignee mentions (@name) with bold formatting
- Handles footer information with distinct styling
- Comprehensive error handling

## Prerequisites

- Google Account
- Google Cloud Project with Google Docs API enabled
- Python 3.7+

## Setup Instructions

### 1. Enable Google Docs API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Docs API"
   - Click "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Desktop app" as application type
   - Download the credentials JSON file
   - Rename it to `credentials.json`

### 2. Running in Google Colab

#### Option A: Using the Provided Notebook

1. Open the `markdown_to_gdocs.ipynb` file in Google Colab
2. Upload your `credentials.json` file when prompted (or use Colab's file upload)
3. Run all cells
4. Authenticate with your Google account when prompted
5. The script will output a link to your newly created Google Doc

#### Option B: Running the Python Script Directly

1. Upload both `markdown_to_gdocs.py` and `credentials.json` to Colab
2. Install dependencies:
   ```python
   !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Run the script:
   ```python
   !python markdown_to_gdocs.py
   ```

## Required Dependencies

```
google-auth>=2.0.0
google-auth-oauthlib>=0.5.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
```

## How It Works

1. **Authentication**: Uses OAuth 2.0 to authenticate with Google Docs API
2. **Document Creation**: Creates a new Google Doc programmatically
3. **Content Parsing**: Parses markdown content line by line
4. **Formatting Application**: Applies appropriate styles:
   - H1 for main title
   - H2 for section headers
   - H3 for sub-section headers
   - Nested bullet points with proper indentation
   - Checkboxes for action items
   - Bold styling for @mentions
5. **Error Handling**: Graceful handling of API errors and edge cases

## Project Structure

```
markdown-to-gdocs-converter/
├── README.md                    # This file
├── markdown_to_gdocs.py         # Main Python script
├── markdown_to_gdocs.ipynb      # Google Colab notebook
├── meeting_notes.md             # Sample markdown meeting notes
└── credentials.json             # Your Google API credentials (not in repo)
```

## Usage Example

The script automatically processes the meeting notes and creates a formatted Google Doc. After running, you'll receive a shareable link to the document.

## Troubleshooting

### "File not found: credentials.json"
- Ensure you've downloaded and uploaded the credentials file from Google Cloud Console

### "API has not been enabled"
- Make sure you've enabled the Google Docs API in your Google Cloud project

### Authentication errors
- Clear any existing tokens and re-authenticate
- Ensure you're using the correct Google account

## Security Notes

- Never commit `credentials.json` or `token.json` to version control
- These files contain sensitive authentication information
- The `.gitignore` file is configured to exclude these files

## Getting Started Quickly

### Clone the Repository

```bash
git clone https://github.com/joshalon/markdown-to-gdocs-converter.git
cd markdown-to-gdocs-converter
pip install -r requirements.txt
```

### Quick Test

1. Add your `credentials.json` file to the project directory
2. Run the converter:
```bash
python markdown_to_gdocs.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **GitHub Repository:** https://github.com/joshalon/markdown-to-gdocs-converter
- **Live Demo Document 1:** [Technical README](https://docs.google.com/document/d/1zXOp4au4H1jpzDkvuQA8N3JMev-ZV7Ye46fAaEoTlPg/edit)
- **Live Demo Document 2:** [Meeting Notes](https://docs.google.com/document/d/1EihcbdV3aSlDfmEJkJ1V-hUEctQdW2cVdLwnk6xjHSc/edit)

## License

MIT License - Feel free to use this for your projects!

## Author

Created as part of a Full Stack Software Engineer assessment task.

**Project Repository:** https://github.com/joshalon/markdown-to-gdocs-converter
