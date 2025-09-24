# grader_exercise04.py
import hashlib
import sys
from ecdsa import VerifyingKey, SECP256k1, ellipticcurve

def parse_sig(signature: str, n):
    r = int(signature[:64], 16)
    s = int(signature[64:], 16)
    return (r,s)

def grade(filename="solutions/exercise04.txt"):
    with open(filename) as f:
        sig_hex = f.read().strip()

    # TODO: Check pubkey is well formed: starts with 02 or 03 and have 33 bytes
    # TODO: Check if the signature has 64 bytes.

    # Recover pubkey
    pubkey_hex = '020e7d4f8640ec6f3382a1dd61b4b292f815864dc7b6c12ba2744597aa3504d674'
    pubkey_raw = bytes.fromhex(pubkey_hex)
    vk = VerifyingKey.from_string(pubkey_raw, curve=SECP256k1, hashfunc=hashlib.sha256)

    # verify signature
    message = b"transfer 100 BTC"
    try: 
        ok = vk.verify(sig_hex,
                       data=message, 
                       hashfunc=hashlib.sha256,
                       sigdecode=parse_sig)
    except Exception as e:
        # Signature is invalid
        return "FAIL"

    return "PASS" if ok else "FAIL"

if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "solutions/exercise04.txt"
    print(grade(fname))
