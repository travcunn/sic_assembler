SIC/XE Assembler
================

> The SIC machine is a hypothetical computer system that can be found in "System Software: An Introduction to Systems Programming", by Leland Beck.

This is a 2 pass SIC/XE assembler implemented in Python.

###### Written by Travis Cunningham and Ashli Elrod


TODO
----
- [Required Features](https://github.com/travcunn/sic_assembler/issues?labels=required-feature&page=1&state=open)
- [Future Enhancements](https://github.com/travcunn/sic_assembler/issues?labels=enhancement&page=1&state=open)


Requirements
------------
    Python 2.7+

This module has not been tested with Python 3.


Installation
------------
It is helpful to use [virtualenv](https://pypi.python.org/pypi/virtualenv) to create an isolated Python environment.

###### Via source code / GitHub:

##### Standard Installation

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ python setup.py install
    
##### Standard Installation for underprivileged user accounts
> If you are not using [virtualenv](https://pypi.python.org/pypi/virtualenv) and have an underprileged account, it will not be possible to install the module correctly. Fortunately, it is still possible to run the module, since it doesn't depend on any external modules outside of the Python standard library.

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler/sic_assembler
    $ python __init__.py ../test-programs/page58.asm
    
##### Development Installation
> This requires one extra command, which will install any extra dependencies that are used in development.

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ pip install -r requirements.txt
    $ python setup.py develop


Usage
-----
```python
>>> from sic_assembler import Assembler
>>>
>>> # Pass in a file-like object containing the source program
>>> a = Assembler(open('test-programs/simple-program.asm', 'r'))
>>> # Run through both passes
>>> a.assemble()
>>>
>>> # Array of the objects generated with some debugging information
>>> # Each tuple contains the following: mnemonic, location, and the generated instruction
>>> a.generated_objects
[('STL', '0x1033', '141033'), ('JSUB', '0x2039', '482039'), ('LDA', '0x1036', '001036'), ('COMP', '0x1030', '281030'), ('JEQ', '0x1015', '301015'), ('JSUB', '0x2061', '482061'), ('J', '0x1003', '3c1003'), ('LDA', '0x102a', '00102a'), ('STA', '0x1039', '0c1039'), ('LDA', '0x102d', '00102d'), ('STA', '0x1036', '0c1036'), ('JSUB', '0x2061', '482061'), ('LDL', '0x1033', '081033'), ('RSUB', 0, '4c0000'), ('BYTE', "C'EOF'", '454f46'), ('WORD', '3', '000003'), ('WORD', '0', '000000'), ('LDX', '0x1030', '041030'), ('LDA', '0x1030', '001030'), ('TD', '0x205d', 'e0205d'), ('JEQ', '0x203f', '30203f'), ('RD', '0x205d', 'd8205d'), ('COMP', '0x1030', '281030'), ('JEQ', '0x2057', '302057'), ('STCH', '0x1039', '541039'), ('TIX', '0x205e', '2c205e'), ('JLT', '0x203f', '38203f'), ('STX', '0x1036', '101036'), ('RSUB', 0, '4c0000'), ('BYTE', "X'F1'", 'F1'), ('WORD', '4096', '001000'), ('LDX', '0x1030', '041030'), ('TD', '0x2079', 'e02079'), ('JEQ', '0x2064', '302064'), ('LDCH', '0x1039', '501039'), ('WD', '0x2079', 'dc2079'), ('TIX', '0x1036', '2c1036'), ('JLT', '0x2064', '382064'), ('RSUB', 0, '4c0000'), ('BYTE', "X'05'", '05')]
```

**You can also run each pass separately:**
```python
>>> from sic_assembler import Assembler
>>>
>>> a = Assembler(open('test-programs/simple-program.asm', 'r'))
>>> # Run through the first pass
>>> a.first_pass()
>>>
>>> # Array of the intermediate contents produced by the first pass
>>> a.temp_contents
['      FIRST  STL    RETADR', '      CLOOP  JSUB   RDREC', '             LDA    LENGTH', '             COMP   ZERO', '             JEQ    ENDFIL', '             JSUB   WRREC', '             J      CLOOP', '      ENDFIL LDA    EOF', '             STA    BUFFER', '             LDA    THREE', '             STA    LENGTH', '             JSUB   WRREC', '             LDL    RETADR', '             RSUB', "      EOF    BYTE   C'EOF'", '      THREE  WORD   3', '      ZERO   WORD   0', '      RETADR RESW   1', '      LENGTH RESW   1', '      BUFFER RESB   4096', '      RDREC  LDX    ZERO', '             LDA    ZERO', '      RLOOP  TD     INPUT', '             JEQ    RLOOP', '             RD     INPUT', '             COMP   ZERO', '             JEQ    EXIT', '             STCH   BUFFER', '             TIX    MAXLEN', '             JLT    RLOOP', '      EXIT   STX    LENGTH', '             RSUB', "      INPUT  BYTE   X'F1'", '      MAXLEN WORD   4096', '      WRREC  LDX    ZERO', '      WLOOP  TD     OUTPUT', '             JEQ    WLOOP', '             LDCH   BUFFER', '             WD     OUTPUT', '             TIX    LENGTH', '             JLT    WLOOP', '             RSUB', "      OUTPUT BYTE   X'05'"]
>>> # Run through the second pass
>>> a.second_pass()
>>>
>>> # Array of the objects generated by the second pass
>>> a.generated_objects
[('STL', '0x1033', '141033'), ('JSUB', '0x2039', '482039'), ('LDA', '0x1036', '001036'), ('COMP', '0x1030', '281030'), ('JEQ', '0x1015', '301015'), ('JSUB', '0x2061', '482061'), ('J', '0x1003', '3c1003'), ('LDA', '0x102a', '00102a'), ('STA', '0x1039', '0c1039'), ('LDA', '0x102d', '00102d'), ('STA', '0x1036', '0c1036'), ('JSUB', '0x2061', '482061'), ('LDL', '0x1033', '081033'), ('RSUB', 0, '4c0000'), ('BYTE', "C'EOF'", '454f46'), ('WORD', '3', '000003'), ('WORD', '0', '000000'), ('LDX', '0x1030', '041030'), ('LDA', '0x1030', '001030'), ('TD', '0x205d', 'e0205d'), ('JEQ', '0x203f', '30203f'), ('RD', '0x205d', 'd8205d'), ('COMP', '0x1030', '281030'), ('JEQ', '0x2057', '302057'), ('STCH', '0x1039', '541039'), ('TIX', '0x205e', '2c205e'), ('JLT', '0x203f', '38203f'), ('STX', '0x1036', '101036'), ('RSUB', 0, '4c0000'), ('BYTE', "X'F1'", 'F1'), ('WORD', '4096', '001000'), ('LDX', '0x1030', '041030'), ('TD', '0x2079', 'e02079'), ('JEQ', '0x2064', '302064'), ('LDCH', '0x1039', '501039'), ('WD', '0x2079', 'dc2079'), ('TIX', '0x1036', '2c1036'), ('JLT', '0x2064', '382064'), ('RSUB', 0, '4c0000'), ('BYTE', "X'05'", '05')]
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
    
Run a single test called "TestInstructionGeneration":

    $ python tests.py TestInstructionGeneration


Useful development links
------------------------

http://www-rohan.sdsu.edu/~stremler/2003_CS530/SicArchitecture.html

http://www.unf.edu/~cwinton/html/cop3601/s10/class.notes/basic4-SICfmts.pdf

http://cis.csuohio.edu/~jackie/cis335/sicxe_address.txt
