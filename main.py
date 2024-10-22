import requests
from bs4 import BeautifulSoup
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

# Fetch secrets from environment variables
FROMEMAIL = os.environ.get('FROMEMAIL')
TOEMAILBC = os.environ.get('TOEMAILBC')
TOEMAILRSG = os.environ.get('TOEMAILRSG')
YOURSENDGRIDAPIKEY = os.environ.get('YOURSENDGRIDAPIKEY')

# Function to scrape website fields
def scrape_website(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Save the raw HTML to a file for debugging
            with open("sample-2.txt", 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            
            # Select all rows in the table
            rows = soup.select('table tbody tr')

            # Extract and print country names and availability status
            for row in rows:
                try:
                    country = row.select_one('th a').get_text(strip=True)  # Get the country name
                    
                    # Get availability status (if exists)
                    availability_element = row.select_one('td span.text-success')
                    no_availability_element = row.select_one('td span.font-bold')

                    availability = availability_element.get_text(strip=True) if availability_element else None
                    no_availability = no_availability_element.get_text(strip=True) if no_availability_element else None
                    
                    last_checked = row.select_one('td span.badge').get_text(strip=True)  # Get the last checked time
                    
                    # Log the fetched data for debugging
                    #print(f"Country: {country}, Availability: {availability or no_availability}, Last Checked: {last_checked}")
                    # print(availability_element )
                    # print(no_availability)
                    # print(country+"......................")
                    #print(no_availability + "no Avail" )
                    # Write availability status to a file
                    with open("row.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{country}: {availability or no_availability}\n")

                    # If appointment is available, send email
                    if no_availability or availability  != None:
                        print(country)
                        send_email(country, url)

                except AttributeError as e:
                    print(f"Error parsing row: {e}. Skipping this row.")

        else:
            print(f"Failed to fetch the website. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping: {e}")

# Function to send an email via SendGrid
def send_email(country, appointment_url):
    # Create the email content for both recipients
    message_rishav = Mail(
        from_email= FROMEMAIL,
        to_emails=TOEMAILRSG ,
        subject=f'{country} Appointment Available',
        plain_text_content=f'Book here: {appointment_url}',
        html_content=f'<strong>Book appointment: <a href="{appointment_url}">Click here</a></strong>'
    )
    
    message_basab = Mail(
        from_email= FROMEMAIL,
        to_emails= TOEMAILBC,
        subject=f'{country} Appointment Available: High Importance!',
        plain_text_content=f'Book here: {appointment_url}',
        html_content=f'<strong>Book appointment: <a href="{appointment_url}">Click here</a></strong><br><h1>Rishav Sengupta</h1>'
    )

    try:
        sg = SendGridAPIClient(YOURSENDGRIDAPIKEY)  # Replace with your SendGrid API key
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


