# py-cpace
**WARNING:** This is just a PoC. Use at your own risk. <br />
This is a simple python implementation of CPace defined in [draft-irtf-cfrg-cpace-13](https://www.ietf.org/archive/id/draft-irtf-cfrg-cpace-13.html).

It uses [pysodium](https://github.com/stef/pysodium) for all Ristretto255 functions. Therefore libsodium must be pre-installed [libsodium](https://doc.libsodium.org/).

## Usage:
### symmetric setting
```
# User A:
cpaceA = CPace(PRS, role='symmetric', ADa=ADa, ADb=ADb, CI=CI, sid=sid)
Ya, ADa = cpaceA.compute_Yx()

# User B:
cpaceB = CPace(PRS, role='symmetric', ADa=ADa, ADb=ADb, CI=CI, sid=sid)
Yb, ADb = cpaceB.compute_Yx()

# User A:
ISK_A = cpaceA.derive_ISK(Yb)

# User B:
ISK_B = cpaceB.derive_ISK(Ya)
```

### initiator-responder setting
```
# User A:
cpaceA = CPace(PRS, role='initiator', ADa=ADa, ADb=ADb, CI=CI, sid=sid)
Ya, ADa = cpaceA.compute_Yx()

# User B:
cpaceB = CPace(PRS, role='responder', ADa=ADa, ADb=ADb, CI=CI, sid=sid)
Yb, ADb = cpaceB.compute_Yx()

# User A:
ISK_A = cpaceA.derive_ISK(Yb)

# User B:
ISK_B = cpaceB.derive_ISK(Ya)
```
