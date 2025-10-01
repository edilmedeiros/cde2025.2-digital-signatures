# grader_exercise05.py
import hashlib
import sys
from ecdsa import VerifyingKey, SECP256k1


def parse_sig(signature: str, n):
    r = int(signature[:64], 16)
    s = int(signature[64:], 16)
    return (r, s)


def grade(filename="solutions/exercise05.txt"):
    # Read transaction data
    with open(filename) as f:
        tx_data = bytes.fromhex(f.read())

    # Read signature from data
    r = tx_data[47:79]
    s = tx_data[81:113]
    sig_hex = r.hex() + s.hex()

    pubkey = "0411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3"
    message = "0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd37040000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3acffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac0000000001000000"

    z = hashlib.sha256(hashlib.sha256(bytes.fromhex(message)).digest()).digest()

    vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)

    try:
        ok = vk.verify_digest(sig_hex, digest=z, sigdecode=parse_sig)
    except Exception:
        # Signature is invalid
        return "FAIL"

    return "PASS" if ok else "FAIL"


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "solutions/exercise05.txt"
    print(grade(fname))
