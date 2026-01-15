"""
Markdown to Google Docs Converter

This script converts markdown meeting notes into a well-formatted Google Doc
with proper styling, headings, bullet points, and checkboxes.

Author: Full Stack Software Engineer Assessment
Date: 2026-01-15
"""

import os
import re
from typing import List, Dict, Tuple
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes required for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']


class MarkdownToGoogleDocs:
    """
    A class to convert markdown meeting notes to Google Docs format.
    """

    def __init__(self, credentials_path: str = 'credentials.json'):
        """
        Initialize the converter with Google API credentials.

        Args:
            credentials_path: Path to the Google API credentials JSON file
        """
        self.credentials_path = credentials_path
        self.service = None
        self.document_id = None
        self.requests = []
        self.current_index = 1  # Start at index 1 (after title)

    def authenticate(self) -> None:
        """
        Authenticate with Google Docs API using OAuth 2.0.

        Raises:
            FileNotFoundError: If credentials file is not found
            Exception: If authentication fails
        """
        try:
            creds = None

            # Check if we have a token file from a previous session
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)

            # If there are no valid credentials, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        raise FileNotFoundError(
                            f"Credentials file '{self.credentials_path}' not found. "
                            "Please download it from Google Cloud Console."
                        )

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            # Build the Google Docs service
            self.service = build('docs', 'v1', credentials=creds)
            print("✓ Successfully authenticated with Google Docs API")

        except FileNotFoundError as e:
            print(f"✗ Error: {e}")
            raise
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            raise

    def create_document(self, title: str) -> str:
        """
        Create a new Google Doc.

        Args:
            title: The title of the document

        Returns:
            The document ID

        Raises:
            Exception: If document creation fails
        """
        try:
            document = self.service.documents().create(body={'title': title}).execute()
            self.document_id = document.get('documentId')
            print(f"✓ Created document with ID: {self.document_id}")
            return self.document_id

        except HttpError as error:
            print(f"✗ An error occurred while creating document: {error}")
            raise

    def parse_line(self, line: str) -> Dict:
        """
        Parse a line of markdown and determine its type and properties.

        Args:
            line: A line of markdown text

        Returns:
            Dictionary containing line type and properties
        """
        stripped = line.lstrip()
        indent_level = len(line) - len(stripped)

        # Determine line type
        result = {
            'original': line,
            'stripped': stripped,
            'indent_level': indent_level,
            'type': 'text'
        }

        # Check for headings
        if stripped.startswith('# ') and not stripped.startswith('## '):
            result['type'] = 'h1'
            result['text'] = stripped[2:].strip()
        elif stripped.startswith('### '):
            result['type'] = 'h3'
            result['text'] = stripped[4:].strip()
        elif stripped.startswith('## '):
            result['type'] = 'h2'
            result['text'] = stripped[3:].strip()
        elif stripped.startswith('- [ ] '):
            result['type'] = 'checkbox'
            result['text'] = stripped[6:].strip()
            result['checked'] = False
        elif stripped.startswith('- [x] ') or stripped.startswith('- [X] '):
            result['type'] = 'checkbox'
            result['text'] = stripped[6:].strip()
            result['checked'] = True
        elif stripped.startswith('* ') or stripped.startswith('- '):
            result['type'] = 'bullet'
            result['text'] = stripped[2:].strip()
            result['level'] = indent_level // 2
        elif stripped.startswith('---'):
            result['type'] = 'separator'
        elif stripped == '':
            result['type'] = 'empty'
        else:
            result['type'] = 'text'
            result['text'] = stripped

        return result

    def find_mentions(self, text: str) -> List[Tuple[int, int]]:
        """
        Find all @mentions in the text and return their positions.

        Args:
            text: The text to search for mentions

        Returns:
            List of tuples containing (start_position, end_position) for each mention
        """
        mentions = []
        pattern = r'@\w+'
        for match in re.finditer(pattern, text):
            mentions.append((match.start(), match.end()))
        return mentions

    def convert_to_google_docs(self, markdown_content: str) -> None:
        """
        Convert markdown content to Google Docs format.

        Args:
            markdown_content: The markdown text to convert
        """
        lines = markdown_content.split('\n')
        self.requests = []
        self.current_index = 1

        # Track if we're in the footer section
        in_footer = False

        for line in lines:
            parsed = self.parse_line(line)

            # Check if we've reached the separator (footer section)
            if parsed['type'] == 'separator':
                in_footer = True
                continue

            # Skip empty lines
            if parsed['type'] == 'empty':
                continue

            # Handle different line types
            if parsed['type'] == 'h1':
                self._add_heading(parsed['text'], 'HEADING_1')
            elif parsed['type'] == 'h2':
                self._add_heading(parsed['text'], 'HEADING_2')
            elif parsed['type'] == 'h3':
                self._add_heading(parsed['text'], 'HEADING_3')
            elif parsed['type'] == 'checkbox':
                self._add_checkbox(parsed['text'], parsed.get('checked', False))
            elif parsed['type'] == 'bullet':
                self._add_bullet(parsed['text'], parsed['level'])
            elif parsed['type'] == 'text':
                if in_footer:
                    self._add_footer_text(parsed['text'])
                else:
                    self._add_text(parsed['text'])

    def _add_heading(self, text: str, style: str) -> None:
        """Add a heading to the document."""
        # Insert text
        self.requests.append({
            'insertText': {
                'location': {'index': self.current_index},
                'text': text + '\n'
            }
        })

        # Apply heading style
        self.requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': self.current_index,
                    'endIndex': self.current_index + len(text)
                },
                'paragraphStyle': {
                    'namedStyleType': style
                },
                'fields': 'namedStyleType'
            }
        })

        self.current_index += len(text) + 1

    def _add_text(self, text: str) -> None:
        """Add regular text to the document."""
        if not text:
            return

        # Insert text
        start_index = self.current_index
        self.requests.append({
            'insertText': {
                'location': {'index': start_index},
                'text': text + '\n'
            }
        })

        # Find and style @mentions
        mentions = self.find_mentions(text)
        for mention_start, mention_end in mentions:
            self.requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': start_index + mention_start,
                        'endIndex': start_index + mention_end
                    },
                    'textStyle': {
                        'bold': True,
                        'foregroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.2,
                                    'green': 0.4,
                                    'blue': 0.8
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor'
                }
            })

        self.current_index += len(text) + 1

    def _add_footer_text(self, text: str) -> None:
        """Add footer text with distinct styling."""
        if not text:
            return

        start_index = self.current_index
        self.requests.append({
            'insertText': {
                'location': {'index': start_index},
                'text': text + '\n'
            }
        })

        # Apply italic and gray color to footer
        self.requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': start_index + len(text)
                },
                'textStyle': {
                    'italic': True,
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'red': 0.5,
                                'green': 0.5,
                                'blue': 0.5
                            }
                        }
                    }
                },
                'fields': 'italic,foregroundColor'
            }
        })

        self.current_index += len(text) + 1

    def _add_bullet(self, text: str, level: int) -> None:
        """Add a bullet point with proper indentation."""
        start_index = self.current_index

        # Insert text
        self.requests.append({
            'insertText': {
                'location': {'index': start_index},
                'text': text + '\n'
            }
        })

        # Apply bullet styling
        self.requests.append({
            'createParagraphBullets': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': start_index + len(text) + 1
                },
                'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
            }
        })

        # Apply indentation for nested bullets
        if level > 0:
            self.requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': start_index,
                        'endIndex': start_index + len(text) + 1
                    },
                    'paragraphStyle': {
                        'indentStart': {
                            'magnitude': 36 * level,
                            'unit': 'PT'
                        },
                        'indentFirstLine': {
                            'magnitude': 18,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'indentStart,indentFirstLine'
                }
            })

        self.current_index += len(text) + 1

    def _add_checkbox(self, text: str, checked: bool) -> None:
        """Add a checkbox item."""
        start_index = self.current_index

        # Insert checkbox symbol and text
        checkbox_symbol = '☑' if checked else '☐'
        full_text = f"{checkbox_symbol} {text}\n"

        self.requests.append({
            'insertText': {
                'location': {'index': start_index},
                'text': full_text
            }
        })

        # Find and style @mentions in checkbox text
        mentions = self.find_mentions(text)
        for mention_start, mention_end in mentions:
            # Adjust for checkbox symbol and space
            adjusted_start = start_index + len(checkbox_symbol) + 1 + mention_start
            adjusted_end = start_index + len(checkbox_symbol) + 1 + mention_end

            self.requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': adjusted_start,
                        'endIndex': adjusted_end
                    },
                    'textStyle': {
                        'bold': True,
                        'foregroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.2,
                                    'green': 0.4,
                                    'blue': 0.8
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor'
                }
            })

        self.current_index += len(full_text)

    def apply_formatting(self) -> None:
        """
        Apply all formatting requests to the Google Doc.

        Raises:
            Exception: If formatting application fails
        """
        try:
            if self.requests:
                self.service.documents().batchUpdate(
                    documentId=self.document_id,
                    body={'requests': self.requests}
                ).execute()
                print(f"✓ Successfully formatted document with {len(self.requests)} operations")
            else:
                print("⚠ No formatting requests to apply")

        except HttpError as error:
            print(f"✗ An error occurred while formatting: {error}")
            raise

    def get_document_url(self) -> str:
        """
        Get the shareable URL of the created document.

        Returns:
            The URL of the Google Doc
        """
        return f"https://docs.google.com/document/d/{self.document_id}/edit"

    def convert(self, markdown_content: str, doc_title: str) -> str:
        """
        Main method to convert markdown to Google Docs.

        Args:
            markdown_content: The markdown text to convert
            doc_title: The title for the Google Doc

        Returns:
            The URL of the created Google Doc

        Raises:
            Exception: If conversion fails
        """
        try:
            print("\n" + "="*60)
            print("Markdown to Google Docs Converter")
            print("="*60 + "\n")

            # Step 1: Authenticate
            print("[1/4] Authenticating with Google Docs API...")
            self.authenticate()

            # Step 2: Create document
            print("\n[2/4] Creating new Google Doc...")
            self.create_document(doc_title)

            # Step 3: Convert markdown
            print("\n[3/4] Converting markdown content...")
            self.convert_to_google_docs(markdown_content)

            # Step 4: Apply formatting
            print("\n[4/4] Applying formatting...")
            self.apply_formatting()

            # Get the document URL
            doc_url = self.get_document_url()

            print("\n" + "="*60)
            print("✓ Conversion completed successfully!")
            print("="*60)
            print(f"\nYour Google Doc is ready: {doc_url}")
            print("\n")

            return doc_url

        except Exception as e:
            print(f"\n✗ Conversion failed: {e}")
            raise


def main():
    """
    Main function to run the converter.
    """
    # Read the markdown content
    try:
        with open('meeting_notes.md', 'r') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        # If file doesn't exist, use the embedded content
        markdown_content = """# Product Team Sync - May 15, 2023

## Attendees
- Sarah Chen (Product Lead)
- Mike Johnson (Engineering)
- Anna Smith (Design)
- David Park (QA)

## Agenda

### 1. Sprint Review
* Completed Features
  * User authentication flow
  * Dashboard redesign
  * Performance optimization
    * Reduced load time by 40%
    * Implemented caching solution
* Pending Items
  * Mobile responsive fixes
  * Beta testing feedback integration

### 2. Current Challenges
* Resource constraints in QA team
* Third-party API integration delays
* User feedback on new UI
  * Navigation confusion
  * Color contrast issues

### 3. Next Sprint Planning
* Priority Features
  * Payment gateway integration
  * User profile enhancement
  * Analytics dashboard
* Technical Debt
  * Code refactoring
  * Documentation updates

## Action Items
- [ ] @sarah: Finalize Q3 roadmap by Friday
- [ ] @mike: Schedule technical review for payment integration
- [ ] @anna: Share updated design system documentation
- [ ] @david: Prepare QA resource allocation proposal

## Next Steps
* Schedule individual team reviews
* Update sprint board
* Share meeting summary with stakeholders

## Notes
* Next sync scheduled for May 22, 2023
* Platform demo for stakeholders on May 25
* Remember to update JIRA tickets

---
Meeting recorded by: Sarah Chen
Duration: 45 minutes"""

    # Create converter and run
    converter = MarkdownToGoogleDocs()
    doc_url = converter.convert(markdown_content, "Product Team Sync - May 15, 2023")


if __name__ == "__main__":
    main()
