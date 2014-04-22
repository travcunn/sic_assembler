SIC/XE Assembler
================

The SIC machine is a hypothetical computer system that can be found in "System Software: An Introduction to Systems Programming", by Leland Beck.

This is a multi-pass SIC/XE assembler implemented in Python.

###### Written by Travis Cunningham and Ashli Elrod

- [Installation](#installation)
- [Usage](#usage)
- [Command Line Usage](#command-line-usage)
- [Testing](#testing)
- [Caveats](#caveats)


Features
--------
To better understand the functionality of the assembler, more than 2 steps were needed. The 2 step assembler mentioned in the textbook generates object records as each source line is encountered in the second pass. Instead, we added an additional step to allow for easy analysis of the object code. On pass 2, this assembler generates "Format" objects that are placed into an array. This allows for the user to check each bit of the instruction before it is converted into hex. The final step takes each object from the array and generates a hex representation of the instruction.

Basic features:

- Indexed addressing, direct and indirect addressing, immediate addressing modes
- PC and BASE relative addressing
- Extended format instructions (format 4)

Directives:
- BYTE, WORD, RESB, RESW, BASE

Object records:
- Header, Text, and End


Installation
------------

**Requirements**

- Python 2.7+

It is helpful to use [virtualenv](http://www.virtualenv.org/en/latest/) to create an isolated Python environment.

##### Standard Installation

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ python setup.py install
    
##### Standard Installation for underprivileged user accounts
If you are not using [virtualenv](http://www.virtualenv.org/en/latest/) and have an underprileged account, it will not be possible to install the module correctly. Fortunately, it is still possible to run the module, since it doesn't depend on any external modules outside of the Python standard library.

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler/sic_assembler
    $ python __init__.py ../test-programs/page58.asm


Usage
-----
Basic example:
```python
>>> from sic_assembler import Assembler
>>>
>>> # Pass in a file-like object containing the source program
>>> a = Assembler(open('test-programs/page58.asm', 'r'))
>>>
>>> # Run through all passes and return object program records
>>> a.assemble()
['HCOPY  000000001077', 'T0000001D17202D69202D4B1010360320262900003320074B10105D3F2FEC032010', 'T00001D1D0F20160100030F200D4B10105D3E2003454F46B410B400B44075101000', 'T0010401FE32019332FFADB2013A00433200857C003B8503B2FEA1340004F0000F1B410', 'T00105F18774000E32011332FFA53C003DF2008B8503B2FEF4F000005', 'E000000']
```

Run each pass separately:
```python
>>> from sic_assembler import Assembler
>>>
>>> a = Assembler(open('test-programs/page58.asm', 'r'))
>>> # Run through the first pass
>>> a.first_pass()
>>>
>>> # Array of the intermediate contents produced by the first pass
>>> a.temp_contents
[<SourceLine: FIRST, STL, RETADR>, <SourceLine: None, LDB, #LENGTH>, <SourceLine: None, BASE, LENGTH>, <SourceLine: CLOOP, +JSUB, RDREC>, <SourceLine: None, LDA, LENGTH>, <SourceLine: None, COMP, #0>, <SourceLine: None, JEQ, ENDFIL>, <SourceLine: None, +JSUB, WRREC>, <SourceLine: None, J, CLOOP>, <SourceLine: ENDFIL, LDA, EOF>, <SourceLine: None, STA, BUFFER>, <SourceLine: None, LDA, #3>, <SourceLine: None, STA, LENGTH>, <SourceLine: None, +JSUB, WRREC>, <SourceLine: None, J, @RETADR>, <SourceLine: EOF, BYTE, C'EOF'>, <SourceLine: RETADR, RESW, 1>, <SourceLine: LENGTH, RESW, 1>, <SourceLine: BUFFER, RESB, 4096>, <SourceLine: RDREC, CLEAR, X>, <SourceLine: None, CLEAR, A>, <SourceLine: None, CLEAR, S>, <SourceLine: None, +LDT, #4096>, <SourceLine: RLOOP, TD, INPUT>, <SourceLine: None, JEQ, RLOOP>, <SourceLine: None, RD, INPUT>, <SourceLine: None, COMPR, A,S>, <SourceLine: None, JEQ, EXIT>, <SourceLine: None, STCH, BUFFER,X>, <SourceLine: None, TIXR, T>, <SourceLine: None, JLT, RLOOP>, <SourceLine: EXIT, STX, LENGTH>, <SourceLine: None, RSUB, None>, <SourceLine: INPUT, BYTE, X'F1'>, <SourceLine: WRREC, CLEAR, X>, <SourceLine: None, LDT, LENGTH>, <SourceLine: WLOOP, TD, OUTPUT>, <SourceLine: None, JEQ, WLOOP>, <SourceLine: None, LDCH, BUFFER,X>, <SourceLine: None, WD, OUTPUT>, <SourceLine: None, TIXR, T>, <SourceLine: None, JLT, WLOOP>, <SourceLine: None, RSUB, None>, <SourceLine: OUTPUT, BYTE, X'05'>]
>>>
>>> # Run through the second pass
>>> a.second_pass()
>>>
>>> # Generate an array of the objects generated with some debugging information
>>> # (Address(int), (Format object or directive output))
>>> a.generated_objects
[(0, <Format3: mnemonic=STL n=True i=True flags=2 disp=0x30>), (3, <Format3: mnemonic=LDB n=False i=True flags=2 disp=0x33>), (6, <Format3: mnemonic=JSUB n=True i=True flags=1 disp=0x1036>), (10, <Format3: mnemonic=LDA n=True i=True flags=2 disp=0x33>), (13, <Format3: mnemonic=COMP n=False i=True flags=0 disp=0>), (16, <Format3: mnemonic=JEQ n=True i=True flags=2 disp=0x1a>), (19, <Format3: mnemonic=JSUB n=True i=True flags=1 disp=0x105d>), (23, <Format3: mnemonic=J n=True i=True flags=2 disp=0x6>), (26, <Format3: mnemonic=LDA n=True i=True flags=2 disp=0x2d>), (29, <Format3: mnemonic=STA n=True i=True flags=2 disp=0x36>), (32, <Format3: mnemonic=LDA n=False i=True flags=0 disp=3>), (35, <Format3: mnemonic=STA n=True i=True flags=2 disp=0x33>), (38, <Format3: mnemonic=JSUB n=True i=True flags=1 disp=0x105d>), (42, <Format3: mnemonic=J n=True i=False flags=2 disp=0x30>), (45, ('BYTE', "C'EOF'", '454f46')), (4150, <Format2: mnemonic=CLEAR r1=X r2=None>), (4152, <Format2: mnemonic=CLEAR r1=A r2=None>), (4154, <Format2: mnemonic=CLEAR r1=S r2=None>), (4156, <Format3: mnemonic=LDT n=False i=True flags=1 disp=1000>), (4160, <Format3: mnemonic=TD n=True i=True flags=2 disp=0x105c>), (4163, <Format3: mnemonic=JEQ n=True i=True flags=2 disp=0x1040>), (4166, <Format3: mnemonic=RD n=True i=True flags=2 disp=0x105c>), (4169, <Format2: mnemonic=COMPR r1=A r2=S>), (4171, <Format3: mnemonic=JEQ n=True i=True flags=2 disp=0x1056>), (4174, <Format3: mnemonic=STCH n=True i=True flags=12 disp=0x36>), (4177, <Format2: mnemonic=TIXR r1=T r2=None>), (4179, <Format3: mnemonic=JLT n=True i=True flags=2 disp=0x1040>), (4182, <Format3: mnemonic=STX n=True i=True flags=4 disp=0x33>), (4185, <Format3: mnemonic=RSUB n=True i=True flags=0 disp=0>), (4188, ('BYTE', "X'F1'", 'F1')), (4189, <Format2: mnemonic=CLEAR r1=X r2=None>), (4191, <Format3: mnemonic=LDT n=True i=True flags=4 disp=0x33>), (4194, <Format3: mnemonic=TD n=True i=True flags=2 disp=0x1076>), (4197, <Format3: mnemonic=JEQ n=True i=True flags=2 disp=0x1062>), (4200, <Format3: mnemonic=LDCH n=True i=True flags=12 disp=0x36>), (4203, <Format3: mnemonic=WD n=True i=True flags=2 disp=0x1076>), (4206, <Format2: mnemonic=TIXR r1=T r2=None>), (4208, <Format3: mnemonic=JLT n=True i=True flags=2 disp=0x1062>), (4211, <Format3: mnemonic=RSUB n=True i=True flags=0 disp=0>), (4214, ('BYTE', "X'05'", '05'))]
>>>
>>> # Generate object program records in the third pass
>>> a.generate_records()
['HCOPY  000000001077', 'T0000001D17202D69202D4B1010360320262900003320074B10105D3F2FEC032010', 'T00001D1D0F20160100030F200D4B10105D3E2003454F46B410B400B44075101000', 'T0010401FE32019332FFADB2013A00433200857C003B8503B2FEA1340004F0000F1B410', 'T00105F18774000E32011332FFA53C003DF2008B8503B2FEF4F000005', 'E000000']
```

Write object program records to a file:
```python
>>> from sic_assembler import Assembler
>>>
>>> a = Assembler(open('test-programs/page58.asm', 'r'))
>>> out_records = a.assemble()
>>>
>>> # open a file and write each object program record
>>> with open('a.out', 'w') as out:
>>>     for record in output_records:
>>>         out.write(record)
>>>         out.write('\n')
```

Command Line Usage
------------------
Included is a command line utility for assembling source files, which can be run after installing the package:

    $ sic-assembler ./my-program.asm
    
Or specify an output file:

    $ sic-assembler ./my-program.asm -o outfile
    
You can also [pipe](http://www.linfo.org/pipes.html) things around:

    $ cat my-program.asm | sic-assembler > outfile


Testing
-------
Run all of the tests:

    $ python tests.py
    
Code coverage (including a report of lines that were not executed during the tests):

    $ coverage run tests.py
    $ coverage report -m
    
    
Caveats
-------
- __The "simple" SIC program on page 47 is not valid a SIC/XE program.__ As mentioned later in chapter 2, if the mnemonic refers to a Format 4 instruction, our SIC/XE assembler should first attempt PC relative addressing, followed by an attempt to perform BASE relative addressing. An attempt to perform either of these addressing modes would raise an error when processing "CLOOP   JSUB   RDREC", since the label for "RDREC" is at hex(2039) and the location of "CLOOP" is at hex(1003). As we can see, the decimal of hex(2039)-hex(1003)=4150, which is a value too large for either PC or BASE relative. In order for this program to work with SIC/XE, the programmer must use the BASE directive to allow for BASE relative addressing. Alternatively, the programmer could extend the instruction by using "+JSUB" to allow for a larger address to be stored in the DISP field of the instruction.
