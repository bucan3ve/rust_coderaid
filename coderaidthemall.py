import itertools
import random

def generate_codes():
    """Generates all 4-digit codes."""
    return ["".join(code) for code in itertools.product("0123456789", repeat=4)]

def score_code_competitive(code):
    """Scores a code based on the competitive scenario, avoiding easily guessable patterns."""
    score = 0.0

    # Heavy Penalties for common patterns
    if code in ["0123", "1234", "2345", "3456", "4567", "5678", "6789", "9876", "8765", "7654", "6543", "5432", "4321", "3210"]:
        score -= 150.0
    if code[0] == code[1] == code[2] == code[3]:
        score -= 200.0
    if code[0] == code[2] and code[1] == code[3]:
        score -= 75.0
    if code in ['0000', '1000', '2000','9000']:
        score -= 100.0
    # Basic increment
    if int(code[0])+1 == int(code[1]) and int(code[1])+1 == int(code[2]) and int(code[2])+1 == int(code[3]):
        score-=120.0

    # Positional Significance
    if code[0]==code[3]:
        score -= 30.0

    # Year Bonuses
    year_range_90s = [f"{i:02d}" for i in range(90, 100)]
    year_range_00s = [f"{i:02d}" for i in range(0, 11)]
    if code[0:2] in year_range_90s:
        score += 60.0
    if code[2:4] in year_range_90s:
        score += 50.0
    if code[0:2] in year_range_00s or code[2:4] in year_range_00s:
         score += 40.0

    if code[0:2].isdigit() and code[2:4].isdigit():
       month = int(code[0:2])
       day = int(code[2:4])
       if (1<= month <=12 and 1<= day <= 31):
                score += 55 if code[0:2] in year_range_90s or code[2:4] in year_range_90s else 30

    # Sequence Complexity
    diff1 = int(code[1])-int(code[0])
    diff2 = int(code[2])-int(code[1])
    diff3 = int(code[3])-int(code[2])
    if diff1 == diff2 and diff2 == diff3 and diff1 !=1 and diff1 != -1:
        score += 60
    if diff1 !=0 and diff2 !=0 and diff3!=0 and diff1 != diff2 and diff2 != diff3:
         score += 70
    if (int(code[0])+2 == int(code[1]) and int(code[1])+2 == int(code[2]) and int(code[2])+2 == int(code[3])) or \
       (int(code[0])-2 == int(code[1]) and int(code[1])-2 == int(code[2]) and int(code[2])-2 == int(code[3])):
           score += 75

    # Modified Keypad Proximity
    keypad_patterns = {
        "1258": 4, "4572": 4, "7851": 4, "2369": 4, "3685": 4,
        "2574": 4, "1375": 4, "7953": 4, "1482": 4, "9637": 4,
         "1470": 1, "2580": 1, "3690": 1, "1236": 1, "4569": 1, "7896":1, "1254": 1, "7852": 1, "1478": 1,
        "1254":1, "7852": 1
    }
    for pattern, turns in keypad_patterns.items():
        if code in pattern:
            score += 50.0 / turns
            break

    # Uncommon Sequences
    if code in ["2468", "1357", "8642", "7531", "1368", "7524", "8631","9753","1597","6482","7240","9361", "2581", "3692","4713"]:
        score += 100.0

    # Randomness/Logic Mix
    unique_digits = len(set(code))
    if unique_digits == 4:
      score += 20.0
    elif unique_digits == 3:
        score += 10.0

    return score
def sort_and_output(codes, scoring_function, filename):
    """Sorts and outputs codes based on score with random shuffling."""
    scored_codes = [(code, scoring_function(code)) for code in codes]
    sorted_codes = sorted(scored_codes, key=lambda item: item[1], reverse=True)

    # Group by score and shuffle within groups
    grouped_codes = {}
    for code, score in sorted_codes:
        if score not in grouped_codes:
            grouped_codes[score] = []
        grouped_codes[score].append(code)

    shuffled_codes = []
    for score, codes in grouped_codes.items():
      random.shuffle(codes)
      shuffled_codes.extend(codes)

    with open(filename, "w") as f:
         for code in shuffled_codes:
             f.write(f"{code}\n")


if __name__ == "__main__":
    codes = generate_codes()
    sort_and_output(codes,  score_code_competitive, "codes_competitive.txt")
    print("Codes generated and written to 'codes_competitive.txt'")
