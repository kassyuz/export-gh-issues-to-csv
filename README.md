# Export repo issues to CSV

Exports issues from a list of repositories to individual CSV files. Uses OAuth authentication (Github token) to retrieve issues from a repository that username has access to. Supports Github API v3.

## Fork
Forked from: [unbracketed/export_repo_issues_to_csv.py](https://gist.github.com/unbracketed/3380407)

## Usage

### Requeriments
- Python 2.7
- Valid Github token with `read:org` and `repo` permissions

How to generate [Github tokens](https://github.com/settings/tokens)

### Commands

~~~~
python export_repo_issues_to_csv.py --all <organisation name or username>/<repo name>
~~~~

e.g.

~~~~
python export_repo_issues_to_csv.py --all kassyuz/export-gh-issues-to-csv
~~~~

Parameter `--all` will get all issues, opened and closed issues. The default is only `open` issues.

## CSV file

It will generate a CSV file called `<organisation name or username>/<repo name>-issues.csv`

e.g.
`kassyuz/export-gh-issues-to-csv-issues.csv`