import csv
import getpass
import hashlib
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ADMIN_FILE = DATA_DIR / "admins.csv"
ITERATIONS = 260_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def main() -> None:
    if ADMIN_FILE.exists():
        print("O ficheiro data/admins.csv já existe. Não foi alterado.")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    admins = []
    print("Configuração local de administradores. Usa uma palavra-passe única com pelo menos 12 caracteres.")

    while True:
        username = input("Nome de utilizador: ").strip()
        if not username or any(item["username"] == username for item in admins):
            print("Nome vazio ou repetido. Escolhe outro.")
            continue

        password = getpass.getpass("Palavra-passe: ")
        if len(password) < 12:
            print("A palavra-passe deve ter pelo menos 12 caracteres.")
            continue
        confirmation = getpass.getpass("Confirmar palavra-passe: ")
        if password != confirmation:
            print("As palavras-passe não coincidem.")
            continue

        admins.append({
            "admin_id": str(len(admins) + 1),
            "username": username,
            "password_hash": hash_password(password),
        })

        if input("Adicionar outro administrador? [s/N]: ").strip().lower() != "s":
            break

    with ADMIN_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["admin_id", "username", "password_hash"])
        writer.writeheader()
        writer.writerows(admins)

    print(f"Ficheiro local criado: {ADMIN_FILE.relative_to(ROOT)}")
    print("Não partilhes este ficheiro nem o adiciones ao Git.")


if __name__ == "__main__":
    main()
