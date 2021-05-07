import speech_recognition as sr
import pyttsx3 as reader
import mysql.connector
import smtplib
from email.mime.text import MIMEText

s = reader.init()
s.setProperty('rate', 175)
voices = s.getProperty('voices')
s.setProperty('voice', voices[1].id)
r = sr.Recognizer()
r.energy_threshold = 4000
conn = mysql.connector.connect(host='localhost', database='email', user='root', password='')
cursor = conn.cursor()


def emailSenderMain():
    say("To manage your contacts, say manage contacts;"
        "To send an email, say send email;"
        "To go back to the main menu, say main menu")

    answer = transcribe(["manage contacts", "send email", "main menu"])

    if answer == "manage contacts": contactsMenu()
    if answer == "send email": sendEmail()
    if answer == "main menu": return


def contactsMenu():
    say("To list your contacts, say list contacts;"
        "To add a new contact, say add contact;"
        "To update a contact, say update contact;"
        "To delete a contact, say delete contact;"
        "To go back, say back to menu")

    answer = transcribe(["list contacts", "add contact", "update contact", "delete contact", "back to menu"])

    if answer == "list contacts": listContacts()
    if answer == "add contact": newContact()
    if answer == "update contact": updateContact()
    if answer == "delete contact": deleteContact()
    if answer == "back to menu": return emailSenderMain()

    return contactsMenu()


def listContacts():
    print("List Contacts")
    cursor.execute("SELECT name FROM contact")
    contacts = cursor.fetchall()

    if not contacts:
        say("No contacts found! Sending you back")
        return
    else:
        say("{} contacts found.".format(cursor.rowcount))
        say("These are the names of your contacts: {}".format(contacts))
        say("Sending you back!")
        return


def newContact():
    print("New contact")
    contact = contactInput()

    try:
        cursor.execute("INSERT INTO contact (name, email) VALUES ('{}', '{}')".format(contact[0], contact[1]))
        conn.commit()
        say("Added new contact successfully!")
    except:
        say("I could not add new contact")


def contactInput():
    while True:
        say("Please type the name of your contact, preferably just the first or last name.")
        name = input()
        say("Is this the correct name: {}".format(name))
        if transcribe(["yes", "no"]) == "yes": break

    while True:
        say("Please type the email of your contact.")
        email = input()
        say("Is this the correct email: {}".format(email))
        if transcribe(["yes", "no"]) == "yes": break

    return [name, email]


def updateContact():
    print("Update contact")
    cursor.execute("SELECT id, name FROM contact")
    contacts = cursor.fetchall()

    if cursor.rowcount == 0:
        say("You have no contacts to update. Sending you back")
        return

    while True:
        say("Please type the name of your contact")
        name = input()
        for contact in contacts:
            if name in contact[1]:
                say("Found contact")
                updatedContact = contactInput()

                try:
                    cursor.execute("UPDATE contact SET name='{}', email='{}' WHERE id={}".format(updatedContact[0], updatedContact[1], contact[0]))
                    conn.commit()
                    say("Updated contact successfully! Sending you back")
                except:
                    say("I could not update that contact. Sending you back")

                return

            else:
                say("Could not find contact;"
                    "To hear a list of your contacts, say list;"
                    "To try again, say try again;"
                    "To cancel, say cancel")
                answer = transcribe(['list', 'try again', 'cancel'])
                if answer == 'list': listContacts()
                if answer == 'cancel': return


def deleteContact():
    print("Delete contact")
    cursor.execute("SELECT id, name FROM contact")
    contacts = cursor.fetchall()

    if cursor.rowcount == 0:
        say("You have no contacts to delete. Sending you back")
        return

    while True:
        say("Please type the name of your contact")
        name = input()
        for contact in contacts:
            if name in contact[1]:
                try:
                    cursor.execute("DELETE FROM contact WHERE id={}".format(contact[0]))
                    conn.commit()
                    say("Deleted contact successfully! Sending you back")
                except:
                    say("I could not delete that contact. Sending you back")

                return

            else:
                say("Could not find contact;"
                    "To hear a list of your contacts, say list;"
                    "To try again, say try again;"
                    "To cancel, say cancel")
                answer = transcribe(['list', 'try again', 'cancel'])
                if answer == 'list': listContacts()
                if answer == 'cancel': return


def sendEmail():
    print("Send email")
    cursor.execute("SELECT * FROM contact")
    contacts = cursor.fetchall()

    if cursor.rowcount == 0:
        say("You have no contacts to send an email to;"
            "To add a new contact, say new contact;"
            "To cancel, say cancel")
        answer = transcribe(['new contact', 'cancel'])
        if answer == 'new contact': newContact()
        if answer == 'cancel': return

    while True:
        say("Please type the name of the contact you would like to send an email to.")
        name = input()
        for contact in contacts:
            if name in contact[1]:
                say("Found contact.")
                while True:
                    say("Please say a subject for your email")
                    subject = transcribe()
                    say("Your subject line is: {}".format(subject))
                    say("To continue, say continue;"
                        "To try again, say try again;"
                        "To cancel, say cancel")
                    answer = transcribe(['continue', 'try again', 'cancel'])
                    if answer == 'continue': break
                    if answer == 'cancel': return

                content = ""
                while True:
                    say("Please say the content of your email")
                    if answer == 'add more':
                        content += "\n", transcribe()
                    else:
                        content = transcribe()
                    say("Your email's content is: {}".format(content))
                    say("To send email, say continue;"
                        "To add more, say add more;"
                        "To try again, say try again;"
                        "To cancel, say cancel")
                    answer = transcribe(['continue', 'add more', 'try again', 'cancel'])
                    if answer == 'cancel': return
                    if answer == 'continue':
                        email = MIMEText(content)
                        email['From'] = "email@email.com"
                        email['To'] = contact[2]
                        email['Subject'] = subject

                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login("comp264project@gmail.com", "*a)PGaHHk@LCbU&3G3pBf%mnM8_(Uc9)")  # Feel free to hack this account
                        server.send_message(email)
                        server.quit()

                        say("Email has been sent")

                        return


def say(text):
    s.say(text)
    s.runAndWait()


def transcribe(options=[]):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Speak")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="en-US")

            if options:
                if text not in options:
                    print(text)
                    say("Please try again. The options are: {}".format(options))
                    text = transcribe(options)
        except:
            say("Please try again.")
            text = transcribe()

    return text
