from .models import Ballot


def ballot_count(request):
    count = Ballot.objects.get_active_ballots().count()
    return {"ballot_count": count}
