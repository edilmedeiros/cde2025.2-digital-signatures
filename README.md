# Signing without pen and paper

Digital signatures are the backbone of cryptocurrency security.
They serve as the primary form of authorization in blockchain systems, proving ownership of coins or accounts and providing cryptographic attestation that the rightful owner is indeed authorizing a payment or transaction.
Without robust digital signatures, cryptocurrencies would lack the fundamental security property that prevents unauthorized spending—anyone could claim to own anyone else's coins.
Every Bitcoin transaction, Ethereum smart contract interaction, and blockchain operation ultimately depends on the mathematical certainty that digital signatures provide.

However, many things can go wrong when implementing and using digital signatures in practice.
Small implementation mistakes can have catastrophic consequences: reusing random numbers can expose private keys, poor randomness generation can make signatures predictable, and subtle mathematical properties can be exploited to forge signatures or manipulate transactions.
This assignment explores these failure modes through hands-on exploitation, teaching you to think like both an implementer and an attacker.

The assignment emphasizes algorithmic exploitation over brute force attacks.
You will discover how mathematical relationships in signature schemes can be exploited when implementers make subtle mistakes, particularly around nonce generation and signature verification.
This approach teaches both the correct implementation and the security mindset needed to avoid common pitfalls.

### Expected submissions

Your solutions should be in the form of text files in the `submissions` folder of your repo, containing the requested signatures, keys, and messages in hex format.
The autograder will run the scripts in the `graders` folder to verify your answers.
You can use them to check your answers, but DO NOT MODIFY THE GRADER SCRIPTS.

**All cryptographic operations must use the secp256k1 elliptic curve and the sha156 hash function**.
This is the same curve used by Bitcoin and Ethereum, making your implementations directly relevant to real cryptocurrency systems.

You can use any programming language you prefer - the graders only check the final results you provide in text files.
Please commit your source code to the implementation folder so instructors can provide feedback on your approach.
The autograder is triggered when you push changes to the `main` branch.
Check its output on the `Actions` tab in the GitHub interface.

TODO: add suggestions of elliptic curve arithmetic libraries.

---

## ECDSA: The workhorse standard

### Exercise 1: Basic ECDSA signing

Implement ECDSA signature generation using the secp256k1 curve.
Sign the message "Hello Bitcoin!" using any private key of your choice.

*Expected output*: a text file `submissions/exercise01.txt` with three lines:

Line 1: Your public key (66 hex characters, compressed format)
Line 2: Your signature (128 hex characters, `r||s` format)

The notation `r||s` means `r` concatenated with `s`, no spaces in between the bytes.

This exercise gets you familiar with ECDSA basics.
The autograder will verify that your signature is mathematically valid for the given message and keys.


### Exercise 2: ECDSA nonce reuse attack

You are given two ECDSA signatures that were created using the same nonce `k` (a critical vulnerability).
Use them to recover the private key of the signer, then sign the message "I broke ECDSA!" to prove you have the key.

Given signatures:
```
Message 1: "Edil Medeiros"
signature: `4264b8b1ef4c77bf259a8d144689a0e6ea1aa6daf3761eb28b8b8669cf72f73907d78eea283d3841716efdd6eae4f559bc670f2674d0e4ffb66774c4796f71e6`

Message 2: "Neha Narula"
signature: `4264b8b1ef4c77bf259a8d144689a0e6ea1aa6daf3761eb28b8b8669cf72f73905a3eb1483b5498908be8c05c40da3e5a4d5d5cdfb1dc1f8adaca890a67605b0`

Public key: `03133a3a03b4f9a731d4404338a278a0b73b1e20fa74fbeff2ec378ebdc4339cec`
```

*Expected output*: a text file `submissions/exercise02.txt` with a signature (`r||s` format) for the message "I broke ECDSA!" (128 hex characters) in a single line.
The signature will be validated using the same public key as shown above.
Your signature is not required to reuse the nonce.

*Mathematical hint*: When two signatures share the same `r` value (indicating nonce reuse), you can recover the private key using modular arithmetic.
The relationship `k = (hash(m1) - hash(m2))/(s1 - s2) mod n` allows you to find the nonce, then extract the private key.
Note that `n` is the secp256k1 group order:

n = `FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141`

Do not try to naively brute force the signature, we are using real cryptographic schemes here (although in an insecure manner).
This attack has occurred in real systems - notably the Sony PlayStation 3 and various Bitcoin wallets with poor random number generation.

*Question for discussion*: how do we know that you successfully recovered the right key by seeing only a valid signature you forged?

*Bonus*: if you want to have a little more fun, let me tell that this private key was created by hashing (sha256) a 7 ascii-character string.
Can you find which string was that?
This is a technique many people used in the past to generate Bitcoin private keys.
They all probably have lost their funds by now.


### Exercise 3: ECDSA known nonce attack

You intercepted an ECDSA signature along with the nonce that was used to create it (another implementation vulnerability).
This is a real threat in cryptocurrencies since digital signatures are publicly revealed when spending money and we can track when that money was received in the first place, providing an estimate for when a private key was generated.
This information can be used to guess the private key if the wallet implementation used a weak random number generator (which happens even today).
Use this information to recover the private key.

```
Message: "Satoshi Nakamoto"
Signature (`r||s`): 133c76589b4cce6898e63a366e40d43a6471db814f5a354d52c4abcd067942780cc9b3d891c9a4eb8bcce6edc20f31937005595a7f7ea6a4bf20c3f6367f5155
Nonce k: 0x718768e4b0ec256839ddcba80b7902a361d525f4be8c4904c275edd35625afb5
Public key: 034be5c17ff958423a95313317aaf9997607ea64af9edfd90933d1466866794550
```

*Expected output*: a text file `submissions/exercise03.txt` with a signature for the message "I broke ECDSA again!" (128 hex characters) in a single line.

TODO: CHECK ALL FORMULAS...

*Mathematical hint*: With a known nonce `k`, the private key can be directly calculated from the signature equation: `d = (k·s - hash(m))/r mod n`.
This vulnerability occurs when developers use weak random number generators, hardcoded nonces for "testing," or when side-channel attacks reveal nonce information.


### Exercise 4: ECDSA signature malleability

Given a valid ECDSA signature, create a different but equally valid signature for the same message and public key by exploiting signature malleability.

Given:
```
Message: "transfer 100 BTC"
Valid signature: f474d12468415184847778e455189eb0a07df7696d69777008f59fe9ebe497727739e65b40f2a1587b47e953d6fdec9934e82c45c00fe41d446347f35b74708f
Public key: 020e7d4f8640ec6f3382a1dd61b4b292f815864dc7b6c12ba2744597aa3504d674
```

*Expected output*: a text file `submissions/exercise04.txt` with your malleated signature (128 hex characters, r||s format).

*Hint*: For any valid ECDSA signature `(r, s)`, the signature `(r, n-s)` is also mathematically valid, where `n` is the curve group order.

This property was exploited to manipulate Bitcoin transaction IDs before the SegWit upgrade.
Understanding malleability is crucial for secure protocol design, as it can enable double-spending attacks and break smart contract assumptions.

*Questions for discussion*: can someone use this vulnerability to forge a signature, i.e. to spend your money on your behalf? Can someone use this vulnerability to steal something from you?

Note that theses questions have different semantics: the former asks about the security of the protocol, the later asks about the security of how people use the protocol for payments in the real world.

---

## Schnorr: a bag full of tricks

Schnorr signatures were patented until 2010, that's why they were not widely implemented at the time the first cryptocurrencies were designed and deployed.
Yet, there's a trend to design cryptocurrencies based on this kind of digital signature since it allows for many tricks, like signature aggregation and scriptless scripts, that improve privacy and scalability of cryptocurrencies.


### Exercise 5: Basic Schnorr signatures

Implement Schnorr signature generation using the secp256k1 curve.
Sign the message "Schnorr is better" using any private key.

*Expected output*: A text file `submissions/exercise05.txt` with two lines:

Line 1: Your public key (66 hex characters, compressed format)
Line 2: Your Schnorr signature (128 hex characters, r||s format)

*Note*: Schnorr signatures use a different algorithm than ECDSA.
The signature equation is `s = k + e·d mod n`, where `e` is the hash challenge. 
Unlike ECDSA, Schnorr signatures are not malleable and have linear properties that enable aggregation.
You can use the secp256k1lab library or implement the algorithm yourself.
The autograder will verify mathematical correctness.


### Exercise 6: Schnorr signature aggregation

Given two Schnorr signatures from different private keys on the same message, create a valid signature for the aggregate public key P = P₁ + P₂.
Given:

Message: "aggregate this"
Signature A: (R₁, s₁) from private key d₁
Signature B: (R₂, s₂) from private key d₂
Public key A: P₁ = d₁·G
Public key B: P₂ = d₂·G
[All values provided in exercise]

*Expected output*: A text file `submissions/exercise06.txt` with a valid signature for aggregate key (128 hex characters), in a single line.

*Mathematical insight*: This exploits Schnorr's linear properties.
While naive addition of signatures doesn't work securely, this exercise demonstrates the mathematical foundation that enables advanced protocols like MuSig.
This linearity is what makes Schnorr attractive for blockchain applications, enabling signature aggregation that improves both privacy and scalability.

