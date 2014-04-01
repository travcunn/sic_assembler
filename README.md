SIC/XE Assembler
================

A 2 pass SIC/XE assembler.


Installation
------------

Via source code / GitHub:

    $ git clone https://github.com/travcunn/sic_assembler.git sic_assembler
    $ cd sic_assembler
    $ python setup.py install
    

Usage
-----
```python
>>> from sic_assembler import Assembler
>>>
>>> a = Assembler(file='source-file.asm')
>>> # generate some assembly
>>> a.assemble()
>>>
>>> # array of the objects generated with some debugging information
>>> a.generated_objects
[]
```

Command Line
------------
Included is a command line utility for assembling source files, which can be run after installing the package:

    $ sic-assembler ./my-program.asm
    
Or specify an output file:

    $ sic-assembler ./my-program.asm -o outfile
    
You can also pipe things around:

    $ cat my-program.asm | sic-assembler > outfile


Features
--------
todo
