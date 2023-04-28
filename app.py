from jira import JIRA
import argparse
import matplotlib.pyplot as plt
import os
import questionary
from prettytable import PrettyTable
import seaborn as sns
from report import JiraReport
from datetime import datetime, timedelta

# JIRAサーバーの認証資格情報
"""
jira_server2 = "************************"
jira_username = 'USER ID'
jira_password = 'Password'
"""

class IssueHandler:
    def __init__(self, server, user, password, project_name):
        # インスタンス変数を設定
        self.server = server
        self.user = user
        self.password = password
        self.project_name = project_name

        # JIRAオブジェクトを作成
        self.jira = JIRA(self.server, basic_auth=(self.user, self.password))

    def update_bug_report(self, issue_keys, new_labels):
        # ラベルを更新するメソッド
        for issue_key in issue_keys:
            issue = self.jira.issue(issue_key)
            issue.update(fields={'labels': new_labels})

            # ラベルが正常に更新されたかどうかを確認する
            if issue.fields.labels == new_labels:
                print(f"ラベルが正常に更新されました '{issue.key}'")
            else:
                print("ラベルの更新中にエラーが発生しました")

    def create_feature_request(self, title, description, priority):
        # 機能リクエストを作成するメソッド
        pass
    
    def create_support_ticket(self, title, description, priority):
        # サポートチケットを作成するメソッド
        pass
    
    def escalate_issue(self, issue_id, escalation_level):
        # サポートのレベルを上げるメソッド
        pass
    
    def close_issue(self, issue_id):
        # イシューをクローズするメソッド
        pass

    def create_report(self, issue_keys, new_labels):
        # 指定されたラベルを持つ全てのイシューを取得
        ProjectNM  = ' '.join(self.project_name)  
        jql = f'project = "{ProjectNM}" AND labels in ({", ".join(new_labels)})'
        issues = self.jira.search_issues(jql)

        # ラベルごとのカウント数を格納する辞書を作成
        label_counts = {
            'status': {
                'Open': 0,
                'In Progress': 0,
                'Blocked': 0,
                'Rejected': 0,
                'Fixed': 0,
                'Closed': 0
            },
            'resolution': {
                'Unresolved': 0,
                'Released': 0,
                'Rejected': 0,
                'Duplicate': 0,
                'Resolved': 0
            },
            'priority': {
                'High': 0,
                'Medium': 0,
                'Low': 0,
                'None': 0
            }
        }

        label_counts_all = {}
        for issue in issues:
            status = issue.fields.status.name
            resolution = issue.fields.resolution.name if issue.fields.resolution is not None else 'Unresolved'
            priority = issue.fields.priority.name
            label_counts['status'][status] += 1
            label_counts['resolution'][resolution] += 1
            label_counts['priority'][priority] += 1

            for label in issue.fields.labels:
                if label not in label_counts:
                    label_counts[label] = 0
                label_counts[label] += 1
                if label in new_labels:
                    if label not in label_counts_all:
                        label_counts_all[label] = 0
                    label_counts_all[label] += 1

        # 現在の作業ディレクトリを取得する
        cwd = os.getcwd()
        sns.set(style='whitegrid')

       # サブプロットのグリッドを作成する
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(20, 20))
        fig.subplots_adjust(hspace=0.3)

        # ステータスの円グラフ
        status_counts = {k: v for k, v in label_counts['status'].items() if v != 0}
        statuses = list(status_counts.keys())
        status_sizes = list(status_counts.values())
        axes[0, 0].pie(status_sizes, labels=statuses, autopct='%1.1f%%')
        #axes[0, 0].set_title('Issue Status Distribution', fontsize=14)
        axes[0, 0].axis('equal')
        #ステータスの分布のためのテーブルチャートを作成する
        table_data = []
        for status in statuses:
            count = status_counts[status]
            percentage = round(count/sum(status_counts.values())*100, 2)
            table_data.append([status, count, percentage])
        table_headers = ['Status', 'Issues', 'Percentage']
        table = PrettyTable(table_headers)
        table.title = 'Issue Status Distribution'
        for row in table_data:
            table.add_row(row)
        axes[0, 1].text(0, 1, str(table), va='top', family='monospace', fontsize=12)
        axes[0, 1].axis('off')

        resolution_counts = {k: v for k, v in label_counts['resolution'].items() if v != 0}
        resolutions = list(resolution_counts.keys())
        resolution_sizes = list(resolution_counts.values())
        axes[1, 0].pie(resolution_sizes, labels=resolutions, autopct='%1.1f%%')
        #axes[1, 0].set_title('Issue Resolution Distribution', fontsize=14)
        axes[1, 0].axis('equal')       

        #解決状況の分布のためのテーブルチャートを作成する
        table_data = []
        for resolution in resolutions:
            count = resolution_counts[resolution]
            percentage = round(count/sum(resolution_counts.values())*100, 2)
            table_data.append([resolution, count, percentage])
        table_headers = ['Resolution', 'Issues', 'Percentage']
        table = PrettyTable(table_headers)
        table.title = 'Issue Resolution Distribution'

        for row in table_data:
            table.add_row(row)
        axes[1, 1].text(0, 1, str(table), va='top', family='monospace', fontsize=12)
        axes[1, 1].axis('off')
        # Priority pie chart
        priority_counts = {k: v for k, v in label_counts['priority'].items() if v != 0}
        priorities = list(priority_counts.keys())
        priority_sizes = list(priority_counts.values())
        axes[2, 0].pie(priority_sizes, labels=priorities, autopct='%1.1f%%')
        #axes[2, 0].set_title('Issue Priority Distribution', fontsize=14)
        axes[2, 0].axis('equal')    

        for row in table_data:
            table.add_row(row)
        axes[1, 1].text(0, 1, str(table), va='top', family='monospace', fontsize=12)
        axes[1, 1].axis('off')
        # Priority pie chart
        priority_counts = {k: v for k, v in label_counts['priority'].items() if v != 0}
        priorities = list(priority_counts.keys())
        priority_sizes = list(priority_counts.values())
        axes[2, 0].pie(priority_sizes, labels=priorities, autopct='%1.1f%%')
        #axes[2, 0].set_title('Issue Priority Distribution', fontsize=14)
        axes[2, 0].axis('equal')

        #優先度の分布についてテーブルチャートを作成する
        table_data = []
        for priority in priorities:
            count = priority_counts[priority]
            percentage = round(count/sum(priority_counts.values())*100, 2)
            table_data.append([priority, count, percentage])
        table_headers = ['Priority', 'Issues', 'Percentage']
        table = PrettyTable(table_headers)
        table.title = 'Issue Priority Distribution'

        for row in table_data:
            table.add_row(row)
        axes[2, 1].text(0, 1, str(table), va='top', family='monospace', fontsize=12)
        axes[2, 1].axis('off')

        # Label pie chart
        label_counts_all = {k: v for k, v in label_counts_all.items() if v != 0}
        labels = list(label_counts_all.keys())
        label_sizes = list(label_counts_all.values())
        axes[3, 0].pie(label_sizes, labels=labels, autopct='%1.1f%%')
        #axes[3, 1].set_title('Issue Label Distribution', fontsize=14)
        axes[3, 0].axis('equal')

        #ラベルの分布に対するテーブルチャートを作成する
        table_data = []
        for label in labels:
            count = label_counts_all[label]
            percentage = round(count/sum(label_counts_all.values())*100, 2)
            table_data.append([label, count, percentage])
        table_headers = ['Label', 'Issues', 'Percentage']
        table = PrettyTable(table_headers)
        table.title = 'Issue Label Distribution'

        for row in table_data:
            table.add_row(row)
        axes[3, 1].text(0, 0.8, str(table), va='top', family='monospace', fontsize=12)
        axes[3, 1].axis('off')

        #チャートを画像として保存する
        fig.savefig(os.path.join(cwd, 'issue_distribution.png'))
        plt.show()
        print("All pie charts were generated successfully!")




def main():
    selection = questionary.select(
        "What do you want to do?",
        choices=[
            'update some tickes',
            'export a report based on lables',
            'Ask for other questions'
        ]).ask()  # returns value of selection

    if selection == 'update some tickes':
        print(f"you have selected  {selection} ,so please add arguments")

        """
        parser = argparse.ArgumentParser(description="JIRA issue handler")
        parser.add_argument("--server", required=True,  type=str, help="JIRA server URL")
        parser.add_argument("--user", required=True, help="JIRA usernames")
        parser.add_argument("--password", required=True, help="JIRA password")
        parser.add_argument("--issue_keys", required=True, nargs='+', type=str,help="JIRA issue key")
        parser.add_argument("--new_labels", required=True, nargs='+',type=str,help="new labels need to be updated")

        args = parser.parse_args()
        Issue_handler = IssueHandler(server=args.server, user=args.user, password=args.password)
        Issue_handler.update_bug_report(issue_keys=args.issue_keys,new_labels=args.new_labels)
        """
        server = input("Enter JIRA server URL: ")
        user = input("Enter JIRA username: ")
        password = input("Enter JIRA password: ")
        issue_keys = input("Enter JIRA issue keys (separated by spaces, this parameter is madatory): ").split()
        new_labels = input("Enter new labels (separated by spaces,this parameter is madatory): ").split()
        project_name = input("Enter JIRA project_name (it is mandatory): ").split()

        Issue_handler = IssueHandler(server=server, user=user, password=password,project_name=project_name)
        Issue_handler.update_bug_report(issue_keys=issue_keys, new_labels=new_labels)


    elif selection == 'export a report based on lables':
        server = input("Enter JIRA server URL: ")
        user = input("Enter JIRA username: ")
        password = input("Enter JIRA password: ")
        issue_keys = input("Enter JIRA issue keys (separated by spaces if you put , it could be optional): ").split()
        new_labels = input("Enter new labels (separated by spaces): ").split()
        project_name = input("Enter JIRA project_name (it is mandatory): ").split()

        Issue_handler = IssueHandler(server=server, user=user, password=password,project_name=project_name)

        Issue_handler.create_report(issue_keys=issue_keys, new_labels=new_labels)

    elif selection == 'Ask for other questions':
        server = input("Enter JIRA server URL: ")
        user = input("Enter JIRA username: ")
        password = input("Enter JIRA password: ")
        issue_keys = input("Enter JIRA issue keys (separated by spaces if you put , it could be optional): ").split()
        new_labels = input("Enter new labels (separated by spaces): ").split()
        reporter = input("Enter JIRA reporter : ")
        Assignee = input("Enter JIRA Assignee: ")

        project_name = input("Enter JIRA project_name (it is mandatory): ").split()

        ReporHander=JiraReport (server=server, 
                    user=user, 
                    password=password,
                    issue_keys=issue_keys, 
                    reporter =reporter, 
                    Assignee =Assignee,
                    new_labels=new_labels,
                    project_name=project_name)
        
        selection = questionary.select(
        "please choose what kind of report you want?",
        choices=[
            'Created vs Resolved report',
            'resolution_time_and_average_age_report',
            'Monthly ticket count report',
            'report'
            ]).ask()  # returns value of selection

        if selection == 'Created vs Resolved report':
            ("please provide the date range (default is 30 day report if you don't specify any date range)")
            # Get user input for date range
            start_date_input = input("Enter the start date (YYYY-MM-DD): ")
            end_date_input = input("Enter the end date (YYYY-MM-DD): ")

            if start_date_input !="" and end_date_input !="" :

                start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_input, "%Y-%m-%d")

                print(f'pareased date range  start_date:{start_date}')
                print(f'pareased date range end_date :{end_date}')
                ReporHander.created_vs_resolved_reports(start_date,end_date)
            else:
                
                start_date = datetime.now() - timedelta(days=30)
                end_date = datetime.now()
                ReporHander.created_vs_resolved_reports(start_date,end_date)

        elif selection == 'resolution_time_and_average_age_report':    
            print(f'print out the  resolution time and average age report, please wait!')
            ReporHander.resolution_time_and_average_age_report()
        
        elif selection == 'Monthly ticket count report':
            print(f'Monthly ticket count report it will generate the Jan. till current month, please wait!')
            ReporHander.monthly_data_report()
        elif selection == 'report':
            pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"please check your input values are correct  { e }")