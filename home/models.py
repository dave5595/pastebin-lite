from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.db.models import Q
from gen_utils import generate_random_char_id

class Paste (models.Model):
    # Expiration
    NEVER = "never"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1month"

    char_id = models.CharField(max_length=8, db_index=True)
    title = models.CharField(max_length=128)
    expiration_datetime = models.DateTimeField(null=True, blank=True)
    hits = models.IntegerField(db_index=True, default=0)
    text = models.TextField(max_length=100000, default="")
    deleted = models.BooleanField(default=False)
    submitted = models.DateTimeField(auto_now_add=True, db_index=True)

    def add_paste(self, text, title="Untitled", expiration=None):
        self.char_id = generate_random_char_id(8)
        self.title = title
        self.text = text
        self.hits = 0

        if expiration != Paste.NEVER and expiration != None:
            self.expiration_datetime = self.get_new_expiration_datetime(expiration)
        else:
            self.expiration_datetime = None

        if Paste.objects.filter(char_id=self.char_id).exists():
            raise RuntimeError("A duplicate char ID was generated. Consider participating in a lottery instead.")

        # should probably wrap this in a try/except to handle any error during transactions in a real application
        with transaction.atomic():
            self.save()
        return self.char_id

    def get_pastes(self, include_expired=False, count=10):
        # sort the list descending order to display latest paste
        pastes = Paste.objects.filter(deleted=False).order_by("-submitted")
        if not include_expired:
            current_datetime = timezone.now()
            pastes = pastes.filter(Q(expiration_datetime__isnull=True) | Q(expiration_datetime__gte=current_datetime))[:count]
        return pastes

    def get_pastes_by_query_string(self, include_expired=False, query='',):
        pastes = Paste.objects.filter(deleted=False)
        if not include_expired:
            current_datetime = timezone.now()
            pastes = pastes\
                .filter(Q(expiration_datetime__isnull=True) | Q(expiration_datetime__gte=current_datetime))\
                .filter(title__icontains= query)
        return pastes

    def get_paste_by_id(self, include_expired=False, char_id=None):
        pastes = Paste.objects.filter(deleted=False)
        if not include_expired:
            current_datetime = timezone.now()
            non_expired_pastes = pastes.filter(Q(expiration_datetime__isnull=True) | Q(expiration_datetime__gte=current_datetime))
            paste = non_expired_pastes.get(char_id=char_id)
            return paste

    def delete_paste(self):
        with transaction.atomic():
            self.deleted = True
            self.save()
        return True

    def get_new_expiration_datetime(self, expiration):
        exp_datetime = timezone.now()

        if expiration == self.FIFTEEN_MINUTES:
            exp_datetime += timezone.timedelta(minutes=15)
        elif expiration == self.ONE_HOUR:
            exp_datetime += timezone.timedelta(hours=1)
        elif expiration == self.ONE_DAY:
            exp_datetime += timezone.timedelta(hours=24)
        elif expiration == self.ONE_WEEK:
            exp_datetime += timezone.timedelta(weeks=1)
        elif expiration == self.ONE_MONTH:
            exp_datetime += timezone.timedelta(hours=24 * 31)  # Assume one month means 31 days
        return exp_datetime

    def increment_hits(self):
        self.hits += 1
        self.save()
        return True

