# blockchain
## Overview
This simple blockchain-based code demonstrates the fundamental ideas behind cryptocurrencies.
### Dependencies
 - [Python 3].
 - [ECDSA library for Python].

## Example output
```text
source wallet:
  private key: TWaGQ6IYTQySqs39Zl73SiyqGhBQaXFM
  public  key: RDxhGMCJgYYGKTU8oFA+fsIW6nJCfa5jkxZLH34JhYAkrvYqAZuHxe4JuYeXYt4o

target wallet:
  private key: 9HZwqFg8XQCex0pPHgYyj1i5EQ4LEUIp
  public  key: Bjc7m61soM3BKg9gECqoyyVC8BY+MSxEeVDe9aB+nCBHjiCLaUKNazQpSCoH6/q4

blockchain is valid

blockchain:
index timestamp                  previous_hash
0     2017-11-17 15:02:21.947443 none                                                            
1     2017-11-17 15:02:21.963989 00030a0bec146899598182b75263eb5418175430654376894a8700b116f4af10
  transaction 1:
    from     : network
    to       : RDxhGMCJgYYGKTU8oFA+fsIW6nJCfa5jkxZLH34JhYAkrvYqAZuHxe4JuYeXYt4o
    amount   : 10
    signature: reward
2     2017-11-17 15:02:22.067297 00006ed974af93c70cb6f157283e5fdd78d355f8a26c6622187f9b4f27f98b6a
  transaction 1:
    from     : RDxhGMCJgYYGKTU8oFA+fsIW6nJCfa5jkxZLH34JhYAkrvYqAZuHxe4JuYeXYt4o
    to       : Bjc7m61soM3BKg9gECqoyyVC8BY+MSxEeVDe9aB+nCBHjiCLaUKNazQpSCoH6/q4
    amount   : 2.5
    signature: yORZ48faCCl4nRgYgOGCCtFFr/m+u5z6DFJ1fOxAVKMEdvpcB88GoorB90GQzQez
  transaction 2:
    from     : RDxhGMCJgYYGKTU8oFA+fsIW6nJCfa5jkxZLH34JhYAkrvYqAZuHxe4JuYeXYt4o
    to       : Bjc7m61soM3BKg9gECqoyyVC8BY+MSxEeVDe9aB+nCBHjiCLaUKNazQpSCoH6/q4
    amount   : 3.5
    signature: GcOrw9n0PIG+6wIKfb3VM6j51wW7x1Fw8dQsfcX6ox5O40gxdtm8veUkIVSA3dt3
  transaction 3:
    from     : network
    to       : RDxhGMCJgYYGKTU8oFA+fsIW6nJCfa5jkxZLH34JhYAkrvYqAZuHxe4JuYeXYt4o
    amount   : 10
    signature: reward

source wallet:
  balance: 14.0
target wallet:
  balance: 6.0
```

[Python 3]:https://www.python.org/download/releases/3.0/
[ECDSA library for Python]:https://pypi.python.org/pypi/ecdsa
