The Forensics Playground File Format
====================================

The Forensic Playground File Format (FPFF) is an open format designed to serve as a sandbox for
forensics education and competition. It has three main goals:

1. **Resemblance**. FPFF is similar to many common binary formats, making it a good tool
for familiarizing students with binary layouts and parsing.
2. **Uniqueness**. FPFF is different enough from real formats, preventing automatic analysis with
tools like `binwalk`.
3. **Flexibility**. FPFF's specification is simple, making extension and
modification straightforward.

## Specification

FPFF's spec (and `pandoc` sources) can be found in the [spec](spec) directory.

## Reference implementation

A reference implementation will be added to this repository after
[CMSC389R](https://github.com/UMD-CS-STICs/389Rspring18) concludes.

## Pedagogical notes

Because a reference implementation is available, future course designers and CTF challenge-builders
are encouraged to modify the specification.

## License

The FPFF specification and reference implementation are released under the MIT license.
