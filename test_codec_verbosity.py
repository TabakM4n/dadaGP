import contextlib
import io
import unittest
from types import SimpleNamespace

import guitarpro

from dadagp import (
    get_instrument_token_prefix,
    get_measure_tokens,
    get_tuning_type,
    reset_measure_state,
    tokens_to_beat_effect,
    tokens_to_note_effect,
)


class CodecVerbosityTest(unittest.TestCase):
    def test_repeat_ending_encodes_in_quiet_and_verbose_modes(self):
        song = guitarpro.parse("examples/progmetal.gp3")
        measure = next(m for m in song.tracks[0].measures if m.header.repeatAlternative)
        for verbose in (False, True):
            with self.subTest(verbose=verbose), contextlib.redirect_stdout(io.StringIO()) as output:
                reset_measure_state()
                tokens = get_measure_tokens(measure, verbose=verbose)
                self.assertIn(f"measure:repeat_alternative:{measure.header.repeatAlternative}", tokens)
                self.assertEqual(bool(output.getvalue()), verbose)
        reset_measure_state()

    def test_unsupported_tuning_keeps_domain_error_without_global_verbosity(self):
        with self.assertRaisesRegex(Exception, "Unsupported tuning"):
            get_tuning_type("guitar", ["C0"])

    def test_unrelated_beat_effect_token_is_ignored_without_global_verbosity(self):
        effect = guitarpro.BeatEffect()
        tokens_to_beat_effect(effect, ["unexpected:token"])
        self.assertFalse(effect.fadeIn)

    def test_unrelated_note_effect_token_is_ignored_without_global_verbosity(self):
        note = SimpleNamespace(effect=guitarpro.NoteEffect())
        tokens_to_note_effect(note, ["unexpected:token"])
        self.assertIsNone(note.effect.tremoloPicking)

    def test_tremolo_picking_decodes_without_global_verbosity(self):
        note = SimpleNamespace(effect=guitarpro.NoteEffect())
        tokens_to_note_effect(note, ["nfx:tremolo_picking:duration240"])
        self.assertEqual(note.effect.tremoloPicking.duration.time, 240)

    def test_unknown_track_keeps_domain_assertion_without_global_verbosity(self):
        groups = {key: [] for key in ("drums", "bass", "distorted", "clean", "leads", "pads", "remove")}
        with self.assertRaisesRegex(AssertionError, "doesn't belong to a group"):
            get_instrument_token_prefix(object(), groups)


if __name__ == "__main__":
    unittest.main()
