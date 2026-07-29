import os
import tempfile
import unittest

import guitarpro

from dadagp import parse_decode_metadata, resolve_bass_offset, resolve_initial_tempo


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


class DecodeTempoTest(unittest.TestCase):
    def test_exact_bpm_metadata_overrides_rounded_legacy_tempo(self):
        self.assertEqual(resolve_initial_tempo("97", 100), 97)

    def test_missing_or_invalid_bpm_preserves_legacy_tempo(self):
        self.assertEqual(resolve_initial_tempo(None, 100), 100)
        self.assertEqual(resolve_initial_tempo("not-a-number", 100), 100)
        self.assertEqual(resolve_initial_tempo("0", 100), 100)

    def test_out_of_range_or_oversized_bpm_preserves_legacy_tempo(self):
        self.assertEqual(resolve_initial_tempo(str(1 << 31), 100), 100)
        self.assertEqual(resolve_initial_tempo("-1", 100), 100)
        self.assertEqual(resolve_initial_tempo("9" * 5000, 100), 100)

    def test_out_of_range_bpm_fallback_serializes_as_gp5(self):
        song = guitarpro.parse("examples/progmetal.gp3")
        song.tempo = resolve_initial_tempo(str(1 << 31), 100)

        with tempfile.TemporaryDirectory() as output_dir:
            output_path = os.path.join(output_dir, "fallback-tempo.gp5")
            guitarpro.write(song, output_path, version=(5, 1, 0))

            self.assertEqual(guitarpro.parse(output_path).tempo, 100)


class DecodeBassOffsetTest(unittest.TestCase):
    def test_valid_offsets_are_preserved(self):
        self.assertEqual(resolve_bass_offset("12"), 12)
        self.assertEqual(resolve_bass_offset("-12"), -12)

    def test_missing_or_invalid_offset_defaults_to_zero(self):
        self.assertEqual(resolve_bass_offset(None), 0)
        self.assertEqual(resolve_bass_offset("not-a-number"), 0)
        self.assertEqual(resolve_bass_offset(""), 0)
        self.assertEqual(resolve_bass_offset("128"), 0)
        self.assertEqual(resolve_bass_offset(str(1 << 31)), 0)
        self.assertEqual(resolve_bass_offset("9" * 5000), 0)


if __name__ == "__main__":
    unittest.main()
