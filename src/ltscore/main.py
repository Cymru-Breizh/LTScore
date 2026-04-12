import requests
from dataclasses import dataclass
from typing import List


@dataclass
class Mistake:
    category: int
    subcategory: int
    rule_name: str


@dataclass
class AnalysisResult:
    score: float
    mistakes: List[Mistake]


class LTScore:
    def __init__(self, input_text=None, *, path=None):
        self.test_path = "assets/text-sample.txt"
        self.source_url = "https://api.techiaith.cymru/cysill/v2/dl6"
        self.input_text = ""

        if input_text:
            self.input_text = input_text
        elif path:
            self.input_text = self.get_text(path)
        else:
            raise Exception("__ARGUMENT MISSING__: Missing a path or a text.")

    def get_text(self, input_file):
        from pathlib import Path

        # Convert string path to a Path object
        path = Path(input_file)

        # Check if it actually exists before trying to read
        if not path.exists():
            raise FileNotFoundError(f"Could not find the file: {input_file}")

        # Read the entire file as a string
        content = path.read_text(encoding="utf-8")

        return content
    

    def find_errors(self):
        import string

        text = self.input_text
        url = self.source_url
        headers = {"Content-Type": "application/json"}
        data = {"text": text, "format": "text", "language": "cy", "max_errors": 1000}

        # Remove pure spelling mistakes to keep grammatical ones (e.g."NASA" is flagged as a mistake by Cysill)
        res = requests.post(url, headers=headers, json=data).json()["result"]
        mistakes = [
            Mistake(
                category=n["rule_category"]["category"],
                subcategory=n["rule_category"]["subcategory"],
                rule_name=n["rule_name"],
            )
            for n in res if not n["is_spelling"]
        ]

        text_len = len(
            text.translate(str.maketrans("", "", string.punctuation)).split(" ")
        )

        score = 100 * len(mistakes) / text_len

        data = {
            "score": score,
            "mistakes": mistakes
        }

        return AnalysisResult(score=score, mistakes= mistakes)

def run_cli():
    """Entry point for the CLI"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="cysgor",
        description="""!--{|Cymraeg|}--! Amlapiwr Cysill sy'n rhoi sgôr gramadegolrwydd i destunnau Cymraeg. Sgoriau mwy sy'n golygu mwy o wallau gramadegol. Sgoriau llau sy'n golygu bod gramadegolwydd yn well. !--{|English|}--! 
        A wrapper for the Cysill Welsh spell checker to measure the grammaticality of Welsh texts. Higher scores mean more grammatical mistakes. A smaller score means a higher degree of grammaticality.""",
    )

    parser.add_argument("input_text",
      nargs="?",
      help="Text to be be parsed")

    parser.add_argument(
        "--path",
        "-p",
        help="Path to the text-sample.txt or data file"
        )

    parser.add_argument(
        "--test",
        "-t",
        help="Path to the text-sample.txt or data file"
        )

    args = parser.parse_args()

    # 1. Check if a positional string was provided first
    if args.input_text:
        cysgorWrapper = Cysgor(args.input_text)
    # 2. Check if a path flag was provided
    elif args.path:
        cysgorWrapper = Cysgor(path=args.path)
    # 3. Only check for piped data if no arguments were given
    elif not sys.stdin.isatty():
        piped_data = sys.stdin.read()
        if piped_data.strip():
            cysgorWrapper = Cysgor(piped_data)
        else:
            print("Error: Piped input was empty.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: No input detected.", file=sys.stderr)
        sys.exit(1)

    res = cysgorWrapper.find_errors()
    print(res.score)

