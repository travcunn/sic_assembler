SIC/XE Assembler
================

The SIC machine is a hypothetical computer system that can be found in "System Software: An Introduction to Systems Programming", by Leland Beck.

This is a 2 pass SIC/XE assembler implemented in Python.

###### Written by Travis Cunningham and Ashli Elrod


Features
--------
TODO


Usage
-----
```python
>>> from sic_assembler import Assembler
>>>
>>> # Pass in a file-like object containing the source program
>>> a = Assembler(open('test-programs/page58.asm', 'r'))
>>> # Run through both passes
>>> a.assemble()
>>>
>>> # Array of the objects generated with some debugging information
>>> # Each tuple contains the following: mnemonic, location, and the generated instruction
>>> a.generated_objects
[('STL', '0x30', '17202D'), ('LDB', '0x33', '69202D'), ('JSUB', '0x1036', '4B101036'), ('LDA', '0x33', '032026'), ('COMP', '0', '290000'), ('JEQ', '0x1a', '332007'), ('JSUB', '0x105d', '4B10105D'), ('J', '0x6', '3F2FEC'), ('LDA', '0x2d', '032010'), ('STA', '0x36', '0F2016'), ('LDA', '3', '010003'), ('STA', '0x33', '0F200D'), ('JSUB', '0x105d', '4B10105D'), ('J', '0x30', '3E2003'), ('BYTE', "C'EOF'", '454f46'), ('CLEAR', ('X', None), 'B410'), ('CLEAR', ('A', None), 'B400'), ('CLEAR', ('S', None), 'B440'), ('LDT', '1000', '75101000'), ('TD', '0x105c', 'E32019'), ('JEQ', '0x1040', '332FFA'), ('RD', '0x105c', 'DB2013'), ('COMPR', ('A', 'S'), 'A004'), ('JEQ', '0x1056', '332008'), ('STCH', '0x36', '57C003'), ('TIXR', ('T', None), 'B850'), ('JLT', '0x1040', '3B2FEA'), ('STX', '0x33', '134000'), ('RSUB', 0, '4F0000'), ('BYTE', "X'F1'", 'F1'), ('CLEAR', ('X', None), 'B410'), ('LDT', '0x33', '774000'), ('TD', '0x1076', 'E32011'), ('JEQ', '0x1062', '332FFA'), ('LDCH', '0x36', '53C003'), ('WD', '0x1076', 'DF2008'), ('TIXR', ('T', None), 'B850'), ('JLT', '0x1062', '3B2FEF'), ('RSUB', 0, '4F0000'), ('BYTE', "X'05'", '05')]
```

**You can also run each pass separately:**
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
>>> # Run through the second pass
>>> a.second_pass()
>>>
>>> # Array of the objects generated by the second pass
>>> a.generated_objects
[('STL', '0x30', '17202D'), ('LDB', '0x33', '69202D'), ('JSUB', '0x1036', '4B101036'), ('LDA', '0x33', '032026'), ('COMP', '0', '290000'), ('JEQ', '0x1a', '332007'), ('JSUB', '0x105d', '4B10105D'), ('J', '0x6', '3F2FEC'), ('LDA', '0x2d', '032010'), ('STA', '0x36', '0F2016'), ('LDA', '3', '010003'), ('STA', '0x33', '0F200D'), ('JSUB', '0x105d', '4B10105D'), ('J', '0x30', '3E2003'), ('BYTE', "C'EOF'", '454f46'), ('CLEAR', ('X', None), 'B410'), ('CLEAR', ('A', None), 'B400'), ('CLEAR', ('S', None), 'B440'), ('LDT', '1000', '75101000'), ('TD', '0x105c', 'E32019'), ('JEQ', '0x1040', '332FFA'), ('RD', '0x105c', 'DB2013'), ('COMPR', ('A', 'S'), 'A004'), ('JEQ', '0x1056', '332008'), ('STCH', '0x36', '57C003'), ('TIXR', ('T', None), 'B850'), ('JLT', '0x1040', '3B2FEA'), ('STX', '0x33', '134000'), ('RSUB', 0, '4F0000'), ('BYTE', "X'F1'", 'F1'), ('CLEAR', ('X', None), 'B410'), ('LDT', '0x33', '774000'), ('TD', '0x1076', 'E32011'), ('JEQ', '0x1062', '332FFA'), ('LDCH', '0x36', '53C003'), ('WD', '0x1076', 'DF2008'), ('TIXR', ('T', None), 'B850'), ('JLT', '0x1062', '3B2FEF'), ('RSUB', 0, '4F0000'), ('BYTE', "X'05'", '05')]
```


Command Line Usage
------------------
Included is a command line utility for assembling source files, which can be run after installing the package:

    $ sic-assembler ./my-program.asm
    
Or specify an output file:

    $ sic-assembler ./my-program.asm -o outfile
    
You can also [pipe](http://www.linfo.org/pipes.html) things around:

    $ cat my-program.asm | sic-assembler > outfile


Installation
------------

**Requirements**

- Python 2.7+

_This module has not been tested with Python 3._

It is helpful to use [virtualenv](http://www.virtualenv.org/en/latest/) to create an isolated Python environment.

###### Via source code / GitHub:

##### Standard Installation

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ python setup.py install
    
##### Standard Installation for underprivileged user accounts
> If you are not using [virtualenv](http://www.virtualenv.org/en/latest/) and have an underprileged account, it will not be possible to install the module correctly. Fortunately, it is still possible to run the module, since it doesn't depend on any external modules outside of the Python standard library.

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler/sic_assembler
    $ python __init__.py ../test-programs/page58.asm
    
##### Development Installation
> This requires one extra command, which will install any extra dependencies that are used in development.

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ pip install -r requirements.txt
    $ python setup.py develop


Testing
-------
This SIC/XE assembler has unit tests and regression tests.

Run all of the tests:

    $ python tests.py
    
Code coverage (including a report of lines that were not executed during the tests):

    $ coverage run tests.py
    $ coverage report -m
    
    
Caveats:
--------
- __The "simple" SIC program on page 47 is not valid a SIC/XE program.__ As mentioned later in chapter 2, if the mnemonic refers to a Format 4 instruction, our SIC/XE assembler should first attempt PC relative addressing, followed by an attempt to perform BASE relative addressing. An attempt to perform either of these addressing modes would raise an error when processing "CLOOP   JSUB   RDREC", since the label for "RDREC" is at hex(2039) and the location of "CLOOP" is at hex(1003). As we can see, the decimal of hex(2039)-hex(1003)=4150, which is a value too large for either PC or BASE relative. In order for this program to work with SIC/XE, the programmer must use the BASE directive to allow for BASE relative addressing. Alternatively, the programmer could extend the instruction by using "+JSUB" to allow for a larger address to be stored in the DISP field of the instruction.


Useful development links
------------------------

http://www-rohan.sdsu.edu/~stremler/2003_CS530/SicArchitecture.html

http://www.unf.edu/~cwinton/html/cop3601/s10/class.notes/basic4-SICfmts.pdf

http://cis.csuohio.edu/~jackie/cis335/sicxe_address.txt

Littab information: 
http://www.ut.edu.sa/documents/10156/1897914/Chapter+17-18
