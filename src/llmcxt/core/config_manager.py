import json
from pathlib import Path
from typing import Dict
from .file_manager import FileManager

CONFIG_FILE = '.llmcxt_config.json'

class ConfigManager:
    def __init__(self, project_root: Path, file_manager: FileManager):
        self.project_root = project_root
        self.file_manager = file_manager
        self.config_path = self.project_root / CONFIG_FILE

    def load_config(self) -> Dict[str, str]:
        if self.config_path.exists():
            content = self.file_manager.read_file(self.config_path)
            return json.loads(content)
        return {}

    def save_config(self, context: Dict[str, str]) -> None:
        content = json.dumps(context)
        self.file_manager.write_file(self.config_path, content)