# Graded exercises for [Amaranth HDL](https://amaranth-lang.org/docs/amaranth/latest/intro.html)

Work in progress!

* [00 - Introduction](00_intro.md)
* [01 - Counting coin: basic concepts](01_input.md)
* [02 - The day after: more if, and switch-case](02_switch.md)
* [03 - Life finds a way: parts of signals](03_parts.md)
* [04 - Signs: signed signals](04_signs.md)
* [05 - Synchronicity: synchronous signals](05_sync.md)
* [06 - Living in the past: multi-step asserts](06_past.md)
* [07 - Prove it! Formal verification by induction](07_proof.md)


# Kosmos

## Python virtual environment

Detailed setup: [follow this link](https://github.com/Logitech/cpg_kosmos_microblaze/blob/develop/README.md#python-virtual-environment)
 
Manual setup:
```shell
python -m venv --upgrade-deps --prompt Amaranth-Exercises .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

## PyCharm IDE
After running above commands, open PyCharm, and set the Python interpreter to the one in the virtual environment.  
It should be named `Amaranth-Exercises` and located in the project directory.
