from collections import defaultdict

import pygal
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from web.account.utils import is_manager, Chart
from web.issue.models import Issue, StatusChoices


class NumberOfIssueChart(Chart):

    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs, inner_radius=.4)
        self.chart.title = 'Number of Issues in each category'
        self.user = kwargs.get('user', None)

    def get_data(self):
        """
        Query the db for chart data, pack them into a dict and return it.
        """
        data = defaultdict(int)
        if is_manager(self.user):
            data["Resolved"] = Issue.objects.filter(manage_by=self.user, status=StatusChoices.RESOLVED).count()
            data["Review"] = Issue.objects.filter(manage_by=self.user, status=StatusChoices.REVIEW).count()
        else:
            data["Opened"] = Issue.objects.filter(created_by=self.user, status=StatusChoices.TODO).count()
            data["Resolved"] = Issue.objects.filter(created_by=self.user, status=StatusChoices.RESOLVED).count()
            data["In Review"] = Issue.objects.filter(created_by=self.user, status=StatusChoices.REVIEW).count()
        return data


class YearlyIssueChart(Chart):

    def __init__(self, **kwargs):
        self.chart = pygal.Bar(**kwargs, inner_radius=.4)
        self.chart.title = 'Last year History of issues'
        self.user = kwargs.get('user', None)

    def get_dates_for_chart(self):
        today = get_today_date()
        last_year = get_last_year_date(today)
        start_date_of_year = get_start_date_of_year(last_year)
        return today, last_year, start_date_of_year

    def get_x_labels_list(self):
        today, last_year, start_date_of_year = self.get_dates_for_chart()

        label_list = []
        for year in range(start_date_of_year.year, today.year + 1):
            if year < today.year:
                month = start_date_of_year.month
                limit = 12
            else:
                month = 1
                limit = today.month

            for month in range(month, limit + 1):
                label = f"{str(month)}/{str(year)}"
                label_list.append(label)

        return label_list

    def get_manager_data(self, monthly_assigned_issues_dict, monthly_resolved_issues_dict):
        data = defaultdict(list)
        today, last_year, start_date_of_year = self.get_dates_for_chart()
        for year in range(start_date_of_year.year, today.year + 1):
            if year < today.year:
                month = start_date_of_year.month
                limit = 12
            else:
                month = 1
                limit = today.month

            for month in range(month, limit + 1):
                number_of_assign_issues = 0
                number_of_resolve_issues = 0
                for monthly_count_dict in monthly_assigned_issues_dict:
                    if monthly_count_dict.get("assigned_at__month") == month and \
                            monthly_count_dict.get("assigned_at__year") == year:
                        number_of_assign_issues = monthly_count_dict.get('number_of_issues')

                for monthly_count_dict in monthly_resolved_issues_dict:
                    if monthly_count_dict.get("assigned_at__month") == month and \
                            monthly_count_dict.get("assigned_at__year") == year:
                        number_of_resolve_issues = monthly_count_dict.get('number_of_issues')

                data["Assigned"].append(number_of_assign_issues)
                data["Resolved"].append(number_of_resolve_issues)

        return data

    def get_customer_data(self, monthly_opened_issues_dict, monthly_resolved_issues_dict,
                          monthly_reviewed_issues_dict):

        data = defaultdict(list)

        today, last_year, start_date_of_year = self.get_dates_for_chart()

        for year in range(start_date_of_year.year, today.year + 1):
            if year < today.year:
                month = start_date_of_year.month
                limit = 12
            else:
                month = 1
                limit = today.month

            for month in range(month, limit + 1):
                number_of_opened_issues = 0
                number_of_resolve_issues = 0
                number_of_reviewed_issues = 0

                for monthly_count_dict in monthly_opened_issues_dict:
                    if monthly_count_dict.get("created_at__month") == month and \
                            monthly_count_dict.get("created_at__year") == year:
                        number_of_opened_issues = monthly_count_dict.get('number_of_issues')

                for monthly_count_dict in monthly_reviewed_issues_dict:
                    if monthly_count_dict.get("assigned_at__month") == month and \
                            monthly_count_dict.get("assigned_at__year") == year:
                        number_of_reviewed_issues = monthly_count_dict.get('number_of_issues')

                for monthly_count_dict in monthly_resolved_issues_dict:
                    if monthly_count_dict.get("assigned_at__month") == month and \
                            monthly_count_dict.get("assigned_at__year") == year:
                        number_of_resolve_issues = monthly_count_dict.get('number_of_issues')

                data["Opened"].append(number_of_opened_issues)
                data["Assigned"].append(number_of_resolve_issues)
                data["Reviewed"].append(number_of_reviewed_issues)

        return data

    def get_data(self):

        today, last_year, start_date_of_year = self.get_dates_for_chart()

        if is_manager(self.user):

            monthly_assigned_issues_dict = Issue.objects.filter(
                manage_by=self.user,
                assigned_at__range=(start_date_of_year, today)
            ).values(
                'assigned_at__month',
                'assigned_at__year'
            ).annotate(number_of_issues=Count('*')).order_by("-number_of_issues")

            monthly_resolved_issues_dict = Issue.objects.filter(
                manage_by=self.user,
                resolved_at__range=(start_date_of_year, today),
                status=StatusChoices.RESOLVED
            ).values(
                'resolved_at__month',
                'resolved_at__year'
            ).annotate(number_of_issues=Count('*')).order_by("-number_of_issues")

        else:

            monthly_opened_issues_dict = Issue.objects.filter(
                created_by=self.user,
                created_at__range=(start_date_of_year, today)
            ).values(
                'created_at__month',
                'created_at__year'
            ).annotate(number_of_issues=Count('*')).order_by("-number_of_issues")

            monthly_reviewed_issues_dict = Issue.objects.filter(
                created_by=self.user,
                assigned_at__range=(start_date_of_year, today)
            ).values(
                'assigned_at__month',
                'assigned_at__year'
            ).annotate(number_of_issues=Count('*')).order_by("-number_of_issues")

            monthly_resolved_issues_dict = Issue.objects.filter(
                created_by=self.user,
                assigned_at__range=(start_date_of_year, today),
                status=StatusChoices.RESOLVED
            ).values(
                'assigned_at__month',
                'assigned_at__year'
            ).annotate(number_of_issues=Count('*')).order_by("-number_of_issues")

        if is_manager(self.user):
            data = self.get_manager_data(monthly_assigned_issues_dict, monthly_resolved_issues_dict)
        else:
            data = self.get_customer_data(
                monthly_opened_issues_dict,
                monthly_resolved_issues_dict,
                monthly_reviewed_issues_dict
            )

        self.chart.x_labels = self.get_x_labels_list()
        return data


def get_start_date_of_year(last_year):
    return timezone.datetime(last_year.year, last_year.month, 1, tzinfo=timezone.utc)


def get_last_year_date(today):
    return today + relativedelta(years=-1)


def get_today_date():
    return timezone.localtime(timezone.now())


class TopManagersChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs, inner_radius=.4)
        self.chart.title = 'Top Three Managers Based on Issue Resolving'
        self.user = kwargs.get('user', None)

    def get_data(self):
        """
        Query the db for chart data, pack them into a dict and return it.
        """
        data = defaultdict(int)
        top_managers = Issue.objects.values('manage_by').annotate(count=Count('manage_by')).order_by("-count")[:3]
        for manager in top_managers:
            user = User.objects.get(id=manager["manage_by"])
            data[user.username] = manager["count"]

        return data
