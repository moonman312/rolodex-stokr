import os
import smtplib
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
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())

# Main function
def main():
    data_file = 'contacts_data.txt'
    data = load_data(data_file)

    # Check and notify about overdue interactions
    today = datetime.now().date()
    overdue_contacts = [contact for contact in data if today > datetime.strptime(contact['next_interaction'], '%Y-%m-%d').date()]

    for contact in overdue_contacts:
        print(f"Overdue: {contact['name']} - Last Interaction: {contact['last_interaction']}")
        send_email('your_email@gmail.com', f"Overdue: {contact['name']}", f"Don't forget to interact with {contact['name']} today!")

    # Update last_interaction and next_interaction dates
    for contact in data:
        contact['last_interaction'] = today.strftime('%Y-%m-%d')
        contact['next_interaction'] = (today + timedelta(days=contact['frequency'])).strftime('%Y-%m-%d')

    # Save the updated data
    save_data(data_file, data)

if __name__ == "__main__":
    main()
