import subprocess
from pathlib import Path
from ltscore.main import LTScore, AnalysisResult

# Utility to get the path to your sample file
SAMPLE_FILE = (
    Path(__file__).parent.parent / "src" / "ltscore" / "assets" / "text-sample-br.txt"
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
