import hashlib
from ecdsa import SigningKey, SECP256k1

# 1. Generate private key
seed = hashlib.sha256(b"Bitcoin").hexdigest()
sk = SigningKey.from_string(bytes.fromhex(seed), curve=SECP256k1)
vk = sk.get_verifying_key()

# 2. Hash the messages
message1 = b"Edil Medeiros"
z1 = hashlib.sha256(message1).digest()
message2 = b"Neha Narula"
z2 = hashlib.sha256(message2).digest()
test_message = b"I broke ECDSA again!"
z_test = hashlib.sha256(test_message).digest()

# Generate nonce
nonce = hashlib.sha256(b"Duplicated nonce").digest()
nonce = int.from_bytes(nonce, "big")

# 3. Sign with ECDSA (returns DER-encoded by default, so we parse r,s)
r1, s1 = sk.sign_digest(z1, sigencode=lambda r, s, order: (r, s), k=nonce)
r2, s2 = sk.sign_digest(z2, sigencode=lambda r, s, order: (r, s), k=nonce)
# We don't reuse the nonce for the new signature.
r_test, s_test = sk.sign_digest(z_test, sigencode=lambda r, s, order: (r, s))

# 4. Format outputs
pubkey_compressed = vk.to_string("compressed")
r1_hex = r1.to_bytes(32, "big").hex()
s1_hex = s1.to_bytes(32, "big").hex()
signature1_hex = r1_hex + s1_hex
r2_hex = r2.to_bytes(32, "big").hex()
s2_hex = s2.to_bytes(32, "big").hex()
signature2_hex = r2_hex + s2_hex
r_test_hex = r_test.to_bytes(32, "big").hex()
s_test_hex = s_test.to_bytes(32, "big").hex()
signature_test_hex = r_test_hex + s_test_hex

# 5. Save to file
with open("solutions/exercise03.txt", "w") as f:
    f.write(signature_test_hex + "\n")

print("Public key (compressed):", pubkey_compressed.hex())
print("Private key:", sk.to_string().hex())
print("Signature1 (r||s):", signature1_hex)
print("Signature2 (r||s):", signature2_hex)
print()
print("Signature test (r||s): ", signature_test_hex)
