from django.contrib.auth.models import Group


def get_group(name):
    return Group.objects.get(name=name)


def is_manager(user):
    group = user.groups.first()
    if group and group.name == 'Manager':
        return True

    return False


def is_manager_admin(user):
    group = user.groups.first()
    if group and group.name == 'ManagerAdmin':
        return True

    return False


def get_group_name(user):
    group = user.groups.first()
    return group.name if group else None


class Chart:

    def get_data(self):
        raise NotImplementedError()

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
