import requests
from bs4 import BeautifulSoup
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Function to scrape website fields
def scrape_website(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Select all rows in the table
            rows = soup.select('table tbody tr')

            # Extract and print country names and availability status
            for row in rows:
                try:
                    country = row.select_one('th a').get_text(strip=True)  # Get the country name
                    availability = row.select_one('td span.text-error').get_text(strip=True)  # Get the availability status
                    last_checked = row.select_one('td span.badge').get_text(strip=True)  # Get the last checked time
                    print(f"Country: {country}, Availability: {availability}, Last Checked: {last_checked}")
                    
                    # If appointment is available, send email
                    if availability != "No availability":
                        send_email(country, url)
                except AttributeError:
                    print("Some elements are missing in the row. Skipping this row.")
        else:
            print(f"Failed to fetch the website. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping: {e}")

# Function to send an email via SendGrid
def send_email(country, appointment_url):
    # Create the email content for both recipients
    message_rishav = Mail(
        from_email='sgrishav@gmail.com',
        to_emails='sgrishav@gmail.com',
        subject=f'{country} Appointment Available',
        plain_text_content=f'Book here: {appointment_url}',
        html_content=f'<strong>Book appointment: <a href="{appointment_url}">Click here</a></strong>'
    )
    
    message_basab = Mail(
        from_email='sgrishav@gmail.com',
        to_emails='basabdatta.chaudhury@outlook.com',
        subject=f'{country} Appointment Available',
        plain_text_content=f'Book here: {appointment_url}',
        html_content=f'<strong>Book appointment: <a href="{appointment_url}">Click here</a></strong><br><h1>Rishav Sengupta</h1>'
    )

    try:
        sg = SendGridAPIClient('your-sendgrid-api-key')  # Replace with your SendGrid API key
        response_rishav = sg.send(message_rishav)
        print(f"Email sent to Rishav: {response_rishav.status_code}")
        
        response_basab = sg.send(message_basab)
        print(f"Email sent to Basabdatta: {response_basab.status_code}")

    except Exception as e:
        print(f"Error sending email: {e}")

# URL of the website to scrape
url = 'https://schengenappointments.com/in/dublin/tourism'

# Infinite loop to check the website every 30 minutes
while True:
    scrape_website(url)
    time.sleep(1800)  # Sleep for 30 minutes (1800 seconds)
    
# send grid recovery key:  62BS69MYNRTWRB9PRDE84BRY
