import unittest

from dadagp import parse_decode_metadata


class DecodeMetadataTest(unittest.TestCase):
    def test_original_format_uses_first_token_as_artist(self):
        metadata = parse_decode_metadata([
            "dadabots",
            "downtune:0",
            "tempo:120",
            "start",
        ])

        self.assertEqual(metadata["title"], "untitled")
        self.assertEqual(metadata["artist"], "dadabots")

    def test_extended_format_prefers_explicit_artist_metadata(self):
        metadata = parse_decode_metadata([
            "[TITLE:Obsidian Riff]",
            "[ARTIST:TabakMan]",
            "source_artist_token",
            "downtune:0",
            "tempo:120",
            "start",
        ])

        self.assertEqual(metadata["title"], "Obsidian Riff")
        self.assertEqual(metadata["artist"], "TabakMan")

    def test_extended_format_without_artist_falls_back_to_first_non_bracket_token(self):
        metadata = parse_decode_metadata([
            "[TITLE:Metadata Only Title]",
            "[BPM:96]",
            "source_artist_token",
            "downtune:0",
            "tempo:96",
            "start",
        ])

        self.assertEqual(metadata["title"], "Metadata Only Title")
        self.assertEqual(metadata["artist"], "source_artist_token")


if __name__ == "__main__":
    unittest.main()
