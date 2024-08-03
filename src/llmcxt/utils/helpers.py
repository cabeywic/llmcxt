import re
from pathlib import Path

def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

class ProjectRootFinder:
    @staticmethod
    def find_project_root() -> Path:
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            if (current_dir / '.cxtignore').exists():
                return current_dir
            if (current_dir / '.gitignore').exists():
                return current_dir
            current_dir = current_dir.parent
        return Path.cwd()  # If no .cxtignore or .gitignore found, use current directory