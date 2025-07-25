import argparse
import logging
import random
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Homoglyph mapping (extend as needed)
HOMOGLYPHS = {
    'a': ['а', 'ɑ'],  # Cyrillic 'a', Latin 'alpha'
    'b': ['Ь', 'ʙ'],  # Cyrillic soft sign, small capital B
    'c': ['ϲ', 'с'],  # Greek sigma, Cyrillic 's'
    'd': ['ԁ', 'đ'],  # Cyrillic 'd', eth
    'e': ['е', 'є'],  # Cyrillic 'ye', Ukrainian 'ye'
    'f': ['ƒ'],      # florin sign
    'g': ['ɡ', 'ց'],  # Latin script g, Armenian 'ts'
    'h': ['հ', 'ɦ'],  # Armenian 'ho', Latin h with hook
    'i': ['і', 'ı'],  # Cyrillic 'i', dotless i
    'j': ['ϳ'],      # Greek capital letter jota
    'k': ['κ', 'κ'],  # Greek kappa, same as original
    'l': ['Ɩ', 'ӏ'],  # Latin letter l with hook, Cyrillic palochka
    'm': ['м'],      # Cyrillic 'em'
    'n': ['ո', 'п'],  # Armenian 'vo', Cyrillic 'pe' (visually similar in some fonts)
    'o': ['о', 'ο'],  # Cyrillic 'o', Greek omicron
    'p': ['р', 'ρ'],  # Cyrillic 'er', Greek rho
    'q': ['զ'],      # Armenian 'za'
    'r': ['г'],      # Cyrillic 'ge'
    's': ['ѕ', 'ꜱ'],  # Cyrillic 'dze', small capital s
    't': ['т'],      # Cyrillic 'te'
    'u': ['υ', 'ս'],  # Greek upsilon, Armenian 'se'
    'v': ['ν'],      # Greek nu
    'w': ['ѡ'],      # Cyrillic omega
    'x': ['х'],      # Cyrillic 'ha'
    'y': ['у', 'γ'],  # Cyrillic 'u', Greek gamma
    'z': ['z', 'з'],  # original z, Cyrillic 'ze'
    '0': ['O'],
    '1': ['l', 'I'],
    '2': ['Ƨ'],
    '5': ['Ƽ'],
    '6': ['9'],
    '8': ['B'],
    ' ': ['\u00A0'],  # Non-breaking space
    '.': ['․'],      # One dot leader
    '-': ['–'],      # En dash
    '_': ['˯']      # Modifier letter low right corner angle
}


def replace_with_homoglyph(text, probability=0.5):
    """
    Replaces characters in a string with visually similar homoglyphs.

    Args:
        text (str): The input string to be modified.
        probability (float): The probability of replacing each character with a homoglyph.
                              Defaults to 0.5 (50%).

    Returns:
        str: The modified string with homoglyphs.  Returns an empty string if input is invalid

    Raises:
        TypeError: If input text is not a string
        ValueError: If probability is outside of [0,1] range
    """
    if not isinstance(text, str):
        logging.error("Invalid input: Text must be a string.")
        raise TypeError("Input must be a string.")

    if not (0 <= probability <= 1):
        logging.error("Invalid input: Probability must be between 0 and 1.")
        raise ValueError("Probability must be between 0 and 1.")

    result = []
    for char in text:
        char_lower = char.lower()
        if char_lower in HOMOGLYPHS and random.random() < probability:
            replacement_options = HOMOGLYPHS[char_lower]
            replacement = random.choice(replacement_options)
            # Preserve the case of the original character.
            if char.isupper():
                replacement = replacement.upper()
            result.append(replacement)
        else:
            result.append(char)
    return "".join(result)


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Replaces characters in a string with visually similar homoglyphs."
    )
    parser.add_argument(
        "text", help="The input string to be modified."
    )
    parser.add_argument(
        "-p",
        "--probability",
        type=float,
        default=0.5,
        help="The probability of replacing each character (default: 0.5).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output file to write the masked data to. If not specified, prints to stdout.",
    )

    return parser


def main():
    """
    Main function to parse arguments, call the homoglyph replacement function,
    and print or write the output.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        masked_text = replace_with_homoglyph(args.text, args.probability)
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(masked_text)
                logging.info(f"Masked text written to {args.output}")
            except IOError as e:
                logging.error(f"Error writing to file: {e}")
                sys.exit(1)


        else:
            print(masked_text)
    except (TypeError, ValueError) as e:
        logging.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.exception("An unexpected error occurred:") # More verbose logging for unexpected errors
        sys.exit(1)


if __name__ == "__main__":
    main()