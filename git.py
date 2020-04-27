from github import Github
from datetime import *
g = Github("29167964dd3bdcb30758a7ff7778fbe88e272b78")
user = g.get_user()
all_repos = user.get_repos()
grafana_repo = user.get_repo("customMetrics)



def get_commits_metrics():
        commits = grafana_repo.get_commits()
        additions = 0
        deletions = 0
        for commit in commits:
                additions = additions+commit.stats.additions
                deletions = deletions+commit.stats.deletions
        data=[
                 {
                        'columns':[
                                        {'text':'Modification','type':'string'},
                                        {'text':'Count','type':'number'}
                                ],
                        'rows':[
                                        ['Additions',additions],
                                        ['Deletions',deletions]
                                ],
                        'type':'table'
                } 
        ]
        return data



def get_commit_activity(target,number_of_weeks):

        stats_commit_activity = grafana_repo.get_stats_commit_activity()
        stats_commit_list = []
        for i in stats_commit_activity:
                stats_commit_list.append(i)
        stats_commit_list = stats_commit_list[-number_of_weeks:]
        week_commit_list = []
        for stats in stats_commit_list:
                week_commit_list.append(stats.days)
        today = datetime.combine(datetime.now().date(),time())
        datelist = [today - timedelta(days=x) for x in range(number_of_weeks*7)]
        datelist.sort()
        timestamps = [int(str(int(date.replace(tzinfo=timezone.utc).timestamp()))+'000') for date in datelist]
        timestamp_list = [timestamps[i:i + 7] for i in range(0, len(timestamps), 7)] 
        raw_data = [[week_commit_list[i][j],timestamp_list[i][j]] for i in range(len(timestamp_list)) for j in range(7)]
        data = [
                        {
                                'target':target,
                                'datapoints':raw_data
                        }
                ]
        return data
