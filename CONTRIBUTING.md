# Contributing to `sqlalchemy_db_graphing`


Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/erwann-met/sqlalchemy_db_graphing/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/erwann-met/sqlalchemy_db_graphing/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome!

## Get Started!

Ready to contribute? Here's how to set up `sqlalchemy_db_graphing` for local development.

1. Fork the `sqlalchemy_db_graphing` repo on GitHub.
2. Clone your fork locally::

```bash
git clone git@github.com:your_name_here/sqlalchemy_db_graphing.git
cd sqlalchemy_db_graphing/
```

3. Install your local copy into a virtualenv.

```bash
python -m venv venv
source venv/bin/activate
pip install -U pip wheel setuptools
pip install -e ".[dev]"
```

Install tox the pre-commit tool which wil run automated reformating to your code upon commit:
```bash
pip install tox pre-commit
pre-commit install
```

Run pre-commit once to install all pre-commit hooks:

```bash
pre-commit
```

4. Create a branch for local development::

```bash
git checkout -b name-of-your-bugfix-or-feature
```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linters and the
   tests:

```bash
tox -e py
tox -e ruff
tox -e black
tox -e mypy
```

6. Commit your changes and push your branch to GitHub::

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

7. Submit a pull request through the GitHub website.
