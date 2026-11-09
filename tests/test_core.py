import subprocess
import sys
import unittest

from rapi_transkrip import clean_transcript


class CleanTranscriptTests(unittest.TestCase):
    def test_removes_only_standalone_common_fillers(self):
        source = "Eee saya em ingin anu bertanya kepada teman."
        cleaned, counts = clean_transcript(source)
        self.assertEqual(cleaned, "saya ingin bertanya kepada teman.")
        self.assertEqual(counts, {"anu": 1, "em": 1, "eee": 1})

    def test_keeps_meaningful_interjections_and_words_containing_filler_letters(self):
        source = "Eh, hmm, teman saya sedang membaca."
        cleaned, counts = clean_transcript(source)
        self.assertEqual(cleaned, source)
        self.assertEqual(counts, {})

    def test_tidies_orphaned_punctuation_and_spacing(self):
        source = "Eee,  saya, anu, mau bertanya ."
        cleaned, counts = clean_transcript(source)
        self.assertEqual(cleaned, "saya, mau bertanya.")
        self.assertEqual(counts, {"anu": 1, "eee": 1})

    def test_preserves_newlines_and_trims_horizontal_whitespace(self):
        source = "  Eee, baris pertama.  \n\n  Baris kedua em.  "
        cleaned, counts = clean_transcript(source)
        self.assertEqual(cleaned, "baris pertama.\n\nBaris kedua.")
        self.assertEqual(counts, {"eee": 1, "em": 1})

    def test_cli_pipes_clean_text_and_reports_counts_only_to_stderr(self):
        process = subprocess.run(
            [sys.executable, "-m", "rapi_transkrip", "--stats"],
            input="Anu, saya eee siap.",
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(process.stdout, "saya siap.\n")
        self.assertIn("menghapus 2 kata jeda", process.stderr)
        self.assertNotIn("saya eee siap", process.stderr)

    def test_empty_text_stays_empty(self):
        self.assertEqual(clean_transcript(""), ("", {}))


if __name__ == "__main__":
    unittest.main()
