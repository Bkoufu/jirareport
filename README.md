<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About The Project](#about-the-project)
  * [Description](#description)
  * [Prerequisites](#prerequisites)
* [Usage](#usage)
* [License](#license)

<!-- ABOUT THE PROJECT -->
## About The Project
JIRA Issue Handler is a Python script that provides a CLI interface to handle JIRA issues. It allows users to update JIRA issues with new labels, create reports based on labels, and generate reports for specific queries.

### Description
JIRA Issue Handler is a Python script that provides a CLI interface to handle JIRA issues. It allows users to update JIRA issues with new labels, create reports based on labels, and generate reports for specific queries.

### Prerequisites
Before using the JIRA Issue Handler script, you should have the following:
* A virtual environment set up in your project directory.
* Python installed on your system.
* JIRA server URL, username, and password.

<!-- USAGE EXAMPLES -->
## Usage

To use the JIRA Issue Handler script, follow these steps:

1. Install the required packages using the following command:

2. Copy the `app.py` script to the root of your project directory.

3. Open your terminal.

4. Navigate to the directory where the `app.py` script is located.

5. Activate your virtual environment (if you have one set up).

6. Run `python app.py`.

7. Upon running the script, you will be prompted to select one of the following options:
* Update some tickets: Update some tickets with new labels. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, and project name.
* Export a report based on labels: Export a report based on issues with specific labels. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, and project name.
* Ask for other questions: Generate a report for specific queries. You will be asked to provide JIRA server URL, username, password, JIRA issue keys, new labels, reporter, assignee, and project name. You can choose one of the following reports:
  * Created vs Resolved report: A report that shows the number of issues created and resolved in a specific date range.
  * Resolution time and average age report: A report that shows the average time it took to resolve an issue and the average age of unresolved issues.
  * Monthly ticket count report: A report that shows the number of issues created and resolved each month.
  * Custom report: A report that shows the number of issues with specific labels, statuses, resolutions, and priorities.

<!-- LICENSE -->
## License
This script is licensed under the MIT License.
