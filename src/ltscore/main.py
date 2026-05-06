from pathlib import Path

import requests
from cysgor import get_score, get_mistakes
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

list_of_languages = {
    "ar": "Arabic",
    "ast": "Asturian",
    "be": "Belarusian",
    "br": "Breton",
    "ca": "Catalan",
    "crh": "Crimean Tatar",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "fa": "Persian",
    "fr": "French",
    "ga": "Irish",
    "gl": "Galician",
    "it": "Italian",
    "ja": "Japanese",
    "km": "Khmer",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sv": "Swedish",
    "ta": "Tamil",
    "tl": "Tagalog",
    "uk": "Ukrainian",
    "zh": "Chinese"
}


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
            self.path = path
        else:
            raise Exception("__ARGUMENT MISSING__: Missing a path or a text.")

    def get_text(self, input_file):
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
        text = self.input_text.strip()
        url = self.source_url
        data = {"text": text, "format": "text", "language": language}

        if language == "cy":
            score = get_score(text)
            mistakes = get_mistakes(text)
            return AnalysisResult(score=score, mistakes=mistakes)
        try:
            res = requests.post(url, data=data).json()["matches"]
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

    def add_column_to_ndjson(self, target_column="prediction"):
        import polars as pl

        df = pl.read_ndjson(self.path)

        scores = []
        mistakes = []
        for row in df[target_column]:
            self.input_text = row
            res = self.find_errors()
            scores.append(res.score)
            mistakes.append(
                [m.subcategory for m in res.mistakes] if res.mistakes else None
            )

        df = df.with_columns(pl.Series("ltscore", scores))
        df = df.with_columns(pl.Series("mistakes_categories", mistakes))
        df.write_ndjson(self.path)
        return df

    def generate_report(self, target_column="prediction"):
        import polars as pl
        df = pl.read_ndjson(self.path)
        report_title = f"{self.path.split('/')[-1]} ({list_of_languages[self.language]})"

        # Step 0: Check whether the file was processed already
        ltscore_col = df.get_column(
            "ltscore", default=pl.Series("ltscore", [None] * len(df))
        )
        if not (ltscore_col.dtype == pl.Float64):
            self.add_column_to_ndjson(target_column=target_column)
            df = pl.read_ndjson(self.path)

        md_report = f"# LTScore Report: {report_title}\n\n"

        # Part 1: Generate the KDE plot of the ltscore
        md_report += f"# Part 1: Visualization\n\n"
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.figure(figsize=(10, 6))
        # Create a KDE plot of the ltscore distribution with a logistic y-axis to better visualize the distribution of the scores, especially if there are many low scores
        sns.kdeplot(
            df["ltscore"], fill=True, color="blue", alpha=0.5, label="LTScore KDE plot"
        )
        plt.legend(loc="upper center")
        plt.ylabel("Density (KDE)")
        plt.xlabel("LTScore / Tokens count per segment")
        plt.title(f"Distribution of LTScore for {report_title}")

        # Add the length of the segments to the plot
        len_segments = [len(s.split(" ")) for s in df[target_column].to_list()]

        # Plot the length of the segments as a secondary x-axis the number elements in the y-axis is shown in the right side of the plot
        plt.twinx()
        sns.histplot(
            len_segments,
            bins=100,
            color="orange",
            alpha=0.5,
            label="Segment Length Distribution",
        )
        plt.yscale("log")
        plt.legend(loc="upper right")
        plt.ylabel("Count (log scale)")

        plot_path = Path(
            "/".join(
                self.path.split("/")[:-1]
                + [self.path.split("/")[-1].split(".")[0] + "_ltscore_kde_plot.png"]
            )
        )
        plt.savefig(plot_path)
        plt.close()

        md_report += f"![LTScore Distribution]({plot_path.name})\n\n"

        # Part 2: Get samples by mistake category
        md_report += f"# Part 2: Descriptive Statistics\n\n"
        md_report += f"- Segments:\n\n"
        md_report += f"  - Total number: **{df.height}**\n\n"
        md_report += f"  - Average length: **{sum(len_segments) / len(len_segments):.2f} tokens**\n\n"

        md_report += f"- Scores:\n\n"
        md_report += f"  - Average: **{df['ltscore'].mean():.2f} mistakes found per 100 tokens**\n\n"
        md_report += f"  - Median: **{df['ltscore'].median():.2f}**\n\n"
        md_report += f"  - Standard Deviation of LTScore: **{df['ltscore'].std():.2f}**\n\n"

        # Part 3: Get samples by mistake category
        md_report += f"# Part 3: Mistake Categories Analysis\n\n"
        md_report += f"## 3.1 Overview\n\n"
        # Add the tables to the report

        # Step 1: Flatten the mistakes_categories and count frequencies
        mistake_counts = df.select(
            pl.col("mistakes_categories")
            .explode()
            .value_counts()
            .alias("mistake_counts")
        ).unnest("mistake_counts")
        # remove rows where the mistakes_categories is `null`
        mistake_counts = mistake_counts.filter(pl.col("mistakes_categories").is_not_null()).sort("count", descending=True)

        # Step 2: Calculate percentages
        total_rows = df.height
        mistake_percentages = mistake_counts.with_columns(
            (pl.col("count") / total_rows * 100).alias("percentage")
        )
        md_report += f"The table below shows the frequency of each mistake category across the segments in the file.\n\n"
        md_report += "| Mistake Category | Count | Percentage |\n"
        md_report += "| --- | --- | --- |\n"
        for row in mistake_percentages.iter_rows():
            md_report += f"| {row[0]} | {row[1]} | {row[2]:.2f}% |\n"

        # Step 3: For each mistake above 1%, find the sentences with highest and lowest ltscore
        result = []
        has_reference = "target" in df.columns  # Check once outside the loop

        for row in mistake_percentages.filter(pl.col("percentage") > 1).iter_rows():
            mistake_category = row[0]
            percentage = row[2]

            # Filter and sort
            sentences_with_mistake = (
                df.filter(pl.col("mistakes_categories").list.contains(mistake_category))
                .sort("ltscore", descending=True)
            )

            if sentences_with_mistake.height == 0:
                continue

            # Access first and last rows
            highest_ltscore_sentence = sentences_with_mistake[target_column][0]
            highest_ltscore = sentences_with_mistake["ltscore"][0]

            lowest_ltscore_sentence = sentences_with_mistake[target_column][-1]
            lowest_ltscore = sentences_with_mistake["ltscore"][-1]

            dict_entry = {
                "mistake": mistake_category,
                "percentage": percentage,
                "highest_ltscore_sentence": highest_ltscore_sentence,
                "highest_ltscore": highest_ltscore,
                "lowest_ltscore_sentence": lowest_ltscore_sentence,
                "lowest_ltscore": lowest_ltscore,
            }

            if has_reference:
                dict_entry["reference_highest_ltscore_sentence"] = sentences_with_mistake["target"][0]
                dict_entry["reference_lowest_ltscore_sentence"] = sentences_with_mistake["target"][-1]

            result.append(dict_entry)

        # Print the result
        md_report += f"## 3.2 Details\n\n"
        md_report += f"The following sections provide examples of the most and least grammatical sentences for each mistake category that appears in more than 1% of the segments, along with their respective LTScore and reference sentence if available.\n\n"
        for i, entry in enumerate(result):
            md_report += f"### 3.2.{i+1} {entry['mistake']}\n\n"
            md_report += f"- Least grammatical sentence containing this category of mistake:\n"
            md_report += f"  - LTScore: {entry['highest_ltscore']}\n"
            md_report += f"  - Segment: *{entry['highest_ltscore_sentence'].strip()}*\n"

            if "reference_highest_ltscore_sentence" in entry:
                md_report += f"  - Reference: *{entry['reference_highest_ltscore_sentence'].strip()}*\n\n"

            md_report += f"- Most grammatical sentence containing this category of mistake:\n"
            md_report += f"  - LTScore: {entry['lowest_ltscore']}\n"
            md_report += f"  - Segment: *{entry['lowest_ltscore_sentence'].strip()}*\n"

            if "reference_lowest_ltscore_sentence" in entry:
                md_report += f"  - Reference: *{entry['reference_lowest_ltscore_sentence'].strip()}*\n\n"

        # Print the markdown report to a file
        report_path =  Path("/".join(self.path.split("/")[:-1] + [self.path.split("/")[-1].split(".")[0] + "_ltscore_report.md"]))

        report_path.write_text(md_report, encoding="utf-8")

        return None


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
        help=f"Language code for the text being analyzed. Language codes: {", ".join([f"{k}: {v}" for k, v in list_of_languages.items()])}",
        required=True,)

    parser.add_argument("input_text",
      nargs="?",
      help="Text to be be parsed")

    parser.add_argument(
        "--target",
        "-t",
        help="Target column (must use with path to a ndjson file)"
        )

    parser.add_argument(
        "--report",
        "-r",
        action=argparse.BooleanOptionalAction,
        help="Generate a detailed report of errors in a file takes a --target argument defaulting to 'prediction' (must use with path to a ndjson or jsonl file)"
        )

    parser.add_argument(
        "--path",
        "-p",
        help="Path to the data file"
        )

    args = parser.parse_args()

    # 1. Check if a positional string was provided first
    if args.input_text:
        wrapper = LTScore(language=args.language, input_text=args.input_text)

        res = wrapper.find_errors()
        print(res.score)

    # 2. Check if a path flag was provided
    elif args.path:
        wrapper = LTScore(language=args.language, path=args.path)
        if args.report:
            wrapper.generate_report(target_column=args.target)
        elif args.target:
            wrapper.add_column_to_ndjson(target_column=args.target)
        else:
            res = wrapper.find_errors()
            print(res.score)

    # 3. Only check for piped data if no arguments were given
    elif not sys.stdin.isatty():
        piped_data = sys.stdin.read()
        if piped_data.strip():
            wrapper = LTScore(language=args.language, input_text=piped_data)
        else:
            print("Error: Piped input was empty.", file=sys.stderr)
            sys.exit(1)

        res = wrapper.find_errors()
        print(res.score)
    else:
        print("Error: No input detected.", file=sys.stderr)
        sys.exit(1)
