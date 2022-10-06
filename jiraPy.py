from jira.client import JIRA, JIRAError
import argparse
import configparser
from prettytable import PrettyTable
import sys
import textwrap

# Loading configuration
config = configparser.ConfigParser()
config.read("/usr/local/bin/jiraPy/config.ini")
server = config.get("variables", "server")
token = config.get("variables", "token")
base_project = config.get("variables", "base_project")
support_project = config.get("variables", "support_project")
# Aliases - need cleanup
Done = config.get("aliases", "Done")
Closed = config.get("aliases", "Closed")
# Text formatting
BOLD = '\033[1m'
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'
ENDC = '\033[0m'
FAIL = '\033[91m'

# Creating parser
parser = argparse.ArgumentParser(prog='jiraPy',
                                 usage='%(prog)s [options] ',   
                                 description='Browse Jira through the terminal',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80))

# Arguments (Add Inspect issue - to read the description of the task etc)
parser.add_argument('-l', '--list', 
                    action='store_true',
                    help='List current issues')

parser.add_argument('-s', '--support', 
                    action='store_true',
                    help='List assigned support issues')
parser.add_argument('-c', '--comment', 
                    nargs='*',
                    help='Comment selected issue')
parser.add_argument('-m', '--move', 
                    nargs=2,
                    metavar=('ISSUE', 'Review'),
                    help='Move selected issue')
parser.add_argument('-a', '--add', 
                    nargs='*',
                    help='Create a new issue')

args=parser.parse_args()

# You will need to identify the codes
# that are valid for you. Check: https://jira.readthedocs.io/examples.html#transitions
wflow_dict = {'Backlog': 11,
             'Doing': 31,
             'Done': 41,
             'Review': 61,
             'Blocked': 71,
             'Rejected': 81
             }

# Defines a function for connecting to Jira
def connect_jira(server, token):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        jira_options = {'server': server}
        jira = JIRA(options=jira_options, token_auth=(token))
        return jira
    except Exception as e:
        print("Could not connect to the server")
        return None

# Set the jira globally
jira = connect_jira(server, token)

def get_issues(project_name):
    issue_table = PrettyTable(['Issue', 'Type', 'Status', 'Description', 'Creation Date'])
    issues = jira.search_issues('assignee = currentUser() AND project = %s' %(project_name))
    for issue in issues:
        if Done in str(issue.fields.status):
            pass
        elif Closed in str(issue.fields.status):
            pass
        else:
            issue_table.add_row([issue, issue.fields.issuetype, issue.fields.status, issue.fields.summary, issue.fields.created[:10]])
    if issue_table.rows:
        print(issue_table)
    else:
        print(f"Nothing assigned in project {project_name}")

def add_comment(j_issue, comment=""):
    if not comment:
        comment_count = 1
        try:
            issue = jira.issue(j_issue)
            comments = issue.fields.comment.comments
            if issue.fields.description is not None:
                print(f"{OKGREEN}Description:{ENDC}\n\n",textwrap.fill(issue.fields.description, 79))
            for comment in comments:
                print("=" *79)
                print(f"{comment_count}. {OKCYAN}Comment:{ENDC}")
                print(f"{textwrap.fill(comment.body, 79)}\n\n Author: {comment.author.displayName}\n Date: {comment.created[:10]}\n")
                comment_count = comment_count + 1
        except JIRAError:
            print(f"{FAIL}ERROR:{ENDC} Could not read {j_issue}, The issue was not found")
    else:
        try:
            jira.add_comment(j_issue, comment)
            print(f"The issue {BOLD} {j_issue} {ENDC} was commented with: \n{OKCYAN}Comment:{ENDC} {comment}")
        except JIRAError:
            print(f"{FAIL}ERROR:{ENDC} Could not add comment to {j_issue}")

def transition_issue(issue, w_flow):
    print("Moving issue: %s to: %s" % (issue, args.move[1]))
    try:
        jira.transition_issue(issue, w_flow)
    except JIRAError:
        print(f"Issue: {args.move[0]} does not exist, try again")

# Note that custom fields are specific for the environment etc. Inspect the code on your browser to see
# What values are relevant.
def create_issue(summary, issue_type="Feil", description="Adding later", assignee=jira.current_user()):
    issue_dict = {
    'project': {'key': base_project},
    'summary': summary,
    'description': description,
    'issuetype': {'name': issue_type},
    'assignee': {'name': assignee},
    'customfield_17400': {'value': 'OpenShift'}
}
    try:
        jira.create_issue(fields=issue_dict)
        print("=" *34) # Character length of the first line in the following row.
        print(f"Issue created with the following:\n\n Issue type: {issue_type}\n Summary: {summary}\n Description: {description}\n Assignee: {assignee}")
    except JIRAError as e:
        print(f"{FAIL}Error{ENDC} Could not create issue {args.add[0]} {e}")
    

def main():
    if args.list:
        get_issues(base_project)
    if args.support:
        get_issues(support_project)
    if args.status:
        get_status()
    if args.comment:
        if len(args.comment) == 2:
            add_comment(args.comment[0], args.comment[1])
        elif len(args.comment) == 1:
            add_comment(args.comment[0])
        else:
            print("Contains too many arguments got: \n",', '.join(args.comment))
    if args.move:
        if args.move[1] in wflow_dict:
            transition_issue(args.move[0], wflow_dict[args.move[1]])
        else:
            print(f"Error, {args.move[1]} not recognized")
    if args.add:
        if len(args.add) < 2:
            create_issue(args.add[0])
        elif len(args.add) == 2:
            create_issue(args.add[0], args.add[1])
        elif len(args.add) == 3:
            create_issue(args.add[0], args.add[1], args.add[2])
        elif len(args.add) == 4:
            create_issue(args.add[0], args.add[1], args.add[2], args.add[3])
        else:
            print("Contains too many arguments got: \n",', '.join(args.add))


if __name__ == "__main__":
    main()