import email
import imaplib
from email.header import decode_header
import os
from email.utils import parsedate_to_datetime
import re

# Folder to store everything
SAVE_FOLDER = "attachments"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Clean filename function
def clean_filename(name):
    name = re.sub(r'[\\/*?:"<>|\r\n]', "_", name)  # Remove invalid chars
    name = name.strip()
    return name[:100]  # Optional: limit to 100 chars



# Connect to mail server
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT="gdczainapora@gmail.com"
EMAIL_PASSWORD="sdkn eiic slot jdan"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
mail.select("INBOX")

# Search and process emails
status, message = mail.search(None, 'ALL')
email_ids = message[0].split()
email_ids.reverse()

print(f"Total emails found: {len(email_ids)}")

count = 0
for email_id in email_ids[0:len(email_ids)]:  # Adjust range as needed

    status, msg_data = mail.fetch(str(email_id, 'utf-8'), "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_body = ""
            msg = email.message_from_bytes(response_part[1])

            from_email = msg.get("From")
            to_email = msg.get("To")
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            date_sent = msg.get("Date")
            parsed_date = parsedate_to_datetime(date_sent)
            year_only = parsed_date.year
            month_name = parsed_date.strftime("%B")

            # Get plain text body
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" and part.get_content_disposition() is None:
                    payload = part.get_payload(decode=True)
                    if payload:
                        email_body += payload.decode("utf-8", errors="ignore")

            # Create folders
            if year_only and month_name:
                year_folder = os.path.join(SAVE_FOLDER, str(year_only))
                month_folder = os.path.join(year_folder, month_name)
                os.makedirs(month_folder, exist_ok=True)

                # Save email as PDF
                safe_subject = "".join(x if x.isalnum() or x in " _-" else "_" for x in subject[:50])
               

                # Save attachments
                for part in msg.walk():
                    content_disposition = part.get_content_disposition()
                    if content_disposition == "attachment":
                        filename = part.get_filename()
                        if filename:
                            filename, encoding = decode_header(filename)[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8")
                            filename = clean_filename(filename)
                            attachment_path = os.path.join(month_folder, filename)
                            with open(attachment_path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Saved attachment: {attachment_path}")

            print(f"Processed email: {subject}")
            count += 1
