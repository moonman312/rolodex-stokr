import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import config

# Function to load or create the data file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = eval(file.read())  # This is a basic way to store and load data, consider using JSON or a database for more robust solutions
    else:
        data = []
    return data

# Function to save the data to a file
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        file.write(str(data))

# Function to send email notification
def send_email(to_email, subject, message):
    # Replace these values with your own email and app password
    from_email = config.sender_email_address
    app_password = config.app_password

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message to the body of the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())

def check_emails():
    # Replace these values with your own email and app password
    email_address = config.sender_email_address
    app_password = config.app_password

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, app_password)
    mail.select('inbox')

    # Search for emails with a specific subject (e.g., "Interaction Update")
    result, data = mail.search(None, '(SUBJECT "Interaction Update")')
    email_ids = data[0].split()

    # Process each email
    for email_id in email_ids:
        result, message_data = mail.fetch(email_id, '(RFC822)')
        raw_email = message_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract relevant information from the email
        sender = msg.get('From')
        subject = msg.get('Subject')
        body = ""

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8')

        # Process the interaction update
        update_contact_interaction(sender, body)

        # Mark the email as seen
        mail.store(email_id, '+FLAGS', '(\Seen)')

    # Disconnect from the IMAP server
    mail.logout()

# Function to update contact interaction based on email content
def update_contact_interaction(sender, body):
    # Parse the email body to extract relevant information
    lines = body.split('\n')
    name = lines[0].strip()
    interaction_status = lines[1].strip().lower()

    # Update the contact's interaction status
    for contact in data:
        if contact['name'].lower() == name.lower():
            if interaction_status == 'yes':
                contact['last_interaction'] = today.strftime('%Y-%m-%d')
                if len(lines) > 2:
                    next_interaction = lines[2].strip()
                    contact['next_interaction'] = next_interaction
                else:
                    contact['next_interaction'] = (today + timedelta(days=contact['frequency'])).strftime('%Y-%m-%d')
            elif interaction_status == 'no':
                # Do something if needed when interaction is not done
                pass

    # Save the updated data
    data_file = 'contacts_data.txt'
    save_data(data_file, data)

# Main function
def main():
    data_file = 'contacts_data.txt'
    data = load_data(data_file)
    full_message = ''

    # Check and notify about overdue interactions
    today = datetime.now().date()
    overdue_contacts = [contact for contact in data if today > datetime.strptime(contact['next_interaction'], '%Y-%m-%d').date()]

    for contact in overdue_contacts:
        # print(f"Overdue: {contact['name']} - Last Interaction: {contact['last_interaction']}")
        time_since_last_interaction = today - datetime.strptime(contact['last_interaction'], '%Y-%m-%d').date()
        full_message += f"OVERDUE: {contact['name']} \n"
        full_message += f"Don't forget to interact with {contact['name']} today!"
        full_message += f" You haven't spoken in {time_since_last_interaction.days} days."
        full_message += '\n\n'
    full_message += "To update, you can send an email with the subject 'Interaction Update' with the format: \nJohn Doe\nyes\n2024-02-18"
    send_email(config.your_email, 'Rolodex Stokr Overdue Interatction', full_message)

    save_data(data_file, data)
    print(data)

if __name__ == "__main__":
    main()
