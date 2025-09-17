# grader_exercise01.py
import hashlib
import sys
from ecdsa import VerifyingKey, SECP256k1


def parse_sig(signature: str, n):
    r = int(signature[:64], 16)
    s = int(signature[64:], 16)
    return (r, s)


def grade(filename="solutions/exercise01.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    pubkey_hex, sig_hex = lines

    # TODO: Check pubkey is well formed: starts with 02 or 03 and have 33 bytes
    # TODO: Check if the signature has 64 bytes.

    # Recover pubkey
    pubkey_raw = bytes.fromhex(pubkey_hex)
    try:
        vk = VerifyingKey.from_string(
            pubkey_raw, curve=SECP256k1, hashfunc=hashlib.sha256
        )
    except Exception:
        # Got an invalid pubkey
        return "FAIL"

    # verify signature
    message = b"Hello Bitcoin!"
    try:
        ok = vk.verify(
            sig_hex, data=message, hashfunc=hashlib.sha256, sigdecode=parse_sig
        )
    except Exception:
        # Signature is invalid
        return "FAIL"

    return "PASS" if ok else "FAIL"


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "solutions/exercise01.txt"
    print(grade(fname))
