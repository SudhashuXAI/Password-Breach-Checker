# Password Breach Checker

A command-line tool that checks whether a password has appeared in known data breaches — without ever sending your actual password (or even its full hash) over the internet.

Built as a CS50P final project, using the concepts from the **Libraries** lecture (`requests`, `argparse`, `hashlib`) along with exception handling and unit testing.

## How it works

This tool uses the [Have I Been Pwned](https://haveibeenpwned.com/) Pwned Passwords API, which is powered by a clever privacy-preserving technique called **k-anonymity**.

Here's the flow:

1. Your password is converted into a **SHA-1 hash** — a fixed-length fingerprint of the password.
2. The hash is split into two parts: the **first 5 characters** (prefix) and the **remaining characters** (suffix).
3. Only the 5-character prefix is sent to the API — never the full hash, and never the raw password.
4. The API responds with *every* leaked password hash that starts with that same prefix — often hundreds of them.
5. The matching is done **locally**, on your own machine, by searching the response for your specific suffix.

Because the server only ever sees a 5-character prefix shared by hundreds of other possible passwords, it never learns which exact password you were checking. This is what makes the check privacy-safe.

## Why SHA-1 here is fine

SHA-1 is no longer considered secure for things like digital signatures or certificates, because it's vulnerable to deliberately engineered collisions. However, that weakness doesn't apply to this use case — here, SHA-1 is only used as a lookup fingerprint against an existing breach database, not as a cryptographic guarantee against forgery. This is also why Have I Been Pwned itself still uses SHA-1 for this exact purpose.

## Features

- Checks a password against real, known data breaches
- Never transmits your raw password or full password hash
- Works both interactively and via a CLI flag
- Handles network errors (no internet, slow/unresponsive server) gracefully
- Comes with unit tests (`pytest`)

## Installation

```bash
pip install requests
pip install pytest
```

## Usage

**Interactive mode** (prompts you to type a password):
```bash
python project.py
```

**CLI flag mode** (pass the password directly):
```bash
python project.py --password yourpasswordhere
```

## Running tests

```bash
python -m pytest test_project.py
```

## Example output

```
Enter the password:- password123
Prefix: CBFDA
Suffix: C008F9CAB4083784CBD1874F76618D2A97
---- oh no..!! ----
 PASSWORD HAS BREACHED  3861730  many times .....
```

```
Enter the password:- xk29fjqm3l8sdf
Prefix: 91A2B
Suffix: ...
~ ~ ~ oh ! wow ! ~ ~ ~
 NO PASSWORD BREACH IS THERE ...
```

## Project structure

```
password-breach-checker/
├── project.py          # main logic
├── test_project.py     # unit tests
└── README.md
```

## What I learned

Building this project was less about the code and more about understanding *why* real-world security tools are designed the way they are — specifically, how k-anonymity lets a service verify something sensitive without ever learning the sensitive thing itself. I also got hands-on with using external APIs responsibly, handling network failures gracefully, and writing testable functions with predictable inputs and outputs.

## Credits

This project uses the free [Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) provided by Have I Been Pwned, created by Troy Hunt. This project is an independent tool built on top of that public API — it does not claim to replace or compete with the original service.
