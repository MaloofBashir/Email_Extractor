import email
import imaplib
from email.header import decode_header
import os
from email.utils import parsedate_to_datetime
import re

def clean_filename(name):
    # Remove special characters and limit the length
    name = re.sub(r'[\\/*?:"<>|\r\n]', "_", name)
    return name[:100]  # Optional: trim to 100 characters

SAVE_FOLDER = "attachments"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    
IMAP_SERVER="imap.gmail.com"
EMAIL_ACCOUNT="gdczainapora@gmail.com"
EMAIL_PASSWORD="sdkn eiic slot jdan"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

mail.select("INBOX")

status,message=mail.search(None,'ALL')
email_ids=message[0].split()
email_ids.reverse()

print(f"total no of emails id {len(email_ids)}")

count=0
for email_id in email_ids[1:len(email_ids)]:
    if count<50:
        status, msg_data =  mail.fetch(str(email_id, 'utf-8'), "(RFC822)")
        inner_c=0
        for response_part in msg_data:
            
            if isinstance(response_part, tuple):
                email_body = ""
                msg = email.message_from_bytes(response_part[1])

                from_email = msg.get("From")  # Sender
                to_email = msg.get("To")  # Recipient(s)
                cc_email = msg.get("Cc")  # CC (if available)
                bcc_email = msg.get("Bcc")  # BCC (if available)
                date_sent = msg.get("Date")  # Date and time when email was sent
                parsed_date=parsedate_to_datetime(date_sent)

                year_only=parsed_date.year
                month_name = parsed_date.strftime("%B")

                # print(f"year is {year_only} and month name is {month_name}")
                # print(f"Date sent: {date_sent}")

                for part in msg.walk():
                    content_type = part.get_content_type()
                    
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    if content_type == "text/plain":  # Plain text email body
                        email_body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
                # email_body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            filename, encoding = decode_header(filename)[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8")
                                filename = clean_filename(filename)  # <-- Clean filename


                            filepath = os.path.join(SAVE_FOLDER, filename)
                            if year_only and month_name:
                                year_folder = os.path.join(SAVE_FOLDER, str(year_only))
                                month_folder = os.path.join(year_folder, month_name)

                                # Create folders if they don't exist
                                os.makedirs(month_folder, exist_ok=True)

                                # Final path where the attachment will be saved
                                filepath = os.path.join(month_folder, filename+subject+" ")

                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"Saved attachment: {filename} in {month_folder}")

                

                # print(f"From: {from_email}")
                # print(f"date_sent: {date_sent}")
               
                count=count+1
                print(f"Processing email..... {subject} and completed {count} no of emails")
                
    else:
        break