from mcp.server.fastmcp import FastMCP
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional, List
import json
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP()

@mcp.tool()
def gmail_tool(
    action: str,
    to_email: str = "",
    subject: str = "",
    body: str = "",
    prompt: str = "",
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    attachment_paths: Optional[List[str]] = None,
    html_body: Optional[str] = None
):
    """
    A Tool for drafting and sending emails through Gmail using given prompts.
    
    Args:
        action (str): Action to perform - "draft", "send", or "draft_from_prompt"
        to_email (str): Recipient email address
        subject (str): Email subject line
        body (str): Email body content (plain text)
        prompt (str): Natural language prompt to generate email content
        cc (str, optional): CC email addresses (comma-separated)
        bcc (str, optional): BCC email addresses (comma-separated)
        attachment_paths (List[str], optional): List of file paths to attach
        html_body (str, optional): HTML version of email body
    
    Returns:
        dict: Result of the operation with status and details
    """
    
    try:
        # Get Gmail credentials from environment variables
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')    
        
        if not gmail_user or not gmail_password:
            return {
                "status": "error",
                "message": "Gmail credentials not found. Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables."
            }
        
        if action == "draft_from_prompt":
            # Generate email content from prompt
            if not prompt:
                return {"status": "error", "message": "Prompt is required for draft_from_prompt action"}
            
            # Simple prompt-based email generation (you can enhance this with AI models)
            draft_content = generate_email_from_prompt(prompt)
            return {
                "status": "success",
                "action": "draft_created",
                "content": draft_content,
                "message": "Email draft created from prompt. Use 'send' action to send it."
            }
        
        elif action == "draft":
            # Create email draft
            if not all([to_email, subject, body]):
                return {"status": "error", "message": "to_email, subject, and body are required for draft action"}
            
            draft = create_email_draft(
                to_email=to_email,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                html_body=html_body,
                attachment_paths=attachment_paths
            )
            
            return {
                "status": "success",
                "action": "draft_created",
                "draft": draft,
                "message": f"Email draft created for {to_email}"
            }
        
        elif action == "send":
            # Send email
            if not all([to_email, subject, body]):
                return {"status": "error", "message": "to_email, subject, and body are required for send action"}
            
            result = send_email(
                gmail_user=gmail_user,
                gmail_password=gmail_password,
                to_email=to_email,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                html_body=html_body,
                attachment_paths=attachment_paths
            )
            
            return result
        
        else:
            return {"status": "error", "message": "Invalid action. Use 'draft', 'send', or 'draft_from_prompt'"}
    
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def generate_email_from_prompt(prompt: str) -> dict:
    """
    Generate email content from a natural language prompt.
    This is a simple implementation - you can enhance it with AI models like OpenAI GPT.
    """
    
    # Simple keyword-based email generation
    prompt_lower = prompt.lower()
    
    if "meeting" in prompt_lower:
        subject = "Meeting Request"
        body = """Dear [Recipient],

I hope this email finds you well. I would like to schedule a meeting to discuss [topic].

Please let me know your availability for the coming week.

Best regards,
[Your Name]"""
    
    elif "follow up" in prompt_lower or "follow-up" in prompt_lower:
        subject = "Follow-up"
        body = """Dear [Recipient],

I wanted to follow up on our previous conversation regarding [topic].

Please let me know if you need any additional information.

Best regards,
[Your Name]"""
    
    elif "thank" in prompt_lower:
        subject = "Thank You"
        body = """Dear [Recipient],

Thank you for [reason]. I really appreciate [specific detail].

Best regards,
[Your Name]"""
    
    else:
        # Generic professional email
        subject = "Professional Inquiry"
        body = f"""Dear [Recipient],

I hope this email finds you well.

{prompt}

Please let me know if you need any additional information.

Best regards,
[Your Name]"""
    
    return {
        "subject": subject,
        "body": body,
        "generated_from": prompt
    }

def create_email_draft(
    to_email: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    html_body: Optional[str] = None,
    attachment_paths: Optional[List[str]] = None
) -> dict:
    """Create an email draft without sending it."""
    
    draft = {
        "to": to_email,
        "subject": subject,
        "body": body,
        "cc": cc,
        "bcc": bcc,
        "html_body": html_body,
        "attachments": attachment_paths or []
    }
    
    return draft

def send_email(
    gmail_user: str,
    gmail_password: str,
    to_email: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    html_body: Optional[str] = None,
    attachment_paths: Optional[List[str]] = None
) -> dict:
    """Send an email through Gmail SMTP."""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc
        
        # Add plain text body
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML body if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Add attachments if provided
        if attachment_paths:
            for file_path in attachment_paths:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        
        # Send email
        recipients = [to_email]
        if cc:
            recipients.extend([email.strip() for email in cc.split(',')])
        if bcc:
            recipients.extend([email.strip() for email in bcc.split(',')])
        
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.quit()
        
        return {
            "status": "success",
            "action": "email_sent",
            "message": f"Email sent successfully to {to_email}",
            "recipients": recipients
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }

# Example usage functions
@mcp.tool()
def send_quick_email(to_email: str, subject: str, message: str):
    """
    Quick function to send a simple email.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        message (str): Email message
    """
    return gmail_tool(
        action="send",
        to_email=to_email,
        subject=subject,
        body=message
    )

@mcp.tool()
def draft_email_from_prompt(prompt: str):
    """
    Create an email draft from a natural language prompt.
    
    Args:
        prompt (str): Natural language description of the email you want to create
    """
    return gmail_tool(action="draft_from_prompt", prompt=prompt)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()