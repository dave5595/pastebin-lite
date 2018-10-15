from home.models import Paste
from django.utils import timezone
from django.db.models import Q


# cant use Q(expiration_datetime__gt=timezone.now() to get if pastes is expired or not
# if paste is not expired and deleted, get it !
def get_queryset(self):
    return Paste.objects\
        .filter(deleted=False)\
        .filter(Q(expiration_datetime=None))\
        .get(char_id=self.kwargs['char_id'])
