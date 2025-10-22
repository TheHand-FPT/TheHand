import os
import random

NOISE_CHARS = "#@$%_-+=:./|~^aeiou[]"


def asset_path(category: str, filename: str) -> str:
    return os.path.join("./data", category, filename)


def print_inline(text: str) -> None:
    print(f"\r{' ' * 80}\r{text[-80:].ljust(80)}", end="", flush=True)


def generate_noise_string(length: int = 15) -> str:
    random_chars = random.choices(NOISE_CHARS, k=length)

    noise = "".join(random_chars)

    return noise
