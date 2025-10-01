import hashlib
from ecdsa import VerifyingKey, SECP256k1


def parse_sig(signature: str, n):
    r = int(signature[:64], 16)
    s = int(signature[64:], 16)
    return (r, s)


# Read transaction data
with open(
    "data/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16.dat"
) as f:
    tx_data = bytes.fromhex(f.read())

print("Transaction raw data: ", tx_data.hex())

txid = hashlib.sha256(hashlib.sha256(tx_data).digest()).digest()
print("txid: ", txid.hex())
txid = hex(int.from_bytes(txid, "little"))
print("txid: ", txid[2:])

# Read signature from data
r = tx_data[47:79]
s = tx_data[81:113]
print("r: ", r.hex())
print("s: ", s.hex())

sig_hex = r.hex() + s.hex()
print("sig: ", sig_hex)

pubkey = "0411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3"
scriptPubKey = "410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac"

message = "0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd37040000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3acffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac0000000001000000"
z = hashlib.sha256(hashlib.sha256(bytes.fromhex(message)).digest()).digest()

print("digest: ", z.hex())

vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
print(vk.to_string().hex())

try:
    ok = vk.verify_digest(sig_hex, digest=z, sigdecode=parse_sig)
except Exception:
    # Signature is invalid
    print("FAIL")

print("PASS")

print(s)
print(type(s))
# Malleate signature
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
new_s = (n - int.from_bytes(s, "big")) % n
print(hex(new_s)[2:])
new_s_hex = new_s.to_bytes(32, "big").hex()
new_signature_hex = r.hex() + new_s_hex

try:
    ok = vk.verify_digest(new_signature_hex, digest=z, sigdecode=parse_sig)
except Exception:
    # Signature is invalid
    print("FAIL")

print("PASS")

# Create solution
new_tx = tx_data[:81].hex() + hex(new_s)[2:] + tx_data[113:].hex()
print(new_tx)

# 5. Save to file
with open("solutions/exercise05.txt", "w") as f:
    f.write(new_tx + "\n")
