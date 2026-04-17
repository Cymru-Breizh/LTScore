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
    def __init__(self, language, input_text=None, *, path=None):
        self.test_path = "assets/text-sample.txt"
        self.source_url = "http://localhost:8010/v2/check"
        self.input_text = ""
        self.language = language

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
        language = self.language
        text = self.input_text
        url = self.source_url
        headers = {"Content-Type": "application/json"}
        data = {"text": text, "format": "text", "language": language}

        try:
            res = requests.post(url, headers=headers, data=data).json()["matches"]
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Could not connect to a LanguageTool server. Please ensure there is one running on port 8010."
            )

        mistakes = [
            Mistake(
                category=n["rule"]["issueType"],
                subcategory=n["rule"]["category"]["id"],
                rule_name=n["rule"]["id"],
            )
            for n in res
            if n["type"]["typeName"] != "UnknownWord"
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
        prog="ltscore",
        description="""
        A wrapper for the LanguageTool multilingual spell checker to measure the grammaticality of continuous texts. Higher scores mean more grammatical mistakes. A smaller score means a higher degree of grammaticality, zero being no mistake detected.""",
    )

    parser.add_argument(
        "--language",
        "-l",
        help="""Language code for the text being analyzed. Language codes:
            ar (Arabic), 
            ast (Asturian), 
            be (Belarusian), 
            br (Breton), 
            ca (Catalan), 
            da (Danish), 
            de (German), 
            el (Greek), 
            en (English), 
            eo (Esperanto), 
            es (Spanish), 
            fa (Persian), 
            fr (French), 
            ga (Irish), 
            gl (Galician), 
            it (Italian), 
            ja (Japanese), 
            km (Khmer), 
            nl (Dutch), 
            pl (Polish), 
            pt (Portuguese), 
            ro (Romanian), 
            ru (Russian), 
            sk (Slovak), 
            sl (Slovenian), 
            sv (Swedish), 
            ta (Tamil), 
            tl (Tagalog), 
            uk (Ukrainian), 
            zh (Chinese), 
            crh (Crimean Tatar)""")

    parser.add_argument("input_text",
      nargs="?",
      help="Text to be be parsed")

    parser.add_argument(
        "--path",
        "-p",
        help="Path to the data file"
        )

    args = parser.parse_args()

    # 1. Check if a positional string was provided first
    if args.input_text:
        wrapper = LTScore(language=args.language, input_text=args.input_text)
    # 2. Check if a path flag was provided
    elif args.path:
        wrapper = LTScore(language=args.language, path=args.path)
    # 3. Only check for piped data if no arguments were given
    elif not sys.stdin.isatty():
        piped_data = sys.stdin.read()
        if piped_data.strip():
            wrapper = LTScore(language=args.language, input_text=piped_data)
        else:
            print("Error: Piped input was empty.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: No input detected.", file=sys.stderr)
        sys.exit(1)

    res = wrapper.find_errors()
    print(res.score)
