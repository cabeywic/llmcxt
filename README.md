# llmcxt (LLM Context Tool)

llmcxt is a command-line tool designed to manage and generate context for Large Language Models (LLMs) from your project files. It allows you to easily add, remove, and list files in your project, and generate a comprehensive context that includes both the project structure and the contents of selected files.

## Features

- Add single or multiple files to the context
- Remove single or multiple files from the context
- List the project structure
- Generate a comprehensive context for LLMs
- Ignore files based on .cxtignore or .gitignore patterns
- Colorized output for better readability
- Easy cleanup with a delete command
- Automatically copy generated context to clipboard (optional)
- View list of files in the current context

## Installation

You can install llmcxt directly from PyPI:

```
pip install llmcxt
```

## Usage

After installation, you can use the `llmcxt` command from anywhere in your project directory. The tool will look for a `.cxtignore` file (or `.gitignore` if `.cxtignore` is not found) in the parent directories to determine the project root.

### Basic Commands

- Add file(s) to context:
  ```
  llmcxt add <file1> [<file2> ...]
  ```

- Remove file(s) from context:
  ```
  llmcxt remove <file1> [<file2> ...]
  ```

- List project structure:
  ```
  llmcxt ls
  ```

- Generate context:
  ```
  llmcxt generate
  ```

- Generate context and copy to clipboard:
  ```
  llmcxt generate --clipboard
  ```

- View current context (file paths):
  ```
  llmcxt context
  ```

- Drop all context:
  ```
  llmcxt drop
  ```

- Delete llmcxt and all related files:
  ```
  llmcxt delete
  ```

### Examples

1. Add multiple files to the context:
   ```
   llmcxt add src/main.py tests/test_main.py
   ```

2. Remove a file from the context:
   ```
   llmcxt remove src/deprecated.py
   ```

3. Generate context for LLM:
   ```
   llmcxt generate > llm_context.txt
   ```

## Configuration

### Ignore File

Create a `.cxtignore` file in your project root to specify patterns for files and directories that should be ignored. If `.cxtignore` is not found, the tool will fall back to using `.gitignore`.

Example `.cxtignore`:
```
# Ignore Python cache files
__pycache__/
*.pyc

# Ignore virtual environment
venv/

# Ignore .git directory
.git/

# Ignore the configuration file itself
.llmcxt_config.json
```

## Uninstallation

To remove llmcxt and all related files, run:
```
llmcxt delete
```

This will prompt for confirmation before removing the tool and its dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.