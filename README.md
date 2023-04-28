JIRA Issue Handler
This script provides a CLI interface to handle JIRA issues, such as updating issues with new labels, creating reports based on labels, and generating a report for specific queries.

Prerequisites
Before running the script, the following packages should be installed on your system:

JIRA
Matplotlib
Seaborn
PrettyTable
Questionary
You can install these packages by running the following command:

python
Copy code
pip install jira matplotlib seaborn prettytable questionary
How to use
To use the script, run python jira_issue_handler.py in the terminal.

Upon running the script, you will be prompted to select one of the following options:

Update some tickes: Update some tickets with new labels. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, and project name.

Export a report based on lables: Export a report based on issues with specific labels. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, and project name.

Ask for other questions: Generate a report for specific queries. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, reporter, assignee, and project name. You can choose one of the following reports:

Created vs Resolved report: A report that shows the number of issues created and resolved in a specific date range.

Resolution time and average age report: A report that shows the average time it took to resolve an issue and the average age of unresolved issues.

Monthly ticket count report: A report that shows the number of issues created and resolved each month.

Custom report: A report that shows the number of issues with specific labels, statuses, resolutions, and priorities.

License
This script is licensed under the MIT License.