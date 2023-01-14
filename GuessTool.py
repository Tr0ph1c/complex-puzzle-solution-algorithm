import random
import re

REGEX_FILTER = r'^[0-3]{4}$'

ITERATIONS_NUMBER = 500
BATCHMODE = 0
CUSTOMEMODE = 0
DEBUGMODE = 0

pastguess = [4, 4, 4, 4] # For error handling in case two
                         # consecutive guesses were the same
guess    = [0, 0, 0, 0]
password = [3, 3, 1, 2]
truevals = [0, 0, 0, 0]

choices = [-1, -1, -1, -1]

possibilities = [[0, 1, 2, 3],
                 [0, 1, 2, 3],
                 [0, 1, 2, 3],
                 [0, 1, 2, 3]]


intro = '''
BATCH : runs ITERATION_NUMBER (500) of games and gives statistics of the algorithm's performance at the end.\n
CUSTOM: asks the user for a certain starting guess and a certain password to guess and runs a simulation
of the algorithm guess by guess. (used for testing a certain case)\n
DEBUG:  runs a singular game and moves through the algorithm guess by guess.\n
CHEAT:  tries to guess an unknown password and asks for the evaluation to be entered by the user.\n
'''
def UI():
    global ITERATIONS_NUMBER
    global BATCHMODE
    global CUSTOMEMODE
    global DEBUGMODE

    while True:
        print(intro)
        BATCHMODE = CUSTOMEMODE = DEBUGMODE = 0
        inp = input('Choose mode ( 0 to exit ):\n[1] BATCH\n[2] CUSTOM\n[3] DEBUG\n[4] CHEAT(Default)\n')
        try:
            inp = int(inp)
        except: pass

        if inp == 0:   break
        elif inp == 1: BATCHMODE = 1
        elif inp == 2: CUSTOMEMODE = 1
        elif inp == 3: DEBUGMODE = 1

        entry()

def entry():
    if BATCHMODE:
        i = 1
        counts = []
        while i <= ITERATIONS_NUMBER:
            reset()
            count = main()
            print(f"--- DONE ITERATION {i} : {count} tries ---")
            counts.append(count)
            i += 1
        print(f'Finished with the following statistics:')
        print(f'- An average try count of {sum(counts)/len(counts)}')
        print(f'- A maximum try count of  {max(counts)}')
    elif CUSTOMEMODE:
        reset()

        inpGuess = re.search(REGEX_FILTER, input('Enter initial guess: '))
        inpPass = re.search(REGEX_FILTER, input('Enter password to guess: '))

        if inpGuess and inpPass:
            for i in range(4):
                guess[i] = int(inpGuess.group()[i])
                password[i] = int(inpPass.group()[i])
            main()
        else:
            print('Invalid Input(s).')
    elif DEBUGMODE:
        reset()
        main()
    else:
        reset()
        cheatMode()
    input('DONE, RETURNING TO MAIN MENU...')

def reset():
    global password
    global possibilities
    global truevals
    global choices
    global pastguess

    for i in range(4): #random password
        password[i] = random.randint(0,3)

    possibilities = [[0, 1, 2, 3],
                     [0, 1, 2, 3],
                     [0, 1, 2, 3],
                     [0, 1, 2, 3]]

    truevals = [0, 0, 0, 0]
    choices = [-1,-1,-1,-1]
    pastguess = [4,4,4,4]

def cheatMode():
    global guess
    global truevals
    global possibilities

    for i in range(4): #first run randomization
        guess[i] = random.randint(0,3)

    while True:
        print('\n'*25)
        print(f'Guess:  {guess}\n')
        inpTV = re.search(REGEX_FILTER, input('Please enter the evaluation of the guess (i.e. 0021):\n'))
        if not inpTV: input('Invalid Input(s)'); continue
        if (sum(truevals) == 8): break # once all values in truevals are 2
        if catchError(): # Repeating Guesses Handling
            print('Repition!')
            exit()
        evalPossibilities()
        evalChoices()
        print('---------------')
        newGuess()

    print(f'\n\n\nWE FOUND THE PASSWORD!\n{guess}\n=================\n')

def main():
    global guess
    global truevals
    global password
    global possibilities
        
    if not CUSTOMEMODE:
        for i in range(4): #first run randomization
            guess[i] = random.randint(0,3)
    
    counter = 1
    while True:
        evaluate()
        print(f'Guess:  {guess}\nActual: {password}\nTruths: {truevals}\n')
        if (sum(truevals) == 8): break # once all values in truevals are 2
        if catchError(): # Repeating Guesses Handling
            print('Repition!')
            exit()
        evalPossibilities()
        evalChoices()
        print(f'NEXT GUESS: \nChoice: {choices}')
        printPossibs()
        print('---------------')
        newGuess()
        if not BATCHMODE: input()
        counter += 1

    print(f'\n\n\nTHE PASSWORD IS {guess}\n=================\n')
    return counter

# 0 means not right
# 1 means right but not in current pos
# 2 means right in the current pos
def evaluate():
    global guess
    global truevals
    global password

    tempPassword = password.copy()
    
    truevals = [0,0,0,0]

    for i in range(4):
        if guess[i] == password[i]:
            truevals[i] = 2
            tempPassword.remove(guess[i])

    for i in range(4):
        if guess[i] in tempPassword and truevals[i] != 2:
            tempPassword.remove(guess[i])
            truevals[i] = 1

def catchError():
    global guess
    global pastguess

    if guess == pastguess:
        print(f'{guess} = {pastguess}')
        return 1
    
    pastguess = guess.copy()
    return 0

def evalPossibilities():
    global guess
    global truevals
    global possibilities

    confirmedvalues = []

    for i in range(4):
        #IF 0, remove the possibility from all slots
        if truevals[i] == 0:
            try:
                possibilities[i].remove(guess[i])
                
                if guess[i] in confirmedvalues: continue
                for p in possibilities:
                    p.remove(guess[i])
            except ValueError:
                pass
        #IF 1, complex beyong comprehension
        elif truevals[i] == 1:
            confirmedvalues.append(guess[i])
            try: 
                possibilities[i].remove(guess[i]) 
            except ValueError: pass
        #IF 2, block choosing
        else:
            possibilities[i].clear()
            choices[i] = 'x'

def evalChoices():
    global guess
    global truevals
    global choices
    global possibilities

    pastchoices = choices.copy()

    for i in range(4):
        if truevals[i] == 1:
            for p in range(4):
                if p != i and (truevals[p] != 2) and (choices[p] == -1) and (guess[i] in possibilities[p]):
                    choices[p] = guess[i]
                    break

    for i in range(4):
        if choices[i] == pastchoices[i] and choices[i] != 'x':
            choices[i] = -1

def newGuess():
    global guess
    global truevals
    global possibilities

    for i in range(4):
        if truevals[i] != 2:
            guess[i] = choose(i)
            

def choose(slot):
    global possibilities
    global choices

    if choices[slot] == -1:
        return possibilities[slot][random.randrange(0,len(possibilities[slot]))]
    else:
        return choices[slot]

def printPossibs():
    global possibilities

    index = 0
    while True:
        if (len(possibilities[0])-1 < index and len(possibilities[1])-1 < index and len(possibilities[2])-1 < index and len(possibilities[3])-1 < index): break
        print("Possibs: ", end='')
        for i in range(4):
            if (len(possibilities[i]) - 1 < index): print(' | ', end=''); continue
            print(possibilities[i][index], end='| ')
        print()
        index += 1

if __name__ == "__main__":
    UI()