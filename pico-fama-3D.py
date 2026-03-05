"""
consider a pico-fermi game, with a random secret comprising four unique digits,
where the player makes unique random (position, value) guesses,
the game responds to each guess with 
"pico" (meaning the guessed value is one of the digits, but at a different position than guessed), or 
"fermi" (meaning the guessed value is the digit at the guessed position) , or 
"no" ( meaning the guessed value is not one of the digits), until the player determines all four values and positions of the secret, 
and create a python console app that plays 100 games,
and plot the results as a three axis stacked bar graph of the fermi guesses, and the non-fermi (pico and no) guesses, 
where the x axis is the total number (pico + fermi + no) of guesses for a game, 
the y axis is the number of fermi guesses for a game,
and the z (vertical) axis is the number of games (of the 100 played) having that total number of guesses. 
"""

import random
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DIGITS = [1,2,3,4,5,6,7,8,9]
NUM_DIGITS = 4
NUM_GAMES = 100000
NO = "no"
PICO = "pico"
FERMI = "fermi"

def generate_secret():
    return random.sample(DIGITS, NUM_DIGITS)

def is_no(secret, digit):
    return digit not in secret

def is_pico(secret, digit):
    return digit in secret

def is_fermi(secret, position, digit):
    return secret[position] == digit

def play_game_for_each_value_guess_positions():
    secret = generate_secret()

    guesses = 0
    no_guesses = 0
    pico_guesses = 0
    fermi_guesses = 0

    found_digit_positions = {}
    open_positions = set(range(NUM_DIGITS))

    for digit in DIGITS:

        available_positions = [p for p in open_positions]
        random.shuffle(available_positions)
        for position in available_positions:
            guesses += 1
            if is_fermi(secret, position, digit):
                fermi_guesses += 1
                found_digit_positions[position] = digit 
                open_positions.discard(position)
                break
            elif is_pico(secret, digit):
                pico_guesses += 1
            elif is_no(secret, digit):
                no_guesses += 1
                break

        if fermi_guesses == NUM_DIGITS:
            break

    if fermi_guesses != NUM_DIGITS:
        print(f"Incorrect number of fermi guesses: {fermi_guesses} should be {NUM_DIGITS}")

    for (pos, val) in found_digit_positions.items():
        if secret[pos] != val:
            print(f"Incorrect guess: secret[pos] {secret[pos]} is not equal to {val}")

    return no_guesses, pico_guesses, fermi_guesses


def play_game_for_each_position_guess_values():
    secret = generate_secret()

    total_guesses = 0
    no_guesses = 0
    pico_guesses = 0
    fermi_guesses = 0

    skip_digits = set()
    found_digit_positions = {}
    found_digits = set()

    for position in range(NUM_DIGITS):
        for digit in DIGITS:
            if digit not in skip_digits:
                total_guesses += 1
                if is_fermi(secret, position, digit):
                    fermi_guesses += 1
                    skip_digits.add(digit)
                    found_digit_positions[position] = digit 
                    break
                elif is_pico(secret, digit):
                    pico_guesses += 1
                    found_digits.add(digit) 
                elif is_no(secret, digit):
                    no_guesses += 1
                    skip_digits.add(digit)

    if fermi_guesses != NUM_DIGITS:
        print(f"Incorrect number of fermi guesses: {fermi_guesses} should be {NUM_DIGITS}")

    for (pos, val) in found_digit_positions.items():
        if secret[pos] != val:
            print(f"Incorrect guess: secret[pos] {secret[pos]} is not equal to {val}")

    return no_guesses, pico_guesses, fermi_guesses


def play_game_guess_all_values_then_guess_their_positions():
    secret = generate_secret()

    no_guesses = 0
    pico_guesses = 0
    fermi_guesses = 0

    pico_digits = set()
    fermi_digit_positions = {}

    # -------------------
    # PASS 1, Set first position, go through digits, if fermi, move to next position etc, until all digits guessed.
    # -------------------
    position = 0
    for digit in DIGITS:

        if is_fermi(secret, position, digit):
            fermi_guesses += 1
            fermi_digit_positions[position] = digit 
            position += 1
            if position == NUM_DIGITS:
                break
        elif is_pico(secret, digit):
            pico_guesses += 1
            pico_digits.add(digit)
        elif is_no(secret, digit):
            no_guesses += 1

    if fermi_guesses + pico_guesses != NUM_DIGITS:
        print(f"Incorrect number of pico digits: {pico_digits} should be {NUM_DIGITS}")

    # -------------------
    # PASS 2, All digits guessed. For each known digit with unknown position, guess position.
    # -------------------
    for digit in pico_digits:

        for position in range(NUM_DIGITS):

            if position not in fermi_digit_positions:
                if is_fermi(secret, position, digit):
                    fermi_guesses += 1
                    fermi_digit_positions[position] = digit 
                    position += 1
                    break
                elif is_pico(secret, digit):
                    pico_guesses += 1
                elif is_no(secret, digit):
                    no_guesses += 1

    if fermi_guesses != NUM_DIGITS:
        print(f"Incorrect number of fermi guesses: {fermi_guesses} should be {NUM_DIGITS}")

    for (pos, val) in fermi_digit_positions.items():
        if secret[pos] != val:
            print(f"Incorrect guess: secret[pos] {secret[pos]} is not equal to {val}")

    return no_guesses, pico_guesses, fermi_guesses


def play_game_random():
    secret = generate_secret()

    # All possible unique (position, value) guesses
    all_guesses = [(pos, val) for pos in range(NUM_DIGITS) for val in DIGITS]
    random.shuffle(all_guesses)

    pico_count = 0
    fermi_count = 0
    no_count = 0
    found_digit_positions = {}
    skip_positions = set()
    skip_digits = set()

    for position, digit in all_guesses:
        if (position not in skip_positions) & (digit not in skip_digits):
            if is_fermi(secret, position, digit):
                fermi_count += 1
                found_digit_positions[position] = digit 
                skip_positions.add(position)
                skip_digits.add(digit)
            elif is_pico(secret, digit):
                pico_count += 1
            elif is_no(secret, digit):
                no_count += 1
                skip_digits.add(digit)

            if fermi_count == NUM_DIGITS:
                break

    if fermi_count != NUM_DIGITS:
        print(f"Incorrect number of fermi guesses: {fermi_count} should be {NUM_DIGITS}")

    for (pos, val) in found_digit_positions.items():
        if secret[pos] != val:
            print(f"Incorrect guess: secret[pos] {secret[pos]} is not equal to {val}")

    return no_count, pico_count, fermi_count


def play_games(id):
    if id == 0:
        results = [play_game_for_each_value_guess_positions() for _ in range(NUM_GAMES)]    
    elif id == 1:
        results = [play_game_for_each_position_guess_values() for _ in range(NUM_GAMES)]
    elif id == 2:
        results = [play_game_guess_all_values_then_guess_their_positions() for _ in range(NUM_GAMES)]
    else:
        results = [play_game_random() for _ in range(NUM_GAMES)]

    games = []
    for no, pico, fermi in results:
        games.append((no, pico, fermi))
    return games


def aggregate_data(games):
    """
    Aggregate by total guesses.

    Returns:
        guess_count_keys: sorted list of unique total guess counts
        guess_count_histogram: histogram of counts of guesses -> number of games having that many guesses
        guess_type_permutations: how many of each type guess -> (num_no, num_pico, num_fermi)
    """
    guess_count_histogram = defaultdict(int)

    guess_type_permutations: dict[int, dict[str, dict[str, int]]]
    guess_type_permutations = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # no, pico, fermi

    for num_no, num_pico, num_fermi in games:
        # histogram of counts of guesses -- each element is number of games having that many guesses
        num_guesses = num_no + num_pico + num_fermi
        guess_count_histogram[num_guesses] += 1

        # permutations of how many of each type of guess
        guess_type_key = str(f"{num_no:02d}{num_pico:02d}{num_fermi:02d}")
        guess_type_permutations[num_guesses][guess_type_key][NO] = num_no
        guess_type_permutations[num_guesses][guess_type_key][PICO] = num_pico
        guess_type_permutations[num_guesses][guess_type_key][FERMI] = num_fermi
    
    guess_count_keys = sorted(guess_count_histogram.keys())
    return guess_count_keys, guess_count_histogram, guess_type_permutations


def plot_3d(guess_count_keys, guess_count_histogram, guess_type_permutations):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    dx = .25
    dy = .25
    expected_value = 0

    for num_guesses in guess_count_keys:
        # count of games having the given number of guesses
        num_games = guess_count_histogram[num_guesses]
        expected_value += num_games * num_guesses

        # iterate through the guess permutations
        y = 0
        sorted_permutations = dict(sorted(guess_type_permutations[num_guesses].items()))
        for guess_counts in sorted_permutations.values():

            no_guesses = (guess_counts[NO] * num_games)/num_guesses
            pico_guesses = (guess_counts[PICO] * num_games)/num_guesses
            fermi_guesses = (guess_counts[FERMI] * num_games)/num_guesses
            y += 1

            # No (bottom stack)
            ax.bar3d(
                num_guesses,        # x = total number of guesses in game 
                y,                  # y = guess permutation index  
                0,                  # z start
                dx,
                dy,
                no_guesses,         # "no" fraction of games having that many guesses
                color='gray'
            )

            # Pico (stacked on no)
            ax.bar3d(
                num_guesses,
                y,
                no_guesses,         # stacked on "no"
                dx,
                dy,
                pico_guesses,       # "pico" fraction of games having that many guesses
                color='blue'
            )

            # Fermi (stacked on pico)
            ax.bar3d(
                num_guesses,
                y,
                no_guesses + pico_guesses,  # stacked on "no" and "pico"
                dx,
                dy,
                fermi_guesses,              # "fermi" fraction of games having that many guesses
                color='orange'
            )

    expected_value = expected_value / NUM_GAMES
    ax.set_xlabel("Total Number of Guesses in Game")
    ax.set_ylabel("Permutations of Guesses")
    ax.set_zlabel("Number of Games")
    ax.set_title(f"Guess Distribution For {NUM_GAMES} Games, EV {expected_value:.2f}")

    plt.tight_layout()
    plt.show()


def main():

    games = play_games(1)
    keys, histogram, permutations = aggregate_data(games)
    plot_3d(keys, histogram, permutations)


if __name__ == "__main__":
    main()