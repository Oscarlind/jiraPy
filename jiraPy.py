from jira.client import JIRA, JIRAError
import logging
import argparse
import configparser
from prettytable import PrettyTable
import sys

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

# Creating parser
parser = argparse.ArgumentParser(prog='jiraPy',
                                 usage='%(prog)s [options] ',   
                                 description='Browse Jira through the terminal',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80))

# Arguments
parser.add_argument('-l', '--list', 
                    action='store_true',
                    help='List current issues')

parser.add_argument('-s', '--support', 
                    action='store_true',
                    help='List assigned support issues')
parser.add_argument('--status', 
                    action='store_true',
                    help='Print status for %s' % base_project)
parser.add_argument('-c', '--comment', 
                    nargs=2,
                    help='Comment selected issue')
parser.add_argument('-m', '--move', 
                    nargs=2,
                    metavar=('ISSUE', 'Review'),
                    help='Move selected issue')
parser.add_argument('-a', '--add', 
                    nargs='*',
#                    metavar=('[Issue]', '[Summary]', '[Description]'),
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
def connect_jira(log, server, token):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        log.info("Connected to: %s" % server)
        jira_options = {'server': server}
        jira = JIRA(options=jira_options, token_auth=(token))
        return jira
    except Exception as e:
        log.error("Failed to connect to JIRA: %s" % e)
        return None

# create logger
log = logging.getLogger("jiraPy")
#logging.basicConfig(level=logging.DEBUG)


def get_issues(project_name):
    jira = connect_jira(log, server, token)
    issue_table = PrettyTable(['Issue', 'Status', 'Description', 'Creation Date'])
    issues = jira.search_issues('assignee = currentUser() AND project = %s' %(project_name))
    for issue in issues:
        if Done in str(issue.fields.status):
            pass
        elif Closed in str(issue.fields.status):
            pass
        else:
            issue_table.add_row([issue, issue.fields.status, issue.fields.summary, issue.fields.created[:10]])
    if issue_table.rows:
        print(issue_table)
    else:
        print(f"Nothing assigned in project {project_name}")

def get_status():
    jira = connect_jira(log, server, token)
    status_table = PrettyTable(['Issue', 'Status', 'Description', 'Creation Date', 'Assignee'])
    issues = jira.search_issues('project = %s' %(base_project))
    for issue in issues:
        status_table.add_row([issue, issue.fields.status, issue.fields.summary, issue.fields.created[:10], issue.fields.assignee])
    print(status_table)

def add_comment(j_issue, comment):
    jira = connect_jira(log, server, token)
    try:
        jira.add_comment(j_issue, comment)
        print(f"The issue \033[1m {j_issue} \033[0m was commented with: \nComment: {comment}")
    except JIRAError:
        print(f"Could not add comment to {j_issue}")

        

def transition_issue(issue, w_flow):
    jira = connect_jira(log, server, token)
    print("Moving issue: %s to: %s" % (issue, args.move[1]))
    try:
        jira.transition_issue(issue, w_flow)
    except JIRAError:
        print(f"Issue: {args.move[0]} does not exist, try again")

def create_issue(summary, issue_type="Feil", description="Adding later"):
    jira = connect_jira(log, server, token)
    issue_dict = {
    'project': {'key': base_project},
    'summary': summary,
    'description': description,
    'issuetype': {'name': issue_type},
    'assignee': {'name': jira.current_user()}
}
    try:
        jira.create_issue(fields=issue_dict)
        print(f"Issue created with the following:\n\n Issue type: {issue_type}\n Summary: {summary}\n Description: {description}")
    except JIRAError as e:
        print(f"Could not create issue {args.add[0]} {e}")
    

def main():
    if args.list:
        get_issues(base_project)
    if args.support:
        get_issues(support_project)
    if args.status:
        get_status()
    if args.comment:
        add_comment(args.comment[0], args.comment[1])
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
        else:
            print("Contains too many arguments got: \n",', '.join(args.add))


if __name__ == "__main__":
    main()