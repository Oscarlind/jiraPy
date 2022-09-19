# jiraPy

Simple CLI to browse and move assigned tasks

## How to use
Simple CLI with two arguments.

`-l or --list` to list current, non-completed issues

`-s or --support` to list assigned support cases

`-m or --move` to change status of the issue. E.g. to Review

E.g.

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