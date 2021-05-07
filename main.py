import Voice_to_text_main
import emailsender
import ticTacToe


def main():
    while True:
        emailsender.say("Welcome to your voice assistant;"
                        "To play tic tac toe, say tic-tac-toe;"
                        "To take notes, say take notes;"
                        "To send emails, say email client;"
                        "To quit, say goodbye")
        answer = emailsender.transcribe(['tic-tac-toe', 'take notes', 'email client', 'goodbye'])
        if answer == 'tic-tac-toe': ticTacToe.game()
        if answer == 'take notes': Voice_to_text_main.Notes()
        if answer == 'email client': emailsender.emailSenderMain()
        if answer == 'goodbye':
            emailsender.say("Goodbye!")
            quit()

# Run Program
main()