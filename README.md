# jiraPy

Simple CLI to browse assigned tasks

## How to use
Simple CLI with two arguments.
-l or --list to list current, non-completed issues
-s or --support to list assigned support cases

E.g.

```bash
(⎈ |ocp-lab1:default)$ python jiraPy.py --list
+---------------+-----------+----------------------------------------------+------------+
|     Issue     |   Status  |                 Description                  |    Age     |
+---------------+-----------+----------------------------------------------+------------+
| BASEPLATT-671 |   Review  | Server tar inte alltid sin DHCP reservation  | 2022-09-09 |
| BASEPLATT-661 | Blokkert  | Testa full installation lab2 (Automatiserad) | 2022-09-06 |
+---------------+-----------+----------------------------------------------+------------+

(⎈ |ocp-lab1:default)$ python jiraPy.py --support
Nothing assigned
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
Backlog: 
InProgress: 
Blocked: 
Review: 
Done: 
Closed: 
```