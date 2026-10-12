import unittest

from token_splitter import split_wait_token, wait_token_list2


class WaitTokenTest(unittest.TestCase):
    def test_long_waits_keep_duration_inside_supported_vocabulary(self):
        for duration in (16385, 32768, 524288, 524289):
            with self.subTest(duration=duration):
                tokens = split_wait_token(f"wait:{duration}")
                self.assertTrue(tokens)
                self.assertTrue(set(tokens).issubset(wait_token_list2))
                self.assertEqual(
                    sum(int(token.split(":", 1)[1]) for token in tokens),
                    duration,
                )

    def test_long_wait_boundary_split(self):
        self.assertEqual(split_wait_token("wait:32768"), ["wait:16384"] * 2)
        self.assertEqual(
            split_wait_token("wait:524289"),
            ["wait:16384"] * 32 + ["wait:1"],
        )


if __name__ == "__main__":
    unittest.main()
