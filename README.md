# AI Email Assistant

This project is an AI-powered email assistant designed to streamline email management. It integrates with Gmail to fetch emails, uses OpenAI's language models for summarization and intent detection, and automates tasks such as replying to emails, scheduling calendar events, sending Slack notifications, and performing web searches. 

## Features

- 📥 **Email Fetching**: Fetch emails from Gmail using the Gmail API.
- 🤖 **AI-Powered Summarization**: Summarize email content using OpenAI's GPT models.
- 🧠 **Intent Detection**: Classify email intent into predefined categories such as scheduling, task requests, status updates, etc.
- ✉️ **Automated Replies**: Generate professional replies to emails based on their content.
- 📅 **Calendar Integration**: Schedule events on Google Calendar for emails with scheduling intent.
- 💬 **Slack Integration**: Send email summaries to a Slack channel.
- 🌐 **Web Search**: Perform contextual web searches to enhance email replies.

## Project Structure

```
AIEmailAssistant/
├── main.py           # Entry point for the assistant workflow
├── gmail.py          # Gmail API integration for fetching and sending emails
├── llm.py            # Core logic for email summarization, intent detection, and reply generation using OpenAI
├── mycalendar.py     # Google Calendar API integration for event scheduling
├── web_search.py     # Web search functionality for generating contextual email replies
├── slack.py          # Slack API integration for notifications
├── database.py       # Database connection and email storage functions
├── db_schema.sql     # Database schema for email and LLM results storage
└── config.json       # Configuration file containing API keys and database settings
```

## Prerequisites

- Python 3.8 or later
- MySQL Database
- Required Python libraries (see [Installation](#installation))
- API keys and credentials:
  - OpenAI API key
  - Google API credentials (for Gmail and Calendar APIs)
  - Slack token and channel ID
  - Google Custom Search Engine (CSE) API key and ID

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/deepkiran-k/deepkiran-kaur-wasserstoff-AiInternTask.git
   cd deepkiran-kaur-wasserstoff-AiInternTask
   ```

2. **Set Up the Environment**:
   Install the required Python libraries:
   ```bash
   pip install openai google-auth google-auth-oauthlib google-api-python-client mysql-connector-python requests
   ```

3. **Set Up the Database**:
   Import the provided `db_schema.sql` file into your MySQL database:
   ```bash
   mysql -u root -p email_assistant < db_schema.sql
   ```

4. **Configure `config.json`**:
   Update `config.json` with your API keys, database credentials, and other configurations:
   ```json
   {
      "dbhost": "localhost",
      "dbuser": "root",
      "dbname": "email_assistant",
      "openai_api_key": "your_open_ai_api_key",
      "google_secret_key": "your_google_secret_key",
      "slack_token": "your_slack_token",
      "google_api_key": "your_google_api_key",
      "google_cse_id": "your_google_cse_id"
   }
   ```

5. **Authenticate Google Services**:
   Place your Google API credentials file (e.g., `credentials.json`) in the project root and authenticate Gmail and Calendar APIs when prompted.

## Usage

1. **Run the Application**:
   Execute the `main.py` script:
   ```bash
   python main.py
   ```

2. **Features Workflow**:
   - The script fetches emails from Gmail.
   - Emails are summarized and classified using OpenAI.
   - Replies are generated and sent automatically.
   - If the email requires scheduling, an event is created on Google Calendar.
   - Summaries are posted to a Slack channel.

## API References

- **Gmail API**: [Documentation](https://developers.google.com/gmail/api)
- **Google Calendar API**: [Documentation](https://developers.google.com/calendar)
- **OpenAI GPT Models**: [Documentation](https://platform.openai.com/docs/)
- **Slack API**: [Documentation](https://api.slack.com/)

## Database Schema

The project uses a MySQL database with the following tables:
- `emails`: Stores email metadata and content.
- `email_attachments`: Stores attachment details linked to emails.
- `llm_results`: Stores results from the LLM, including summaries, detected intent, and generated replies.


## Acknowledgments

- OpenAI for GPT models
- Google for Gmail and Calendar APIs
- Slack for team communication integration
