from jira.client import JIRA
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
Backlog = config.get("aliases", "Backlog")
InProgress = config.get("aliases", "inProgress")
Blocked = config.get("aliases", "Blocked")
Review = config.get("aliases", "Review")
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

args=parser.parse_args()

# Defines a function for connecting to Jira
def connect_jira(log, server, token):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        log.info("Connecting to JIRA: %s" % server)
        jira_options = {'server': server}
        jira = JIRA(options=jira_options, token_auth=(token))
        return jira
    except Exception as e:
        log.error("Failed to connect to JIRA: %s" % e)
        return None

# create logger
log = logging.getLogger(__name__)


def get_issues(project_name):
    jira = connect_jira(log, server, token)
    issue_table = PrettyTable(['Issue', 'Status', 'Description', 'Age'])
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
        print("Nothing assigned")

def main():
    if args.list:
        get_issues(base_project)
    if args.support:
        get_issues(support_project)


if __name__ == "__main__":
    main()