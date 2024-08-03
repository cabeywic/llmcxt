import click
import pyperclip
from pathlib import Path
from .core.file_manager import LocalFileManager
from .core.ignore_manager import IgnorePatternManager
from .core.config_manager import ConfigManager
from .core.context_manager import ContextManager
from .utils.helpers import strip_ansi_codes, ProjectRootFinder

@click.group()
@click.pass_context
def cli(ctx):
    project_root = ProjectRootFinder.find_project_root()
    file_manager = LocalFileManager()
    ignore_manager = IgnorePatternManager(project_root)
    ignore_manager.load_ignore_file()
    config_manager = ConfigManager(project_root, file_manager)
    ctx.obj = ContextManager(project_root, file_manager, ignore_manager, config_manager)

@cli.command()
@click.argument('file_paths', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, help="Add directories recursively")
@click.pass_obj
def add(ctx, file_paths, recursive):
    """Add one or more files or directories to the context"""
    try:
        added = ctx.add_files(file_paths, recursive=recursive)
        
        files_added = [f for f in added if Path(f).is_file()]
        dirs_added = [d for d in added if Path(d).is_dir()]
        
        if files_added:
            click.secho(f"Added {len(files_added)} file(s) to context:", fg="green")
            for file in files_added:
                click.echo(f"  - {file}")
        
        if dirs_added:
            click.secho(f"Added contents of {len(dirs_added)} director{'y' if len(dirs_added) == 1 else 'ies'} to context:", fg="green")
            for dir in dirs_added:
                click.echo(f"  - {dir}")
        
        if not added:
            click.secho("No files were added to the context.", fg="yellow")
    
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red")
    
    click.echo("\nCurrent context:")
    for file in ctx.get_context_files():
        click.echo(f"  - {file}")
        
@cli.command()
@click.argument('file_paths', nargs=-1, required=True)
@click.pass_obj
def remove(ctx, file_paths):
    """Remove one or more files from the context"""
    try:
        removed = ctx.remove_files(file_paths)
        click.secho(f"Removed {len(removed)} file(s) from context:", fg="green")
        for file in removed:
            click.echo(f"  - {file}")
    except Exception as e:
        click.secho(str(e), fg="red")
    
    click.echo("\nCurrent context:")
    for file in ctx.get_context_files():
        click.echo(f"  - {file}")

@cli.command()
@click.option('--clipboard', is_flag=True, help="Copy the generated context to clipboard")
@click.pass_obj
def generate(ctx, clipboard):
    """Generate the context of all the files with the metadata of the file structure"""
    context = ctx.generate_context()
    click.echo(context)
    
    if clipboard:
        clean_context = strip_ansi_codes(context)
        pyperclip.copy(clean_context)
        click.secho("Context copied to clipboard!", fg="green")

@cli.command()
@click.pass_obj
def context(ctx):
    """Show the current context (file paths)"""
    files = ctx.get_context_files()
    if files:
        click.secho("Current context:", fg="green")
        for file in files:
            click.echo(f"  - {file}")
    else:
        click.secho("No files in the current context.", fg="yellow")

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
@click.confirmation_option(prompt="Are you sure you want to delete all llmcxt related files and dependencies?")
def delete():
    """Delete all llmcxt related files and dependencies"""
    # Implementation remains the same as before
    ...

if __name__ == '__main__':
    cli()