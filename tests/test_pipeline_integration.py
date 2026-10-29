import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EndToEndPipelineTests(unittest.TestCase):
    def test_normalized_fixture_runs_all_layers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "lake"
            command = [
                sys.executable, str(ROOT / "scripts/process_election_results.py"),
                "--input", str(ROOT / "examples/election-results-normalized.csv"),
                "--contract", str(ROOT / "contracts/tse/election-results.v1.json"),
                "--output", str(output),
                "--dimensions", "election_year", "state_code", "office",
            ]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(list((output / "bronze").rglob("*.csv")))
            self.assertTrue((output / "silver/election_results/election-results-normalized.csv").is_file())
            self.assertTrue((output / "gold/election_results/aggregates.csv").is_file())


if __name__ == "__main__":
    unittest.main()
