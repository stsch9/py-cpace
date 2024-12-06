# py-cpace
**WARNING:** This is just a PoC. Use at your own risk. <br />
This is a simple python implementation of CPace defined in [draft-irtf-cfrg-cpace-13](https://www.ietf.org/archive/id/draft-irtf-cfrg-cpace-13.html).

It uses [pysodium](https://github.com/stef/pysodium) for all Ristretto255 functions. Therefore libsodium must be pre-installed [libsodium](https://doc.libsodium.org/).

## Usage:
### symmetric setting
```
# User Alice:
cpaceA = CPace(PRF=b'Password', role='symmetric', ADa=b'Alice', ADb=b'Bob', CI=b'CI', sid=b'sid')
Ya, ADa = cpaceA.compute_Yx()

# User Bob:
cpaceB = CPace(PRS=b'Password', role='symmetric', ADa=b'Bob', ADb=b'Alice', CI=b'CI', sid=b'sid')
Yb, ADb = cpaceB.compute_Yx()

# User Alice:
ISK_A = cpaceA.derive_ISK(Yb)

# User Bob:
ISK_B = cpaceB.derive_ISK(Ya)
```

### initiator-responder setting
```
# User Alice:
cpaceA = CPace(PRS=b'Password', role='initiator', ADa=b'Alice', ADb=b'Bob', CI=b'CI', sid=b'sid')
Ya, ADa = cpaceA.compute_Yx()

# User Bob:
cpaceB = CPace(PRS=b'Password', role='responder', ADa=b'Alice', ADb=b'Bob', CI=b'CI', sid=b'sid')
Yb, ADb = cpaceB.compute_Yx()

# User Alice:
ISK_A = cpaceA.derive_ISK(Yb)

# User Bob:
ISK_B = cpaceB.derive_ISK(Ya)
```
