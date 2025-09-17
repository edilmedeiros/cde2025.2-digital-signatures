# grader_exercise03.py
import hashlib
import sys
from ecdsa import VerifyingKey, SECP256k1


def parse_sig(signature: str, n):
    r = int(signature[:64], 16)
    s = int(signature[64:], 16)
    return (r, s)


def grade(filename="solutions/exercise03.txt"):
    with open(filename) as f:
        sig_hex = f.read().strip()

    # TODO: Check pubkey is well formed: starts with 02 or 33 and have 33 bytes
    # TODO: Check if the signature has 64 bytes.

    # Recover pubkey
    pubkey_hex = "03133a3a03b4f9a731d4404338a278a0b73b1e20fa74fbeff2ec378ebdc4339cec"
    pubkey_raw = bytes.fromhex(pubkey_hex)
    vk = VerifyingKey.from_string(pubkey_raw, curve=SECP256k1, hashfunc=hashlib.sha256)

    # verify signature
    message = b"I broke ECDSA again!"
    try:
        ok = vk.verify(
            sig_hex, data=message, hashfunc=hashlib.sha256, sigdecode=parse_sig
        )
    except Exception:
        # Signature is invalid
        return "FAIL"

    return "PASS" if ok else "FAIL"


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "solutions/exercise03.txt"
    print(grade(fname))
