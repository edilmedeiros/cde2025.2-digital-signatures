# Signing without pen and paper

Digital signatures are the backbone of cryptocurrency security.
They serve as the primary form of authorization in blockchain systems, proving ownership of coins or accounts and providing cryptographic attestation that the rightful owner is indeed authorizing a payment or transaction.
When combined with cryptographic hash functions, digital signatures also provide data integrity guarantees.
Without robust digital signatures, cryptocurrencies would lack the fundamental security property that prevents unauthorized spending—anyone could claim to own anyone else's coins.
Every Bitcoin transaction, Ethereum smart contract interaction, and blockchain operation ultimately depends on the mathematical certainty that digital signatures provide.

However, many things can go wrong when implementing and using digital signatures in practice.
Small implementation mistakes can have catastrophic consequences: reusing random numbers can expose private keys, poor randomness generation can make signatures predictable, and subtle mathematical properties can be exploited to forge signatures or manipulate transactions.
This assignment explores these failure modes through hands-on exploitation, teaching you to think like both an implementer and an attacker.

This assignment emphasizes algorithmic exploitation over brute force attacks.
You will discover how mathematical relationships in signature schemes can be exploited when implementers make subtle mistakes, particularly around nonce generation and signature verification.
This approach teaches both the correct implementation and the security mindset needed to avoid common pitfalls.

Do not try to naively brute force the signatures, we are using real cryptographic schemes here (although in an insecure manner).

### Expected submissions

Your solutions should be in the form of text files in the `solutions` folder of your repo, containing the requested signatures, keys, and messages in hex format.
The autograder will run the scripts in the `graders` folder to verify your answers.
You can use them to check your answers, but DO NOT MODIFY THE GRADER SCRIPTS.

**All cryptographic operations must use the secp256k1 elliptic curve and the sha256 hash function**.
This is the same curve used by Bitcoin and Ethereum, making your implementations directly relevant to real cryptocurrency systems.

You can use any programming language you prefer, the graders will check only the final results you provide in text files.
You don't need to implement the cryptographic primitives yourself (although doing so is a fantastic learning experience if you are interested in cryptography).
Here is a list of libraries you can use to solve these exercises:

- Python: `ecdsa`
- C: `libsecp256k1`, `openssl`
- Rust: `rust-secp256k1`, `k256`
- Go: `btcsuite/btcec`

You'll need a big integer implementation to do signature calculations:

- Python: builtin `int` type
- C/C++: `openssl bignum`, `gnu gmp`, `libsecp256k1` scalar type
- Rust: `num-bigint`, `ibig`
- Go: builtin `math/big.Int`

Please commit your source code to the `implementation` folder so instructors can provide feedback on your approach.
The autograder is triggered when you push changes to the `main` branch.
Check its output on the `Actions` tab in the GitHub interface.

---

### Exercise 1: Basic ECDSA signing

Implement ECDSA signature generation using the secp256k1 curve.
Sign the message "Hello Bitcoin!" using any private key of your choice.

*Expected output*: a text file `solutions/exercise01.txt` with three lines:

- Line 1: Your public key (66 hex characters, compressed format)
- Line 2: Your signature (128 hex characters, `r||s` format)

The notation `r||s` means `r` concatenated with `s`, no spaces in between the bytes.

This exercise gets you familiar with ECDSA basics.
The autograder will verify that your signature is mathematically valid for the given message and keys.

*Question for discussion*: how did you generated your private key? How easy (or difficult) it is for someone else guess your private key?

---

### Exercise 2: ECDSA known nonce attack

You intercepted an ECDSA signature along with the nonce that was used to create it.
This is a real threat in cryptocurrencies since digital signatures are publicly revealed when spending money and we can track when that money was spent, providing an estimate for when a nonce was generated.
This information can be used to compute the private key if the wallet implementation used a weak random number generator (which happens even today).
Use this information to recover my private key.

```
Message: "Satoshi Nakamoto"
Signature (`r||s`): 133c76589b4cce6898e63a366e40d43a6471db814f5a354d52c4abcd067942780cc9b3d891c9a4eb8bcce6edc20f31937005595a7f7ea6a4bf20c3f6367f5155
Nonce k: 718768e4b0ec256839ddcba80b7902a361d525f4be8c4904c275edd35625afb5
Public key: 034be5c17ff958423a95313317aaf9997607ea64af9edfd90933d1466866794550
```

*Expected output*: a text file `solutions/exercise02.txt` with a signature for the message "I broke ECDSA!" (128 hex characters) in a single line.
The signature will be validated using the same public key as shown above.
Your signature is not required to reuse the nonce.

*Mathematical hint*: With a known nonce `k`, the private key `e` can be directly calculated from the signature equation: `s = k^(-1) * (hash(m) + r*e) mod n`.
Note that these operations should be calculated modulo `n`, the order of the secp256k1 group:

n = `FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141`

This vulnerability occurs when developers use weak random number generators, hardcoded nonces for "testing", or when side-channel attacks reveal nonce information.

*Question for discussion*: how do we know that you successfully recovered the right key by seeing only a valid signature you forged?

---

### Exercise 3: ECDSA nonce reuse attack

You are given two ECDSA signatures that were created using the same nonce `k` (another critical vulnerability).
Use them to recover the private key of the signer, then sign the message "I broke ECDSA again!" to prove you recovered my private key.

Given signatures:
```
Message 1: "Edil Medeiros"
signature: `4264b8b1ef4c77bf259a8d144689a0e6ea1aa6daf3761eb28b8b8669cf72f73907d78eea283d3841716efdd6eae4f559bc670f2674d0e4ffb66774c4796f71e6`

Message 2: "Neha Narula"
signature: `4264b8b1ef4c77bf259a8d144689a0e6ea1aa6daf3761eb28b8b8669cf72f73905a3eb1483b5498908be8c05c40da3e5a4d5d5cdfb1dc1f8adaca890a67605b0`

My public key: `03133a3a03b4f9a731d4404338a278a0b73b1e20fa74fbeff2ec378ebdc4339cec`
```

*Expected output*: a text file `solutions/exercise03.txt` with a signature (`r||s` format) for the message "I broke ECDSA!" (128 hex characters) in a single line.
The signature will be validated using the same public key as shown above.
Your signature is not required to reuse the nonce.

*Mathematical hint*: When two signatures share the same `r` value (indicating nonce reuse), you can recover the nonce using modular arithmetic.
The relationship `k = (hash(m1) - hash(m2))/(s1 - s2) mod n` allows you to find the nonce, then extract the private key.

This attack has occurred in real systems - notably the Sony PlayStation 3 and various Bitcoin wallets with poor nonce generation.

*Question for discussion*: how could you know those signatures reused the nonce if I didn't told you so?

*Bonus*: if you want to have a little more fun, let me tell that this private key was created by hashing (`sha256`) a 7 ascii-character string.
Can you find which string was that?
We call this a low entropy key.
This is an insecure key generation technique that many people used in the past (and still use) to generate private keys.
They all probably have lost their funds by now.

---

### Exercise 4: ECDSA signature malleability

Given a valid ECDSA signature, create a different but equally valid signature for the same message and public key by exploiting signature malleability.

Given:
```
Message: "transfer 100 BTC"
Valid signature: f474d12468415184847778e455189eb0a07df7696d69777008f59fe9ebe497727739e65b40f2a1587b47e953d6fdec9934e82c45c00fe41d446347f35b74708f
Public key: 020e7d4f8640ec6f3382a1dd61b4b292f815864dc7b6c12ba2744597aa3504d674
```

*Expected output*: a text file `solutions/exercise04.txt` with your malleated signature (128 hex characters, r||s format).

*Hint*: For any valid ECDSA signature `(r, s)`, the signature `(r, n-s)` is also mathematically valid, where `n` is the curve group order.

This property was exploited to manipulate Bitcoin transaction IDs before the SegWit upgrade.
Understanding malleability is crucial for secure protocol design, as it can enable double-spending attacks and break smart contract assumptions.

*Questions for discussion*: can someone use this vulnerability to spend your money on your behalf?
Can someone use this vulnerability to steal something from you?

Note that theses questions have different semantics: the former asks about the security of the protocol, the later asks about how people use the protocol for payments in the real world.

---

### Exercise 5: malleability in context

Bitcoin transactions usually include a digital signature for every coin being spent.
Let's consider the first Bitcoin transaction in which Satoshi Nakamoto paid 10 BTC to Hal Finney.
You can see a rendered version of this transaction in a [block explorer](https://mempool.space/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16).

You will find the raw transaction data in the file `data/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16.dat` in your repo.
From this data:

1. extract the signature `r` and `s` values.
2. produce a new valid signature for this transaction (see exercise 4).
3. substitute the original signature with your malleated version.

*Expected output*: a text file `solutions/exercise05.txt` with the raw data of the malleated transaction.

*Hint*: signatures in Bitcoin are encoded in the DER format.

The grader will check if your new transaction signature validates against the old transaction data.
That is, we took a valid transaction and constructed a different valid transaction with the same semantics.

*Questions for discussion*: transaction malleability is not a problem for confirmed transactions.
Yet, why are they a real concern in cryptocurrency systems?
What counter measures can we take to completely avoid transaction malleability?

*Bonus*: the grader of this exercise will check your signature against this public key (uncompressed form): `0411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3`.
Can you explain where this key comes from?

*Bonus 2*: the grader of this exercise will check your signature against this message:
```
0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd37040000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3acffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac0000000001000000
```
Can you explain how this message was built?

