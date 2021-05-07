import speech_recognition as sr
import pyttsx3 as reader
import random

s = reader.init()
r = sr.Recognizer()
r.energy_threshold = 2000
space = None


def insertLetter(letter, pos):
    space[pos] = letter


def freeSpace(pos):
    return space[pos] == ' '


def myMove():
    run = True
    while run:

        print('Say a square from (1-9)')
        with sr.Microphone() as source:


            audio = r.listen(source)


            try:

                #s.say("Your move. ")
                #s.runAndWait()



                move = r.recognize_google(audio)
                #s.runAndWait()

                #makes sure the audio is an int
                move = int(move)

                #makes sure your number is within range of possible moves
                if move > 0 and move < 10:
                    #if there's a free space where your move was-
                    if freeSpace(move):
                        #move is over, so stop loop
                        run = False
                        #make move
                        insertLetter('X', move)
                    else:
                        print('Not there !')
                else:
                    print('Not in range!')

            except:
                print("Sorry couldn't recognize your voice")

def isWinner(sp, le):
    #this will return each combination of winners and then we will check if this is true, if so term game
    return (sp[7] == le and sp[8] == le and sp[9] == le) or (sp[4] == le and sp[5] == le and sp[6] == le) or (
    sp[1] == le and sp[2] == le and sp[3] == le) or (sp[1] == le and sp[4] == le and sp[7] == le) or (
                       sp[2] == le and sp[5] == le and sp[8] == le) or (
                       sp[3] == le and sp[6] == le and sp[9] == le) or (
                       sp[1] == le and sp[5] == le and sp[9] == le) or (sp[3] == le and sp[5] == le and sp[7] == le)

def compMove():
    #enumarate gives all values in list - gives us any empty space
    possibleMoves = [x for x, letter in enumerate(space) if letter == ' ' and x != 0]
    move = 0

    #check if there's a move for computer to take to win
    for let in ['O', 'X']:
        for i in possibleMoves:
            #creates new list in memory
            boardCopy = space[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move

    cornersOpen = []
    for i in possibleMoves:
        #checks if square 1, 3, 7, or 9 are open, updates list available to user and computer
        if i in [1, 3, 7, 9]:
            cornersOpen.append(i)

    #elect randomly from list available of open corners
    if len(cornersOpen) > 0:
        move = randomizer(cornersOpen)
        return move


    edgesOpen = []
    for i in possibleMoves:
        if i in [2, 4, 6, 8]:
            edgesOpen.append(i)

    if len(edgesOpen) > 0:
        move = randomizer(edgesOpen)

    return move


def randomizer(li):
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]


#this will tell us if the board
def isFull(board):
    if board.count(' ') > 1:
        return False
    else:
        return True


def main():
    printSpaces(space)

    #while list index of all avaialbe spaces is not full (you can play)
    while not (isFull(space)):
        #if you haven't won (checks all lists of winning possible combinations with the opponents letter)
        if not (isWinner(space, 'O')):
            #call move function --> allows you to place a letter X
            myMove()
            #prints the space from what you called
            printSpaces(space)
        else:
            print('You lose!')
            break

        #now check --> if you haven't won
        if not (isWinner(space, 'X')):
            #gets computers move
            move = compMove()
            #if possible spaces = 0 without someone winning, we must have tied
            if move == 0:
                print('Tie Game!')
            #otherwise, insert letter into chosen space
            else:
                insertLetter('O', move)
                print('Opponent went to space # ', move, ':')
                printSpaces(space)
        else:
            print('You won! Congrats')
            break

    if isFull(space):
        print('Tie')


def printSpaces(space):
    print('    |      |')
    print(' ' + space[1] + '  | ' + space[2] + '    | ' + space[3])
    print('    |      |')
    print('-----------------')
    print('    |      |')
    print(' ' + space[4] + '  | ' + space[5] + '    | ' + space[6])
    print('    |      |')
    print('-----------------')
    print('    |      |')
    print(' ' + space[7] + '  | ' + space[8] + '    | ' + space[9])
    print('    |      |')


def game():
    global space

    while True:

        print('TIC TAC TOE (VOICE ONLY EDITION)')
        print('Would you like to play? (say yes or no)')

        with sr.Microphone() as source:
            audio = r.listen(source)

            try:
                answer = r.recognize_google(audio, language="en-US")

                if answer == 'yes':
                    #inserts spaces for a board
                    space = [' ' for x in range(10)]
                    print('-----------------------------------')
                    main()
                elif answer == 'I don\'t know':
                    print('make up your mind')
                elif answer == 'no':
                    return
            except:
                print(answer)
                print('sorry, I\'m not sure what you said.')