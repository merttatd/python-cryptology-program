"""Educational ciphers and encoding/hash utilities."""
import base64
import binascii
import hashlib

LOWER = "abcçdefgğhıijklmnoöprsştuüvyz"
UPPER = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
ALPHABET = LOWER + UPPER


def transform(text, method, key="", decrypt=False):
    if method == "caesar":
        try:
            shift = int(key) * (-1 if decrypt else 1)
        except ValueError:
            raise ValueError("Sezar için tam sayı bir anahtar girin.") from None
        return "".join(ALPHABET[(ALPHABET.index(c) + shift) % len(ALPHABET)]
                       if c in ALPHABET else c for c in text)
    if method == "vigenere":
        if not key or any(c not in ALPHABET for c in key):
            raise ValueError("Anahtar yalnızca Türkçe alfabenin harflerinden oluşmalıdır.")
        shifts = [ALPHABET.index(c) % len(LOWER) for c in key]
        result, position = [], 0
        for c in text:
            chars = LOWER if c in LOWER else UPPER if c in UPPER else None
            if chars:
                shift = shifts[position % len(shifts)] * (-1 if decrypt else 1)
                result.append(chars[(chars.index(c) + shift) % len(chars)])
                position += 1
            else:
                result.append(c)
        return "".join(result)
    if method == "atbash":
        return text.translate(str.maketrans(LOWER + UPPER, LOWER[::-1] + UPPER[::-1]))
    if method == "rail":
        try:
            rails = int(key)
        except ValueError:
            raise ValueError("Ray sayısı 2–100 arasında bir tam sayı olmalıdır.") from None
        if not 2 <= rails <= 100:
            raise ValueError("Ray sayısı 2–100 arasında olmalıdır.")
        cycle = 2 * (rails - 1)
        rows = [[] for _ in range(rails)]
        for i in range(len(text)):
            rows[min(i % cycle, cycle - i % cycle)].append(i)
        order = [i for row in rows for i in row]
        if not decrypt:
            return "".join(text[i] for i in order)
        result = [""] * len(text)
        for char, i in zip(text, order):
            result[i] = char
        return "".join(result)
    if method == "base64":
        if not decrypt:
            return base64.b64encode(text.encode("utf-8")).decode("ascii")
        try:
            return base64.b64decode("".join(text.split()), validate=True).decode("utf-8")
        except (ValueError, binascii.Error, UnicodeError):
            raise ValueError("Geçerli UTF-8 metin içeren bir Base64 değeri girin.") from None
    if method == "sha256":
        if decrypt:
            raise ValueError("SHA-256 tek yönlüdür; geri çözülemez.")
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    raise ValueError("Bilinmeyen yöntem.")
