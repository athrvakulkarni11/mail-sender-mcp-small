# Mail Sender MCP Small

A Python tool for drafting and sending emails through Gmail, supporting both direct sending and prompt-based email generation. The tool is designed for easy integration with the MCP (Modular Command Platform) framework and supports attachments, CC/BCC, and HTML email content.

## Features

- **Draft and Send Emails via Gmail:**  
  Send emails directly using Gmail SMTP, or create drafts for review.

- **Prompt-Based Email Generation:**  
  Generate professional email drafts from natural language prompts (e.g., "Schedule a meeting with..." or "Send a thank you note...").

- **Attachments and Formatting:**  
  Supports file attachments and HTML email bodies.

- **CC/BCC Support:**  
  Add CC and BCC recipients easily.

## How It Works

The core of the repository is a tool (`gmail_tool`) that takes actions such as:
- `draft_from_prompt`: Generate an email draft from a simple prompt.
- `draft`: Create a custom draft (needs `to_email`, `subject`, and `body`).
- `send`: Send an email via Gmail SMTP (needs `to_email`, `subject`, and `body`).

Example natural language prompts are converted to subject/body using simple keyword logic, and can be extended with AI models.

## Requirements

- Python 3.7+
- Gmail account with an **App Password** enabled
- The following Python packages:
  - `smtplib`
  - `email`
  - `python-dotenv`
  - MCP framework (`mcp`)

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/athrvakulkarni11/mail-sender-mcp-small.git
    cd mail-sender-mcp-small
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**

    Create a `.env` file in the root directory with your Gmail credentials:
    ```
    GMAIL_USER=your.email@gmail.com
    GMAIL_APP_PASSWORD=your_app_password
    ```
   get from google cloud console , set app password and copy and paste it in an env
4. **Run the MCP server:**
    ```bash
    python gmail_tool.py
    ```

## Usage

You can use the provided MCP tools to:
- **Send a quick email:**
    ```python
    send_quick_email("recipient@example.com", "Subject", "Message body")
    ```
- **Draft an email from a prompt:**
    ```python
    draft_email_from_prompt("Thank the team for their hard work this quarter")
    ```
- **Custom draft or send:**
    ```python
    gmail_tool(
        action="send",
        to_email="recipient@example.com",
        subject="Subject",
        body="Message body",
        cc="cc@example.com",
        bcc="bcc@example.com",
        attachment_paths=["/path/to/file.pdf"],
        html_body="<b>HTML message</b>"
    )
    ```

## Security

- **Do not commit your `.env` file.**
- Use Gmail App Passwords for better security and to avoid exposing your main account password.

## Extending

The email generation from prompts is basic and can be improved by integrating AI/LLM models for more advanced drafting.

## License

This project is provided as-is for educational or personal use. See [LICENSE](LICENSE) if available.

## Author

[athrvakulkarni11](https://github.com/athrvakulkarni11)
