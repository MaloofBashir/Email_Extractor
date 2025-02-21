import email
import imaplib
from email.header import decode_header
import os
import re
from datetime import datetime

FOLDERS=[]
SAVE_FOLDER = "attachments"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    
IMAP_SERVER="imap.gmail.com"
EMAIL_ACCOUNT="maloofbashir70@gmail.com"
EMAIL_PASSWORD="ckcf ssbb cdmz ghyr"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

mail.select("INBOX")

status,message=mail.search(None,'ALL')
email_ids=message[0].split()
email_ids.reverse()

count=0
print(f"total emails= {len(email_ids)}")
for email_id in email_ids[:20]:
    if count<50:
        status, msg_data =  mail.fetch(str(email_id, 'utf-8'), "(RFC822)")
        inner_c=0
        for response_part in msg_data:
            
            if isinstance(response_part, tuple):
                email_body = ""
                msg = email.message_from_bytes(response_part[1])
                
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                from_email = msg.get("From")  # Sender
                from_email = re.search(r'<([^>]+)>', from_email).group(1)
                to_email = msg.get("To")  # Recipient(s)
                cc_email = msg.get("Cc")  # CC (if available)
                bcc_email = msg.get("Bcc")  # BCC (if available)
                date_sent = msg.get("Date")  # Date and time when email was sent
                mystring=date_sent
                # date_sent=date_sent.split("(")[0]
                # date_sent = date_sent.replace(" (UTC)", "")
                # date_obj = datetime.strptime(date_sent, "%a, %d %b %Y %H:%M:%S %z")
                # formatted_date = date_obj.strftime("%d-%m-%Y")
                
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":  # Plain text email body
                        email_body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
                # email_body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    if part.get_content_disposition() == "attachment":
                        folder_name=from_email
                        if not os.path.exists(folder_name):
                            os.makedirs(folder_name)
                        filename = part.get_filename()
                        if filename:
                            filename, encoding = decode_header(filename)[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8")
                            filepath = os.path.join(folder_name, subject)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Saved attachment: {filename}")


               

                print(f"Processing email..... {subject} from email dated {mystring}")
                count=count+1
    else:
        break