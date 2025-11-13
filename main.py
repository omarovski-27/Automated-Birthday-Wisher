import datetime
import smtplib
import csv
from email.message import EmailMessage
import pandas as pd
import getpass

def load_birthdays():
    df=pd.read_csv("Birthdates.csv")
    data=df.to_dict(orient="records")
    return data
birthdays_list=load_birthdays()


def check_for_birthdays(birthdays_list):
    today =datetime.datetime.now()
    today_month=today.month
    today_day=today.day
    people_to_email=[]
    for person in birthdays_list:
        birthday_string=person["Birthday"]
        birthday_date=datetime.datetime.strptime(birthday_string,"%d/%m/%Y")
        if birthday_date.month == today_month and birthday_date.day == today_day:
            people_to_email.append(person)

    return people_to_email
people_list_to_send=check_for_birthdays(birthdays_list)

def create_message(name,recepient_email,sender_email):
    msg=EmailMessage()
    msg["Subject"]=f"Happy of birthday!"
    msg["From"]=f"omar.ouran27.3@gmail.com"
    msg["To"]=f"{recepient_email}"
    message_content=f"""\
    عيد ميلاد سعيد يا {name}! 🎉
    العمر كله يارب، وكل سنة وانت طيب!

    May this year bring you health, happiness, and success.
    Wishing you the best from Jordan!

    With love,
    Omar"""
    msg.set_content(message_content)
    return msg
    

def send_email(people_list_to_send,sender_email):
    smtp_object = smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.ehlo()
    smtp_object.starttls()
    sender_email="omar.ouran27.3@gmail.com"
    password=getpass.getpass(f'Enter your password: ')
    smtp_object.login(sender_email,password)
    print(f"Login successful, ready to send emails!")
    
    for person_record in people_list_to_send:        
        name=person_record["Name"]
        recepient_email=person_record["Email"]
        msg=create_message(name,recepient_email,sender_email)
        smtp_object.send_message(msg)
        print(f"Sent birthday to {name} ({recepient_email})")
    smtp_object.quit()
SENDER_EMAIL="omar.ouran27.3@gmail.com"
if people_list_to_send:
    print(f"\nFound {len(people_list_to_send)} birthday(s) today!")
    send_email(people_list_to_send, SENDER_EMAIL)
else:
    print("No birthdays found today. Script finished.")

