import re
import requests
from bs4 import BeautifulSoup
from collections import Counter

import matplotlib.pyplot as plt

def plot_frequencies(freqs):
    numbers = list(range(1, len(freqs) + 1))

    plt.figure(figsize=(12, 5))
    plt.bar(numbers, freqs)
    plt.xlabel("Number")
    plt.ylabel("Frequency (last year)")
    plt.title("NJ Jersey Cash 5 – Number Frequencies (Last 12 Months)")
    plt.xticks(numbers)  # show every number on x-axis
    plt.tight_layout()
    plt.show()

def parse_draws_from_txt(path: str):
    """
    Parse a NJ Pick-5 text export like:

        Wednesday, Dec 03, 2025
        5, 7, 25, 35, B: 33
        XTRA: x3
        Est. jackpot: $2.15 Million 

    Returns a list of draws, where each draw is a list of ints.
    """
    draws = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # The line with the main numbers contains "B:"
            if "B:" in line:
                # Keep only the part before "B:" so we skip the bullseye number
                main_part = line.split("B:")[0]

                # Extract all integers from that part
                nums = [int(n) for n in re.findall(r"\d+", main_part)]

                # Sanity check: Pick-5 should give 5 numbers, but keep it flexible
                if nums:
                    draws.append(nums)

    return draws

def compute_frequencies(draws, max_number=45):
    """
    draws: list[list[int]]
    returns: list of counts indexed by number (1..max_number)
    """
    all_nums = [n for draw in draws for n in draw]
    counter = Counter(all_nums)

    # Make a dense list from 1..max_number, filling missing with 0
    freqs = [counter.get(n, 0) for n in range(1, max_number + 1)]
    return freqs

if __name__ == "__main__":
    draws = parse_draws_from_txt("nj_cash5_draws.txt")
    print(f"Fetched {len(draws)} draws")

    freqs = compute_frequencies(draws, max_number=45)
    print("First 10 frequencies:", freqs[:10])

    plot_frequencies(freqs)
