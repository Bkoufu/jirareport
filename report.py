import requests
import json
from jira import JIRA
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

from collections import defaultdict
from datetime import datetime, timedelta
from complementary import _Cal_time_in_status
import numpy as np
from atlassian import Jira
import matplotlib.dates as mdates
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class JiraReport:
    def __init__(self,
                 server,
                 user ,
                 password,
                 issue_keys, 
                 reporter, 
                 Assignee,
                 new_labels, 
                 project_name):
        
        self.server = server
        self.user = user
        self.password = password
        self.issue_keys = issue_keys
        self.reporter = reporter
        self.Assignee = Assignee

        self.new_labels = new_labels
        self.project_name = project_name

        # https://jira.readthedocs.io/installation.html
        self.jira_35 = JIRA(self.server, basic_auth=(self.user, self.password))
        # https://atlassian-python-api.readthedocs.io/jira.html#get-issues-from-jql-search-result-with-all-related-fields
        self.jira = Jira(url=self.server,username=self.user,password=self.password)

        logging.info('you have successfully initialized your project with parameters inputed')

    def _get_data_from_jira(self, url):
        response = requests.get(url, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        return json.loads(response.text)

    def sprint_report(self, sprint_id):
        url = f"{self.base_url}/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={self.project_id}&sprintId={sprint_id}"
        return self._get_data_from_jira(url)

    def velocity_chart(self):
        url = f"{self.base_url}/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={self.project_id}"
        return self._get_data_from_jira(url)

    def risk_report(self):
        # Implement your custom risk report logic here
        pass

    def version_report(self, version_id):
        url = f"{self.base_url}/rest/greenhopper/1.0/version/{version_id}/relatedissue"
        return self._get_data_from_jira(url)

    def cumulative_flow_diagram(self):
        url = f"{self.base_url}/rest/greenhopper/1.0/rapid/charts/cumulativeflowdiagram?rapidViewId={self.project_id}"
        return self._get_data_from_jira(url)
    
    def all_projects_info(self):
        projects =self.jira.get_all_projects()
        project_names = []
        ticket_counts  = []
        
        for project in projects:
            project_names.append(project['key'])
            
            issues = self.jira.get_project_issues_count(project['key'])
            ticket_counts.append(issues)
            
        # 棒グラフを作成
        plt.bar(project_names, ticket_counts)

        # 軸ラベルとタイトルを追加
        plt.xlabel('Project Name')
        plt.ylabel('Number of Tickets')
        plt.title('Ticket Count by Project')
        # 縦向きにX軸ラベルを回転して表示
        plt.xticks(rotation=90)

        rotation_angle = 90
        rotation_transform = transforms.Affine2D().rotate_deg(rotation_angle)

        # 現在の軸に回転変換を適用
        plt.gca().set_transform(rotation_transform + plt.gca().transAxes)

        plt.savefig('ticket_count_by_project_rotated.png', bbox_inches='tight')
        plt.show()

    def monthly_data_report(self):

        new_labels = self.new_labels
        ProjectNM = ' '.join(self.project_name)

        data = {}

        #現在の年の各月を繰り返し処理
        current_year = datetime.now().year
        for month in range(1, 13):
            start_date = f'{current_year}-{month:02d}-01'
            if month == 12:
                end_date = f'{current_year}-{month:02d}-31'
            else:
                end_date = f'{current_year}-{month+1:02d}-01'

            jql = f'project = "{ProjectNM}" AND labels in ({", ".join(new_labels)}) AND created >= "{start_date}" AND created < "{end_date}"'
            tickets = self.jira_35.search_issues(jql)

            data[f'{current_year}-{month:02d}'] = len(tickets)

        x = list(data.keys())
        y = list(data.values())
        plt.bar(x, y)
        plt.xlabel('Months')
        plt.xticks(rotation=45)
        plt.ylabel('Ticket count')
        plt.title(f'Monthly created tickets for {ProjectNM} ({", ".join(new_labels)})')
        plt.show()

    #プロジェクトの課題の平均解決時間を計算
    def resolution_time_and_average_age_report(self):

        new_labels =self.new_labels
        ProjectNM  = ' '.join(self.project_name)  

        jql = f'project = "{ProjectNM}" AND labels in ({", ".join(new_labels)}) AND resolved is not EMPTY'
    
        response = self.jira.jql(jql)
        issues = response['issues']
        resolution_time_dict = {}
        num_issues = len(issues)
        #各課題の解決時間を計算し、週ごとにグループ化
        for issue in issues:
            created_date = datetime.strptime(issue['fields']['created'][:19], '%Y-%m-%dT%H:%M:%S')
            resolved_date = datetime.strptime(issue['fields']['resolutiondate'][:19], '%Y-%m-%dT%H:%M:%S')

            resolution_time_days = (resolved_date - created_date).days
            week_start = created_date - timedelta(days=created_date.weekday())
            week_end = week_start + timedelta(days=6)
            week_label = week_start.strftime('%Y-%m-%d')

            if week_label in resolution_time_dict:
                resolution_time_dict[week_label].append(resolution_time_days)
            else:
                resolution_time_dict[week_label] = [resolution_time_days]

        #各週の平均解決時間を計算
        weekly_resolution_times = {}
        for week_label, resolution_time_list in resolution_time_dict.items():
            weekly_resolution_times[week_label] = sum(resolution_time_list) / len(resolution_time_list)


        #データをリストに変換
        weeks = [datetime.strptime(week_label, '%Y-%m-%d') for week_label in weekly_resolution_times.keys()]
        resolution_times = list(weekly_resolution_times.values())

        fig, ax = plt.subplots()
        ax.plot(weeks, resolution_times, marker='o')
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
        fig.autofmt_xdate()

        plt.xlabel('Week')
        plt.ylabel('Average Resolution Time (days)')
        plt.title('Weekly Average Resolution Time')

        plt.show()

        #カレンダー週ごとに課題をグループ化する関数を作成
    def group_issues_by_week(self,issues, start_date, end_date):
        weekly_counts = defaultdict(int)

        for issue in issues:
            date = issue.fields.created if hasattr(issue.fields, "created") else issue.fields.resolved_date
            date = datetime.strptime(date[:10], "%Y-%m-%d")
            calendar_week = date.strftime("CW%U")

            if start_date <= date <= end_date:
                weekly_counts[calendar_week] += 1

        return weekly_counts
    
    def created_vs_resolved_reports(self,start_date,end_date):
            
            #日付範囲内に作成された課題および解決された課題を取得

            new_labels = self.new_labels   
            ProjectNM  = ' '.join(self.project_name)  

            start_date_formatted = start_date.strftime('%Y-%m-%d %H:%M')
            end_date_formatted = end_date.strftime('%Y-%m-%d %H:%M')

            jql_created = f'project = "{ProjectNM}" AND labels in ({", ".join(new_labels)}) AND created >= "{start_date_formatted}" AND created <= "{end_date_formatted}"'
            jql_resolved = f'project = "{ProjectNM}" AND labels in ({", ".join(new_labels)}) AND resolutiondate >= "{start_date_formatted}" AND resolutiondate <= "{end_date_formatted}"'


            jql_created = jql_created.format(
                new_labels=','.join(new_labels),
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )

            jql_resolved = jql_resolved.format(
                new_labels=','.join(new_labels),
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            issues_created = self.jira_35.search_issues(jql_created)
            issues_resolved = self.jira_35.search_issues(jql_resolved)

            # Group issues by week
            issues_created_weekly = self.group_issues_by_week(issues_created, start_date, end_date)
            issues_resolved_weekly = self.group_issues_by_week(issues_resolved, start_date, end_date)

            calendar_weeks = sorted(set(list(issues_created_weekly.keys()) + list(issues_resolved_weekly.keys())))

            x_axis = range(len(calendar_weeks))
            plt.bar(x_axis, [issues_created_weekly[week] for week in calendar_weeks], color='blue', label='Created')
            plt.bar(x_axis, [issues_resolved_weekly[week] for week in calendar_weeks], bottom=[issues_created_weekly[week] for week in calendar_weeks], color='green', label='Resolved')

            plt.title(f'Created vs. Resolved Report\nLabels {self.new_labels}\n{start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
            plt.xlabel('Calendar Week')
            plt.xticks(x_axis, calendar_weeks)
            plt.ylabel('Number of Issues')
            plt.legend()

            plt.savefig('created_vs_resolved_report_calendar_week.png', dpi=300, bbox_inches='tight')

            plt.show()


    def burndown_and_burnup_charts(self, sprint_id):
        burndown_url = f"{self.base_url}/rest/greenhopper/1.0/rapid/charts/scopechangeburndownchart?rapidViewId={self.project_id}&sprintId={sprint_id}"
        burnup_url = f"{self.base_url}/rest/greenhopper/1.0/rapid/charts/scopechangeburnupchart?rapidViewId={self.project_id}&sprintId={sprint_id}"
        return {
            'burndown': self._get_data_from_jira(burndown_url),
            'burnup': self._get_data_from_jira(burnup_url)
        }

