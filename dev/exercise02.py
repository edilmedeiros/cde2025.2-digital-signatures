import hashlib
from ecdsa import SigningKey, SECP256k1

# 1. Generate private key
seed = hashlib.sha256(b"BITCOIN").hexdigest()
sk = SigningKey.from_string(bytes.fromhex(seed), curve=SECP256k1)
vk = sk.get_verifying_key()

# 2. Hash the message
message = b"Satoshi Nakamoto"
z = hashlib.sha256(message).digest()
message_test = b"I broke ECDSA!"
z_test = hashlib.sha256(message_test).digest()

# Generate nonce
nonce = hashlib.sha256(b"Weak nonce").digest()
nonce = int.from_bytes(nonce, "big")

# 3. Sign with ECDSA (returns DER-encoded by default, so we parse r,s)
r, s = sk.sign_digest(z, sigencode=lambda r, s, order: (r, s), k=nonce)
r_test, s_test = sk.sign_digest(z_test, sigencode=lambda r, s, order: (r, s))

# 4. Format outputs
pubkey_compressed = vk.to_string("compressed")
r_hex = r.to_bytes(32, "big").hex()
s_hex = s.to_bytes(32, "big").hex()
signature_hex = r_hex + s_hex
r_test_hex = r_test.to_bytes(32, "big").hex()
s_test_hex = s_test.to_bytes(32, "big").hex()
signature_test_hex = r_test_hex + s_test_hex

# 5. Save to file
with open("solutions/exercise02.txt", "w") as f:
    f.write(signature_test_hex + "\n")

print("Public key (compressed):", pubkey_compressed.hex())
print("Private key:", sk.to_string().hex())
print("Signature (r||s):", signature_hex)
print("Nonce:", hex(nonce))
print("Test signature: ", signature_test_hex)
