from abc import ABC, abstractmethod
from pathlib import Path

class FileManager(ABC):
    @abstractmethod
    def read_file(self, file_path: Path) -> str:
        pass

    @abstractmethod
    def write_file(self, file_path: Path, content: str) -> None:
        pass

class LocalFileManager(FileManager):
    def read_file(self, file_path: Path) -> str:
        with file_path.open('r') as f:
            return f.read()

    def write_file(self, file_path: Path, content: str) -> None:
        with file_path.open('w') as f:
            f.write(content)