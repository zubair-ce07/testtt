from .models import Ballot


def ballot_count(request):
    """
    Ballot count to be added in Requests, when user is authenticated will show in header.
    """
    count = Ballot.objects.get_active_ballots().count()
    return {"ballot_count": count}
