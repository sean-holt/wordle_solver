import multiprocessing
from itertools import product
import pandas as pd
from solver import evaluate_guess


if __name__ == '__main__':

    with open('resources/guessable_words.txt', 'r') as fi:
        GUESS_WORDS = [l.strip() for l in fi.readlines()]
    with open('resources/mystery_words.txt', 'r') as fi:
        HIDDEN_WORDS = [l.strip() for l in fi.readlines()]

    pool = multiprocessing.Pool(8)

    combos = list(product(GUESS_WORDS, HIDDEN_WORDS))
    guesses = [t[0] for t in combos]
    hiddens = [t[1] for t in combos]
    values = pool.starmap(evaluate_guess, combos)

    data = pd.DataFrame({
        "Hidden Word": hiddens,
        "Guess Word": guesses,
        "Value": values
    })
    data.to_parquet('resources/data.parquet')
    wide = data.pivot(index="Hidden Word",
                      columns="Guess Word", values="Value")
    wide.to_parquet('resources/wide.parquet')
    alt = data.pivot(index="Guess Word", columns="Hidden Word", values="Value")
    alt.to_parquet('resources/alt.parquet')
