from __future__ import print_function
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credential = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                credential, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "message_text.txt"), "r")
    message_text = f.read()
    message = make_message("thomaswjuell@gmail.com","thomaswilhelmjuell@gmail.com","Test",message_text)

    try:
        created_message = service.users().messages().send(userId='me', body=message).execute()
        print('message sent')
    except Exception as e:
        print(f'Error occured: {e}')

def make_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['To'] = to 
    message['From'] = sender 
    message['Subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

if __name__ == '__main__':
    main()