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
from jira import JIRA

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

auth = None
jira = ''
name_jira = ''
jira_project_key = 'SRE'
jira_company_url = 'https://YOURCOMPANY.atlassian.net'
jira_admin_password = '123456'
jira_admin_user = 'serviceadmin'
gh_scrap_user = 'kassyuz'
gh_scrap_token = '123456'
company_domain = '@xyz.com'

# Order 1
def GH_get_issues(name):
    print('Requests issues from GitHub API')
    url = 'https://api.github.com/repos/{}/issues?state=all'.format(name)
    r = gh_session.get(url)

    #write issues from the first page of Github
    write_issues(r)

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
            write_issues(r)
            if pages['next'] == pages['last']:
                print("Importation happended like a charm")
                break
    print("Importation happended like a charm")

# Order 2
def write_issues(r):
    print('Parses JSON response and writes it to JIRA.')
    if r.status_code != 200:
        raise Exception(r.status_code)
    
    for issue in r.json():
        if ('pull_request' not in issue):
            labels = ', '.join([l['name'] for l in issue['labels']])
            if (('no-jira' not in labels and 'open' in issue['state']) or ( 'jira' in labels and 'closed' in issue['state'])):
                date = issue['created_at'].split('T')[0]
                name_jira = get_JIRA_user_based_on_GH_user(issue['user']['login'])
                jira_issue_key = JIRA_create_issue(jira_project_key, issue['title'], issue['body'], 'Task', name_jira, issue['user']['login'], issue['html_url'], date)
                add_GH_comments_to_JIRA_issue(jira_issue_key, name_jira, issue['number'], issue['comments'])
                
# Order 3 
# You must create the dictionary of your team
def get_JIRA_user_based_on_GH_user(gh_name):
    print ('GH name >> '+gh_name)
    if gh_name == 'johnroe':
	    return 'john.roe'
    elif gh_name == 'kassyuz':
        return 'cassio.moreto'
    else:
        return ''

# Order 4
def JIRA_create_issue(project_key, summary, description, issue_type, name_jira, gh_username, gh_issue_url, createdAt):
    print('name_jira >> '+name_jira)
    if name_jira:
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description + '\n\n---\n *Original issue from Github*\n' + '[Created by _'+ name_jira +'_ at '+ createdAt +']\n Github link: ' + gh_issue_url,
            'issuetype': {'name': issue_type},
            'reporter': {
                'name': name_jira,
                'emailAddress': name_jira + your_company_domain'
            },
            'labels': ['imported-github']
        }
    else:
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description + '\n\n---\n *Original issue from Github*\n' + '[Created by _'+ gh_username +'_ at '+ createdAt +']\n Github link: ' + gh_issue_url,
            'issuetype': {'name': issue_type},
            'reporter': {
                'name': ''
            },
            'labels': ['imported-github']
        }
    
    new_issue = jira_session.create_issue(fields=issue_dict)
    print('JIRA issue successfully created. Issue ID >> '+new_issue.key)
    return new_issue.key

# order 5
def add_GH_comments_to_JIRA_issue(jira_issue_key, name_jira, gh_issue_number, comments_numbers):
    url = 'https://api.github.com/repos/{}/issues/{}/comments'.format(repo_name, gh_issue_number)
    r = gh_session.get(url)
    if comments_numbers > 0:
        if r.status_code != 200:
            raise Exception(r.status_code)
        print('Adding all Github comments from issue '+ repo_name +'/issues/'+ str(gh_issue_number) +' to '+ jira_issue_key +' JIRA issue')
        for comment in r.json():
            date = comment['created_at'].split('T')[0]
            JIRA_add_comment_from_GH_to_JIRA(jira_issue_key, comment['user']['login'], comment['body'], comment['html_url'], date)

# order 6
def JIRA_add_comment_from_GH_to_JIRA(jira_issue_key, name_jira, gh_comment, url_gh_comment, createdAt):
    comment = gh_comment + '\n\n---\n*Comment imported from Github*\n [Original made by _*'+ name_jira +'*_ at '+ createdAt +']\n Github link: ' + url_gh_comment
    jira_session.add_comment(jira_issue_key, comment)

parser = argparse.ArgumentParser(description="Write GitHub repository issues "
                                             "to CSV file.")
parser.add_argument('repositories', nargs='+', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed issues.")
args = parser.parse_args()

gh_session = requests.Session()
gh_session.auth = (gh_scrap_user, gh_scrap_token)

jira_session = JIRA(basic_auth=(jira_admin_user, jira_admin_password), options={'server':jira_company_url})

for repository in args.repositories:
    repo_name = repository
    GH_get_issues(repo_name)
