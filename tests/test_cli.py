import subprocess
import polars as pl
from pathlib import Path
from ltscore.main import LTScore, AnalysisResult

# Utility to get the path to your sample file
SAMPLE_FILE = (
    Path(__file__).parent.parent / "src" / "ltscore" / "assets" / "text-sample-br.txt"
)
SAMPLE_FILE_CY = (
    Path(__file__).parent.parent / "src" / "ltscore" / "assets" / "text-sample-cy.txt"
)

def test_cli_path_flag():
    """Test the CLI using the --path argument."""
    result = subprocess.run(
        ["ltscore", "-l", "br", "--path", str(SAMPLE_FILE)], capture_output=True, text=True
    )
    assert result.returncode == 0
    # Check if the output is a float-like string (the score)
    score = float(result.stdout.strip())
    assert 0 <= score
    assert score == 0.2222222222222222


def test_cli_welsh():
    """Test the CLI using the --path argument in Welsh."""
    result = subprocess.run(
        ["ltscore", "-l", "cy", "--path", str(SAMPLE_FILE_CY)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    # Check if the output is a float-like string (the score)
    score = float(result.stdout.strip())
    assert 0 <= score
    assert score == 0.5807200929152149


def test_cli_positional_text():
    """Test the CLI using a direct string of Welsh text."""
    test_text = "Kalz a tud a zo amañ."
    result = subprocess.run(["ltscore", "-l", "br", test_text], capture_output=True, text=True)
    assert result.returncode == 0
    assert float(result.stdout.strip()) == 16.666666666666668


def test_cli_missing_args():
    """Test that the CLI raises the custom exception message when no args are provided."""
    result = subprocess.run(["ltscore"],capture_output=True, text=True)
    assert result.returncode != 0


def test_module_logic():
    """Test the LTScore directly as a python module."""
    text = "Kalz a dud a zo amañ."
    wrapper = LTScore(language="br", input_text=text)
    result = wrapper.find_errors()

    # Verify the custom dataclass structure
    assert isinstance(result, AnalysisResult)
    assert isinstance(result.score, float)
    assert isinstance(result.mistakes, list)

    # If there are mistakes, check the first one is a Mistake object
    # Note: Depending on the API, a short correct sentence might have 0 mistakes
    if len(result.mistakes) > 0:
        from ltscore.main import Mistake

        assert isinstance(result.mistakes[0], Mistake)


def test_add_tlscore_column_to_dataframe():
    """Test that the CLI updates files containing a (nd)json with an additional `ltscore` column containing the score of the target column."""

    entry = """{"source": "'Mañ an dud o tont.", "target": "Les gens arrivent.", "prediction": "Les gens vient."}
{"source": "Un devezh dilabour eo Lun Fask.", "target": "Le lundi de Pâques est un jour férié.", "prediction": "Le lundi de Pâques ai un jours fériée."}"""
    # Create a temporary file with the entry
    temp_file = Path(__file__).parent / "temp_test.ndjson"
    temp_file.write_text(entry)

    # Run the CLI to process the file
    subprocess.run(
        ["ltscore", "-t", "prediction", "-l", "fr", "--path", str(temp_file)],
        capture_output=True,
        text=True,
    )

    # Read the updated file and check for the new column
    df = pl.read_ndjson(temp_file)
    ltscore_col = df.get_column(
        "ltscore", default=pl.Series("ltscore", [None] * len(df))
    )

    # Remove the temporary file
    temp_file.unlink()
    assert ltscore_col is not [None] * len(df)
    assert ltscore_col.dtype == pl.Float64
