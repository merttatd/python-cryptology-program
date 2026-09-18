import unittest
from crypto_methods import ALPHABET, transform


class CryptoTests(unittest.TestCase):
    def test_round_trips(self):
        for method, key in [("caesar", "-63"), ("vigenere", "GÜNEŞ"), ("atbash", ""), ("rail", "3"), ("rail", "100"), ("base64", "")]:
            for text in ["", "a", ALPHABET, "İstanbul, ışık!\n🙂 123 <b> & qwx"]:
                with self.subTest(method=method, text=text):
                    encrypted = transform(text, method, key)
                    self.assertEqual(transform(encrypted, method, key, True), text)

    def test_known_results(self):
        self.assertEqual(transform("abcç zZ!", "caesar", "1"), "bcçd Aa!")
        self.assertEqual(transform("abc ABC!", "vigenere", "b"), "bcç BCÇ!")
        self.assertEqual(transform("aAzZ", "atbash"), "zZaA")
        self.assertEqual(transform("WEAREDISCOVEREDFLEEATONCE", "rail", "3"), "WECRLTEERDSOEEFEAOCAIVDEN")
        self.assertEqual(transform("hello", "base64"), "aGVsbG8=")
        self.assertEqual(transform("abc", "sha256"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_invalid_inputs(self):
        for method, key in [("caesar", ""), ("caesar", "2.5"), ("vigenere", ""), ("vigenere", "abc1"), ("rail", "1"), ("rail", "101"), ("rail", "x"), ("unknown", "")]:
            with self.subTest(method=method, key=key), self.assertRaises(ValueError):
                transform("test", method, key)
        for text in ["!!!", "a", "/w==", "şifre"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                transform(text, "base64", decrypt=True)
        with self.assertRaises(ValueError):
            transform("abc", "sha256", decrypt=True)


if __name__ == "__main__":
    unittest.main()
