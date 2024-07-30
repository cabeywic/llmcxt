import pytest
from click.testing import CliRunner
from llmcxt.cli import cli

def test_cli_add():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test_file.txt', 'w') as f:
            f.write('Test content')
        result = runner.invoke(cli, ['add', 'test_file.txt'])
        assert result.exit_code == 0
        assert 'Added' in result.output

def test_cli_remove():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test_file.txt', 'w') as f:
            f.write('Test content')
        runner.invoke(cli, ['add', 'test_file.txt'])
        result = runner.invoke(cli, ['remove', 'test_file.txt'])
        assert result.exit_code == 0
        assert 'Removed' in result.output

def test_cli_generate():
    runner = CliRunner()
    result = runner.invoke(cli, ['generate'])
    assert result.exit_code == 0
    assert 'Project Root' in result.output