import hashlib
import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import management  # noqa: E402


def make_password_hash(password: str, iterations: int = 260_000) -> str:
    salt = bytes.fromhex("00112233445566778899aabbccddeeff")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest}"


class AdminPasswordTests(unittest.TestCase):
    def test_accepts_correct_password(self):
        encoded = make_password_hash("correct horse battery staple")
        self.assertTrue(management.verificar_password("correct horse battery staple", encoded))

    def test_rejects_incorrect_password(self):
        encoded = make_password_hash("correct horse battery staple")
        self.assertFalse(management.verificar_password("incorrect password", encoded))

    def test_rejects_unsupported_algorithm(self):
        self.assertFalse(management.verificar_password("password", "sha1$260000$00$00"))

    def test_rejects_insufficient_iterations(self):
        encoded = make_password_hash("password", iterations=1000)
        self.assertFalse(management.verificar_password("password", encoded))

    def test_rejects_excessive_iterations(self):
        encoded = make_password_hash("password", iterations=2_000_001)
        self.assertFalse(management.verificar_password("password", encoded))

    def test_rejects_malformed_hash(self):
        self.assertFalse(management.verificar_password("password", "not-a-valid-hash"))

    def test_rejects_invalid_salt_or_digest(self):
        self.assertFalse(management.verificar_password("password", "pbkdf2_sha256$260000$invalid$invalid"))


if __name__ == "__main__":
    unittest.main()
