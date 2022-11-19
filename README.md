python-is-magic
===============

Some Linux distributions have packages called `python-is-python2` and
`python-is-python3` which control whether one gets python2 or python3 in
scripts that have a `#!/usr/bin/env python` shebang.

In either case, things break. That’s where `python-is-magic` comes in. It
rejects those choices and tries to “Do What I Mean”.

How Does It Work?
-----------------

The main mechanism is attempting to compile the target script as Python 3 code
in a subprocess without running it. If this fails, the script is assumed to be
Python 2 code.

What Are the Requirements?
--------------------------

You need Python 3.6 or higher.

What’s the Catch?
-----------------

Some extra startup time. Consider fixing your Python programs.

To-Do
-----

- [ ] Cache results

- [ ] Automate installation into `PATH`

License
-------

Take your pick of “public domain” equivalent licenses:

* [BSD Zero Clause License](https://spdx.org/licenses/0BSD.html)

* [MIT No Attribution](https://github.com/aws/mit-0)

* [The Unlicense](https://unlicense.org/)

* [Creative Commons Zero v1.0 Universal (or later)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)
