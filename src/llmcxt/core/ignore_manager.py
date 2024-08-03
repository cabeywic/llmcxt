import fnmatch
from pathlib import Path
from typing import List

class IgnorePatternManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.ignore_patterns: List[str] = []

    def load_ignore_file(self) -> None:
        ignore_file = self.project_root / '.cxtignore'
        if not ignore_file.exists():
            ignore_file = self.project_root / '.gitignore'
        if ignore_file.exists():
            with ignore_file.open('r') as f:
                self.ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def should_ignore(self, path: str) -> bool:
        # Convert the path to a relative path if it's absolute
        rel_path = Path(path).relative_to(self.project_root) if Path(path).is_absolute() else Path(path)
        
        for pattern in self.ignore_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                if fnmatch.fnmatch(str(rel_path), pattern) or fnmatch.fnmatch(str(rel_path) + '/', pattern):
                    return True
            else:
                # File pattern
                if fnmatch.fnmatch(str(rel_path), pattern):
                    return True
            
            # Check if any parent directory matches the pattern
            for parent in rel_path.parents:
                if fnmatch.fnmatch(str(parent) + '/', pattern):
                    return True
        
        return False

    def debug_ignore(self, path: str) -> None:
        """Debug method to print ignore decision for a given path"""
        rel_path = Path(path).relative_to(self.project_root) if Path(path).is_absolute() else Path(path)
        print(f"Checking ignore for: {rel_path}")
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(str(rel_path), pattern) or fnmatch.fnmatch(str(rel_path) + '/', pattern):
                print(f"  Matched pattern: {pattern}")
                return
        print("  Not ignored")