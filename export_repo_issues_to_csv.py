"""
Exports issues from a list of repositories to individual CSV files.
Uses OAuth authentication (Github token) to retrieve issues
from a repository that username has access to. Supports Github API v3.
Forked from: unbracketed/export_repo_issues_to_csv.py
"""
import argparse
import csv
import requests
import json

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

auth = None
state = 'open'


def write_issues(r, csvout):
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if 'pull_request' not in issue:
            labels = ', '.join([l['name'] for l in issue['labels']])
            date = issue['created_at'].split('T')[0]
            # Change the following line to write out additional fields
            csvout.writerow([labels,  issue['user']['login'], issue['number'], issue['title'], issue['body'], issue['state'], date,
                             issue['html_url']])


def get_issues(name):
    """Requests issues from GitHub API and writes to CSV file."""
    url = 'https://api.github.com/repos/{}/issues?state={}'.format(name, state)
    r = gh_session.get(url)
    csvfilename = '{}-issues.csv'.format(name.replace('/', '-'))
    with open(csvfilename, 'w') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['Labels', 'User-Git', 'Number', 'Title', 'Description', 'State', 'Date', 'URL'])
        write_issues(r, csvout)

        # Multiple requests are required if response is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = gh_session.get(pages['next'])
                print(pages['next'])
                write_issues(r, csvout)
                if pages['next'] == pages['last']:
                    print("CSV file was successfully created")
                    break

parser = argparse.ArgumentParser(description="Write GitHub repository issues "
                                             "to CSV file.")
parser.add_argument('repositories', nargs='+', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed issues.")
args = parser.parse_args()

if args.all:
    state = 'all'


user =  raw_input('Insert your Github user >> ')
token = raw_input('Insert your Github Token (read:org and repo permissions) >> ')

gh_session = requests.Session()
gh_session.auth = (user, token)

for repository in args.repositories:
    get_issues(repository)