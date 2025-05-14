from better_profanity import profanity
import requests

# Load default English profanity words
profanity.load_censor_words()

# Load Hungarian profanity list from GitHub
hungarian_profanities_url_1 = "https://raw.githubusercontent.com/pogboard/hungarian_profanity_filter/main/profanity_list.json"
hungarian_profanities_url_2 = "https://raw.githubusercontent.com/censor-text/profanity-list/refs/heads/main/list/hu.txt"

response1 = requests.get(hungarian_profanities_url_1)
response2 = requests.get(hungarian_profanities_url_2)

#json
hungarian_profanities1 = set(response1.json()["hu"])

#txt
hungarian_profanities2 = set(response2.text.lower().splitlines())

# Merge the two sets
hungarian_profanities = hungarian_profanities1.union(hungarian_profanities2)


def has_profanity(text):
    """
    Checks text for profanity in English (using better-profanity) and Hungarian (using wordlist).
    Returns True if any profanity is found, False otherwise.
    """

    # English
    if profanity.contains_profanity(text):
        return True

    # Hungarian
    clean_text = text.lower().translate(str.maketrans('', '', '!@#$%^&*()_+1234567890'))
    return any(word in clean_text.split() for word in hungarian_profanities)

