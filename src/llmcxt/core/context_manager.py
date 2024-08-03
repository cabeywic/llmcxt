import os
import click
from pathlib import Path
from typing import List, Dict
from .file_manager import FileManager
from .ignore_manager import IgnorePatternManager
from .config_manager import ConfigManager


class ContextManager:
    def __init__(self, project_root: Path, file_manager: FileManager, ignore_manager: IgnorePatternManager, config_manager: ConfigManager):
        self.project_root = project_root
        self.file_manager = file_manager
        self.ignore_manager = ignore_manager
        self.config_manager = config_manager
        self.context = self.config_manager.load_config()

    def add_files(self, file_paths: List[str], recursive: bool = False) -> List[str]:
        added = []
        for file_path in file_paths:
            try:
                abs_path = (self.project_root / file_path).resolve()
                if not abs_path.exists():
                    raise FileNotFoundError(f"File or directory not found: {file_path}")
                
                if abs_path.is_dir():
                    if recursive:
                        for root, dirs, files in os.walk(abs_path):
                            rel_root = Path(root).relative_to(self.project_root)
                            for file in files:
                                file_rel_path = rel_root / file
                                if not self.ignore_manager.should_ignore(str(file_rel_path)):
                                    file_abs_path = self.project_root / file_rel_path
                                    self.context[str(file_rel_path)] = self.file_manager.read_file(file_abs_path)
                                    added.append(str(file_rel_path))
                    added.append(str(abs_path.relative_to(self.project_root)))
                else:
                    rel_path = abs_path.relative_to(self.project_root)
                    if self.ignore_manager.should_ignore(str(rel_path)):
                        raise ValueError(f"File is ignored: {file_path}")
                    self.context[str(rel_path)] = self.file_manager.read_file(abs_path)
                    added.append(str(rel_path))
            except Exception as e:
                raise RuntimeError(f"Error adding {file_path}: {str(e)}")
        self.config_manager.save_config(self.context)
        return added

    def remove_files(self, file_paths: List[str]) -> List[str]:
        removed = []
        for file_path in file_paths:
            rel_path = str(Path(file_path))
            if rel_path in self.context:
                del self.context[rel_path]
                removed.append(file_path)
            else:
                raise ValueError(f"File not in context: {file_path}")
        self.config_manager.save_config(self.context)
        return removed

    def get_context_files(self) -> List[str]:
        return list(self.context.keys())

    def generate_context(self) -> str:
        context = click.style(f"Project Root: {self.project_root}\n\n", fg='green', bold=True)
        context += click.style("Project Structure:\n", fg='yellow', underline=True)
        context += self.list_structure()
        context += click.style("\n\nFile Contents:\n", fg='yellow', underline=True)
        for file_path, content in self.context.items():
            context += click.style(f"\n--- {file_path} ---\n", fg='magenta', bold=True)
            context += content + "\n"
        return context

    def drop_all(self) -> None:
        self.context.clear()
        self.config_manager.save_config(self.context)

    def list_structure(self) -> str:
        structure = []
        for root, dirs, files in os.walk(self.project_root):
            rel_root = Path(root).relative_to(self.project_root)
            
            if self.ignore_manager.should_ignore(str(rel_root)):
                dirs[:] = []
                continue
            
            level = len(rel_root.parts)
            indent = '    ' * level
            structure.append(click.style(f'{indent}{os.path.basename(root)}/', fg='blue', bold=True))
            
            dirs[:] = [d for d in dirs if not self.ignore_manager.should_ignore(str(rel_root / d))]
            
            sorted_files = sorted(files)
            for file in sorted_files:
                file_path = rel_root / file
                if not self.ignore_manager.should_ignore(str(file_path)):
                    structure.append(click.style(f'{indent}    {file}', fg='cyan'))
        
        return '\n'.join(structure)

    def should_ignore(self, path: str) -> bool:
        return self.ignore_manager.should_ignore(path)