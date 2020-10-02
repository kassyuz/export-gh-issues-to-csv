# Export issues from Github Issues to JIRA Cloud

Exports issues from Github Issues directly to JIRA Cloud projects. Uses OAuth authentication (Github token) to retrieve issues from a Github repository that username has access to. Supports Github API v3.

## Fork and based
Forked from: [unbracketed/export_repo_issues_to_csv.py](https://gist.github.com/unbracketed/3380407)

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

## Preparing your Github Issues Pre-requirements

For all OPENED issues:
- All opened issue will be imported
- The label `no-jira` will exclude these/those particular issues from the migration

For all CLOSED issues:
- By default all closed issues will NOT be imported
- If you want to import a closed issues, it must be labeled with `jira` Label
