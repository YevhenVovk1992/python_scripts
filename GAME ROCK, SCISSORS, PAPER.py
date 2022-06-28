from random import choice

ROCK = 'rock'
SCISSORS = 'scissiors'
PAPER = 'paper'
OPTIONS = [ROCK, SCISSORS, PAPER]
MAPPING = {ROCK: SCISSORS, SCISSORS: PAPER, PAPER: ROCK}


# Function that determinate the winner
def get_winner(user_val: str, computer_var: str):
    if user_val == computer_var:
        print('WRAW!')
    elif MAPPING[user_val] == computer_var:
        print('YOU WIN')
    else:
        print('YOU LOSE')
    print('If you want to exit, type "end"')
    print()


# Function that determinate the correct input
def validate_input(user_val: str) -> bool:
    return user_val in OPTIONS


# Game loop
print('', 'Welcome to ma game!', sep='\t')
print('', '!-----------------!', sep='\t')
while True:
    user_val = input(f'Type one of the values: {", ".join(OPTIONS)} \n')
    if user_val == 'end':
        print('', 'Good luck :)', sep='\t')
        break
    elif not validate_input(user_val):
        print('Wrong value. Try again.')
        continue
    computer_var = choice(OPTIONS)
    print('Computer value:', computer_var)
    get_winner(user_val, computer_var)
