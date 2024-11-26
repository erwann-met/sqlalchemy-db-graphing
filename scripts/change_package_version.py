""" Script used to change the version of the package in every relevant file."""

import sys
import re
from pathlib import Path
from datetime import datetime

def update_version_in_file(filepath, pattern, replacement):
    """Updates the version in the specified file."""
    content = filepath.read_text()
    updated_content = re.sub(pattern=pattern, repl=replacement, string=content, flags=re.MULTILINE)
    filepath.write_text(updated_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python change_package_version.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]

    # Regex patterns to match the version in the files
    version_pattern_init = '(__version__\s*=\s*")[^"]+(")'
    version_pattern_pyproject = '(version\s*=\s*")[^"]+(")'
    version_pattern_changelog = '## \[Unreleased\]'
    version_pattern_readme = "# Sqlalchemy DB graphing tool version [0-9.]+"

    # Update __init__.py
    setup_path = Path(".") / "src" / "sqlalchemy_db_graphing" / "__init__.py"
    update_version_in_file(
        filepath=setup_path,
        pattern=version_pattern_init,
        replacement=f'__version__ = "{new_version}"'
    )
    print(f"Version updated to {new_version} in __init__.py.")

    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    update_version_in_file(
        filepath=pyproject_path,
        pattern=version_pattern_pyproject,
        replacement=f'version = "{new_version}"'
    )
    print(f"Version updated to {new_version} in setup.py and pyproject.toml.")

    # Update ChangeLog
    changelog_path = Path("CHANGELOG.md")
    changelog_replacement = f"## [Unreleased]\n\n## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}"
    # First check that the version is not already in the file
    if re.search(f"## \[{new_version}\]", changelog_path.read_text()):
        print(f"Version {new_version} is already in the changelog. Skipping update.")
    else:
        update_version_in_file(
            filepath=changelog_path,
            pattern=version_pattern_changelog,
            replacement=changelog_replacement,
        )
        print(f"Version updated to {new_version} in CHANGELOG.MD.")

    # Update README.md
    readme_path = Path("README.md")
    update_version_in_file(
        filepath=readme_path,
        pattern=version_pattern_readme,
        replacement=f"# Sqlalchemy DB graphing tool version {new_version}"
    )
    print(f"Version updated to {new_version} in README.md.")

if __name__ == "__main__":
    main()
