"""A narrow publication guard, not a guarantee or substitute for human review."""
import re
import subprocess
from pathlib import Path

rules = [
    ('private key', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    ('cloud key', r'AKIA[0-9A-Z]{16}'),
    ('access token', r'gh[pousr]_[A-Za-z0-9]{25,}'),
    ('fine-grained token', r'github_pat_[A-Za-z0-9_]{20,}'),
    ('home directory', r'/(?:Users|home)/[A-Za-z0-9_.-]+/'),
    ('email address', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
]

def inspect_text(text):
    return [label for label, pattern in rules if re.search(pattern, text)]


def main():
    root = Path(__file__).resolve().parents[1]
    paths = list(filter(None, subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')))
    violations = []
    for name in paths:
        path = root / name
        if name.endswith(('.png', '.jpg')):
            continue  # Screenshots require visual inspection.
        if path.suffix.lower() in {'.pdf', '.docx', '.sqlite', '.zip', '.pem'} or path.name.startswith('.env'):
            violations.append(f'{name}: unexpected sensitive/binary artifact')
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            violations.append(f'{name}: unreviewed binary file')
            continue
        violations.extend(f'{name}: {label}' for label in inspect_text(text))
    if violations:
        raise SystemExit('\n'.join(violations))
    print(f'Public-content pattern check passed ({len(paths)} tracked files). Manual review still required.')


if __name__ == '__main__':
    main()
