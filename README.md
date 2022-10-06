# jiraPy

Simple CLI to browse and move assigned tasks

## How to use
Simple CLI with two arguments.

`-l or --list` to list current, non-completed issues

`-s or --support` to list assigned support cases

`-m or --move` to change status of the issue. E.g. to Review

`-c or --comment` read a issues description and comments or comment on the selected issue"

`-a or --add` add an issue. Accepts up to four arguments. Only the first is required with the rest being optional.

E.g. `jiraPy -a "Summary" "Task" "Description "Assignee"`


For example

```bash
(⎈ |ocp-svc:base)$ jiraPy --list
+---------------+-----------+----------------------------------------------+---------------+
|     Issue     |   Status  |                 Description                  | Creation Date |
+---------------+-----------+----------------------------------------------+---------------+
| BASEPLATT-714 |   Review  |      Boot order och rensning av diskar       |   2022-09-16  |
| BASEPLATT-661 | Blokkert  | Testa full installation lab2 (Automatiserad) |   2022-09-06  |
+---------------+-----------+----------------------------------------------+---------------+

(⎈ |ocp-svc:base)$ jiraPy.py --support
Nothing assigned

(⎈ |ocp-svc:base)$ jiraPy -m BASEPLATT-714 Review
Moving issue: BASEPLATT-714 to: Review 

(⎈ |ocp-svc:reelle)$ jiraPy -a "Summary" Oppgave "Description" extsfp
==================================
Issue created with the following:

 Issue type: Oppgave
 Summary: Summary
 Description: Description
 Assignee: extsfp

(⎈ |ocp-svc:reelle)$ jiraPy -c BASEPLATT-791 "This is a comment"
The issue  BASEPLATT-791  was commented with: 
Comment: This is a comment

(⎈ |ocp-svc:reelle)$ jiraPy -c BASEPLATT-791
Description:

 Description
===============================================================================
1. Comment:
This is a comment

 Author: Lindholm, Oscar
 Date: 2022-10-06

===============================================================================
2. Comment:
This is a another comment

 Author: Lindholm, Oscar
 Date: 2022-10-06


```
## Setting up 
Populate the config.ini file appropriately for your environment.

```ini
[variables]
server: <URL to your JIRA> 
token: <Authentication token>
base_project: <Main project for work>
support_project: <Project used for support cases>

# I often use non-english Jira versions. This is for keeping the script the same
[aliases]
Done: 
Closed: 
```