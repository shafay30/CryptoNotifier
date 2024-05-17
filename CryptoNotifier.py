import requests  # Importing requests library for making HTTP requests
import smtplib  # Importing smtplib library for sending emails
import time  # Importing time library for time-related functions

def send_email(receiver_email, subject, message):
    # Add the sender's email address here
    sender_email = "sendersemailhere"  
    # Add the password for the sender email account. App Password will need to be used as shown below:
    # https://www.youtube.com/watch?v=lSURGX0JHbA
    sender_password = "password"  
    
    # SMPT information below is for google's gmail. if you will be using a different mail app
    # update SMPT information accordingly
    
    # SMTP server for gmail to connect to their servers and securely send emails
    smtp_server = "smtp.gmail.com"  
    # Port for SMTP server
    smtp_port = 587  

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    email_message = f"Subject: {subject}\n\n{message}"

    try:
        server.sendmail(sender_email, receiver_email, email_message)
        print(f"{subject} cryptocoin has met your target price of {message}, and the email was successfully sent.")
        print()
        return True
    except:
        print(f"{subject} cryptocoin has met your target price of {message}, there was an error sending the email.")
        print("Email not sent. There was an error sending the email.")
        print()
        return False
    finally:
        server.quit()

def get_crypto_price(crypto_id):
    # CoinGecko API URL for getting cryptocurrency price. Change URL if you want to use a different API
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if crypto_id in data:
        return data[crypto_id]["usd"]
    else:
        return None

while True:
    crypto = input("Enter the crypto you want to track: ")
    target_price = float(input("Enter the target price for the crypto: "))
    notified = False

    while True:
        try:
            price = get_crypto_price(crypto)
            if price is not None:
                if price < target_price:
                    print(f"You will be notified when Target price for {crypto} has been reached!")
                    print()
                    while price is not None and price < target_price:
                        time.sleep(1)  # Check price every second to see if target price has been reached
                        price = get_crypto_price(crypto)
                    if not notified:
                        subject = f"Target price for {crypto} has been reached!"
                        body = f"{crypto} has met your target price of {target_price} and is now at {get_crypto_price(crypto)}"
                        
                        # Enter the receivers email here
                        if send_email("receiveremailhere", subject, body):
                            
                            notified = True
                            break
                elif price >= target_price:
                    response = input(f"{crypto} is higher than or equal to target price, are you sure? (yes/no): ")
                    print()
                    if response.lower() == "yes" or response.lower() == "y":
                        if not notified:
                            subject = f"Target price for {crypto} has been reached!"
                            body = f"{crypto} has met your target price of {target_price} and is now at {get_crypto_price(crypto)}"
                         
                            # Enter the receivers email here
                            if send_email("pyproject1277@gmail.com", subject, body):
                                
                                notified = True
                                break
                            else:
                                print(f"Email not sent. {crypto} is significantly higher than the target price.")
                                print()
                                break
                        elif response.lower() == "no":
                            break
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")
                            print()
            else:
                print("Please enter a valid cryptocurrency.")
                print()
        except ValueError as e:
            print(e)
            print()
            break
