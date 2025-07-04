# deskitprt

A simple command-line tool for encrypting and decrypting files with a password.

## Installation

```bash
pip install deskitprt
```

## Usage

### Encrypt files

```bash
deskit -prt encrypt your_password_here
```

### Decrypt files

```bash
deskit -prt decrypt your_password_here
```

### Alternative Syntax

```bash
deskit encrypt your_password_here -d /path/to/directory
deskit decrypt your_password_here -d /path/to/directory
```

## Security Note

- Always use a strong password
- Keep backups of your encrypted files
- There is no password recovery option
