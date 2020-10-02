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
python export-gh-issues-to-jira-with-comments.py <organisation name or username>/<repo name>

~~~~

e.g.

~~~~
python export-gh-issues-to-jira-with-comments.py kassyuz/this-repo
~~~~

## Github Issues Pre-requirements

For all OPENED issues:
- Those will be imported
- The label `no-jira` will exclude these/those particular issues from the migration

For all CLOSED issues:
- By default those issues will NOT ne imported
- If you want to import a closed issues, it must be labeled with `jira` Label