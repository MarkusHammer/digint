# `digint`

> Base-Agnostic Integer Manipulation

`digint` is a module focused on easy high-level integer manipulation across any numerical base. Works with binary, decimal, or any other base. `digint` seeks to make complex digit-level and notation operations easy, just like they were `Collection`s.

[Documentation](https://MarkusHammer.github.io/digint)

## Setup

This module can be installed using:

```bash
pip install digint
```

## Usage

This module is intended to be used only as a module, and can be imported after installing using the traditional process:

```python
from digint import digitint
```

### Create an integer in any base

```python
# input integers as you would with `int()`,
# if the intiger is already in the base you wish to use
n1 = digitint(1234, base=10)
n2 = digitint("BASE36", base=36)
n3 = digitint(0xABCDEF, base=16)

# convert bases on initialization, if the input is a intiger type
n4 = digitint(255, base=2) # == 0b11111111
n5 = digitint(int("BASE36", 36), base=10) # == 683248722
n6 = digitint(0xABCDEF, base=10) # == 11259375
```

### Access and modify digits like a collection

```python
# get the digit at index 2
print(n1.get_digit(2)) # outputs "3"
num.set_digit(2, 5)
print(n1.get_digit(2)) # outputs "5"
```

### Easy notation

```python
print(str(n2)) # output "BASE36"
print(str(n3)) # output "ABCDEF"
print(str(n5)) # output "683248722", as the base is set to 10
```

### Full mutable collection implementation on integers

```python
print(n2.pop(-1)) #outputs "6"
print(n2.pop(-1)) #outputs "3"
n2.append(int("D", 36))
print(n2) #outputs "BASED"

# The sum of all digits
print(sum(n2)) #outputs "76"

# The average of all digits
print(sum(n2)/len(n2)) #outputs "15.2"
```

### Customizable Notation

```python
# same as str(n3) 
print(n3.notate()) # outputs "ABCDEF"

from digint import NotationFormat
fmt = NotationFormat(*tuple("0123456789ZYXWVU"))
print(n3.notate(fmt)) # outputs "ZYXWVU"
```

### And More

There are a handfull of other ease of use features that this module provides, feel free to reference the [documentation](https://MarkusHammer.github.io/digint) for more information.

## Licence

This is licensed under the Mozilla Public License 2.0 (MPL 2.0) Licence. See the Licence file in this repository for more information.

## Contribute

Contributions are always welcome!
Use the [github repository](https://github.com/MarkusHammer/digint) to report issues and contribute to this project.

## Credits

While not required, feel free to credit "Markus Hammer" (or just "Markus") if you find this code or script useful for whatever you may be doing with it.
