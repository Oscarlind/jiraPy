from jira.client import JIRA, JIRAError
import logging
import argparse
import configparser
from prettytable import PrettyTable

# Loading configuration
config = configparser.ConfigParser()
config.read("config.ini")
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
parser.add_argument('-m', '--move', 
                    nargs=2,
                    metavar=('ISSUE', 'Review'),
                    help='Move selected issue')

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

def transition_issue(issue, w_flow):
    jira = connect_jira(log, server, token)
    log.info("Moving issue: %s to: %s" % (issue, args.move[1]))
    try:
        jira.transition_issue(issue, w_flow)
    except JIRAError:
        print(f"Issue: {args.move[0]} does not exist, try again")

def main():
    if args.list:
        get_issues(base_project)
    if args.support:
        get_issues(support_project)
    if args.move:
        if args.move[1] in wflow_dict:
            transition_issue(args.move[0], wflow_dict[args.move[1]])
        else:
            print(f"Error, {args.move[1]} not recognized")

if __name__ == "__main__":
    main()