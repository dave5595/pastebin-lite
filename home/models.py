from django.db import models, transaction
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import hashlib
import random
import string

# TODO: create user
# TODO: read up on django caching

class PasteManager(models.Manager):
    """
    Handles retrieving multiple pastes
    """

    def get_pastes(self, user=None, include_expired=False, include_hidden=True, count=30, offset=0):
        """
        Get pastes, optionally filtering by user and starting from a provided offset

        If count is None, -1 or "all", retrieve all records
        By default only 30 entries are retrieved
        """
        pastes = Paste.objects.filter(removed=Paste.NO_REMOVAL).order_by("-submitted")

        if user != None:
            pastes = pastes.filter(user=user)

        if not include_expired:
            current_datetime = timezone.now()
            pastes = pastes.filter(Q(expiration_datetime__isnull=True) | Q(expiration_datetime__gte=current_datetime))

        if not include_hidden:
            pastes = pastes.filter(hidden=False)

        start = offset
        end = offset + count

        pastes = pastes[start:end]

        return pastes

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
    # Is the paste removed (removed from view but not deleted)
    text = models.TextField(max_length=100000, default="TEXT")
    deleted = models.BooleanField(default=False)
    submitted = models.DateTimeField(auto_now_add=True, db_index=True)

    def add_paste(self, text, user=None, title="Untitled", expiration=None):
        """Add paste with the provided title and text
        Returns the paste's char ID if the paste was successfully added, False otherwise"""
        self.char_id = self.generate_random_char_id()
        self.title = title
        self.text = text

        if expiration != Paste.NEVER and expiration != None:
            self.expiration_datetime = self.get_new_expiration_datetime(expiration)
        else:
            self.expiration_datetime = None

        # Generating a duplicate char ID is extremely unlikely, but let's check for that to be sure
        # eg. in case we don't have enough entropy and we start generating the same strings,
        # in which case it's probably better to stop than continue
        if Paste.objects.filter(char_id=self.char_id).exists():
            raise RuntimeError("A duplicate char ID was generated. Consider participating in a lottery instead.")

        # Add paste in a transaction
        with transaction.atomic():
            self.save()
        # return self.char_id
        return self

    def delete_paste(self):
        """
        Mark the paste as deleted
        """
        with transaction.atomic():
            self.deleted = True
        return True

    def get_new_expiration_datetime(self, expiration):
        """
        Take the current datetime and move it forward by the given timedelta,
        giving us the paste's expiration date
        """
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

    def save(self, *args, **kwargs):
        """Override the save method to also save the result to cache"""
        super(Paste, self).save(*args, **kwargs)
        cache.set("paste:%s" % self.char_id, self)

    def get_hit_count(self):
        """
        Get hit count for the paste
        """
        con = get_redis_connection("persistent")

        result = con.get("paste:%s:hits" % self.id)

        if result == None:
            return 0
        else:
            return int(result)

    def add_hit(self, ip_address):
        """
        Add a hit by an IP address if it hasn't been added yet
        """
        con = get_redis_connection("persistent")

        if con.get("paste:%s:hit:%s" % (self.char_id, ip_address)):
            hits = con.get("paste:%s:hits" % self.char_id)
            if hits == None:
                return 0
            else:
                return int(hits)
        else:
            # Add an entry for this hit and store it for 24 hours
            con.setex("paste:%s:hit:%s" % (self.char_id, ip_address), 86400, 1)
            return con.incr("paste:%s:hits" % self.char_id)

    @staticmethod
    def is_expired(self):
        """
        Check if the paste has expired

        If paste has an expiration date and has expired, return True
        Otherwise return False
        """
        if self.expiration_datetime == None:
            return False

        current_datetime = timezone.now()

        if self.expiration_datetime < current_datetime:
            return True
        else:
            return False

    @staticmethod
    def is_removed(self):
        """
        Has the paste been removed (paste still exists but can't be viewed),
        usually due to a paste report
        """
        if self.removed > 0:
            return True
        else:
            return False

    @staticmethod
    def generate_random_char_id():
        """
        Generate a random 8 character string for the char id
        """
        # ascii_letters supposedly is a cont of upper and lowercase
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))