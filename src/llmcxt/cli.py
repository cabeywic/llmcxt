import os
import json
import click
import fnmatch
import shutil
from pathlib import Path

CONFIG_FILE = '.llmcxt_config.json'

class ContextManager:
    def __init__(self):
        self.context = {}
        self.ignore_patterns = []
        self.project_root = self.find_project_root()
        self.load_config()
        self.load_ignore_file()

    def find_project_root(self):
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            if (current_dir / '.cxtignore').exists():
                return current_dir
            if (current_dir / '.gitignore').exists():
                click.secho(f"No .cxtignore found, using .gitignore in {current_dir}", fg="yellow")
                return current_dir
            current_dir = current_dir.parent
        return Path.cwd()  # If no .cxtignore or .gitignore found, use current directory

    def load_config(self):
        config_path = self.project_root / CONFIG_FILE
        if config_path.exists():
            with config_path.open('r') as f:
                self.context = json.load(f)

    def save_config(self):
        config_path = self.project_root / CONFIG_FILE
        with config_path.open('w') as f:
            json.dump(self.context, f)

    def load_ignore_file(self):
        ignore_file = self.project_root / '.cxtignore'
        if not ignore_file.exists():
            ignore_file = self.project_root / '.gitignore'
        if ignore_file.exists():
            with ignore_file.open('r') as f:
                self.ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def add_files(self, file_paths):
        added = []
        for file_path in file_paths:
            try:
                abs_path = (self.project_root / file_path).resolve()
                rel_path = abs_path.relative_to(self.project_root)
                if not abs_path.exists():
                    click.secho(f"File not found: {file_path}", fg="red")
                    continue
                if self.should_ignore(str(rel_path)):
                    click.secho(f"File is ignored: {file_path}", fg="yellow")
                    continue
                with abs_path.open('r') as file:
                    self.context[str(rel_path)] = file.read()
                added.append(file_path)
            except Exception as e:
                click.secho(f"Error adding {file_path}: {str(e)}", fg="red")
        self.save_config()
        return added

    def remove_files(self, file_paths):
        removed = []
        for file_path in file_paths:
            rel_path = str(Path(file_path))
            if rel_path in self.context:
                del self.context[rel_path]
                removed.append(file_path)
            else:
                click.secho(f"File not in context: {file_path}", fg="yellow")
        self.save_config()
        return removed

    def drop_all(self):
        self.context.clear()
        self.save_config()

    def should_ignore(self, path):
        return any(fnmatch.fnmatch(path, pattern) for pattern in self.ignore_patterns)

    def list_structure(self):
        structure = []
        for root, dirs, files in os.walk(self.project_root):
            level = Path(root).relative_to(self.project_root).parts
            indent = '    ' * len(level)
            subindent = '    ' * (len(level) + 1)
            
            if not self.should_ignore(str(Path(root).relative_to(self.project_root))):
                structure.append(click.style(f'{indent}{os.path.basename(root)}/', fg="blue", bold=True))
                for file in files:
                    file_path = Path(root) / file
                    if not self.should_ignore(str(file_path.relative_to(self.project_root))):
                        structure.append(f'{subindent}{file}')
        
        return '\n'.join(structure)

    def generate_context(self):
        context = click.style(f"Project Root: {self.project_root}\n\n", fg="green", bold=True)
        context += click.style("Project Structure:\n", fg="cyan", underline=True)
        context += self.list_structure()
        context += click.style("\n\nFile Contents:\n", fg="cyan", underline=True)
        for file_path, content in self.context.items():
            context += click.style(f"\n--- {file_path} ---\n", fg="yellow", bold=True)
            context += content + "\n"
        return context

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = ContextManager()

@cli.command()
@click.argument('file_paths', nargs=-1, required=True, type=click.Path(exists=True))
@click.pass_obj
def add(ctx, file_paths):
    """Add one or more files to the context"""
    added = ctx.add_files(file_paths)
    if added:
        click.secho(f"Added {len(added)} file(s) to context:", fg="green")
        for file in added:
            click.echo(f"  - {file}")
    else:
        click.secho("No files were added to the context.", fg="yellow")

@cli.command()
@click.argument('file_paths', nargs=-1, required=True)
@click.pass_obj
def remove(ctx, file_paths):
    """Remove one or more files from the context"""
    removed = ctx.remove_files(file_paths)
    if removed:
        click.secho(f"Removed {len(removed)} file(s) from context:", fg="green")
        for file in removed:
            click.echo(f"  - {file}")
    else:
        click.secho("No files were removed from the context.", fg="yellow")

@cli.command()
@click.pass_obj
def drop(ctx):
    """Drop all the context of files"""
    ctx.drop_all()
    click.secho("Dropped all context", fg="green")

@cli.command()
@click.pass_obj
def ls(ctx):
    """List the file structure of the project"""
    structure = ctx.list_structure()
    click.echo(structure)

@cli.command()
@click.pass_obj
def generate(ctx):
    """Generate the context of all the files with the metadata of the file structure"""
    context = ctx.generate_context()
    click.echo(context)

@cli.command()
@click.confirmation_option(prompt="Are you sure you want to delete all llmcxt related files and dependencies?")
def delete():
    """Delete all llmcxt related files and dependencies"""
    try:
        # Remove the configuration file
        config_file = Path.cwd() / CONFIG_FILE
        if config_file.exists():
            config_file.unlink()
            click.secho(f"Removed {CONFIG_FILE}", fg="green")

        # Remove the package directory
        package_dir = Path(__file__).parent
        if package_dir.exists():
            shutil.rmtree(package_dir)
            click.secho(f"Removed package directory: {package_dir}", fg="green")

        # Uninstall the package
        os.system(f"pip uninstall -y llmcxt")
        click.secho("Uninstalled llmcxt package", fg="green")

        click.secho("llmcxt has been successfully removed from your system.", fg="blue", bold=True)
    except Exception as e:
        click.secho(f"An error occurred while deleting llmcxt: {str(e)}", fg="red")

if __name__ == '__main__':
    cli()