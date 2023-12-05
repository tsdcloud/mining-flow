from django.db import models
from common.models import BaseUUIDModel
import json
from datetime import datetime

# Create your models here.


class Motive(BaseUUIDModel):
    """ Motive's class purpose is to manage motives """
    suspension_name = models.CharField(max_length=100)
    active_name = models.CharField(max_length=100)
    service = models.CharField(max_length=1000)
    special_active = models.BooleanField(default=False)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["suspension_name", "active_name", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.suspension_name, self.active_name)

    @staticmethod
    def create(
        suspension_name: str,
        active_name: str,
        service: str,
        special_active: bool,
        user: str
    ):
        """ add motive """
        try:
            motive = Motive.objects.get(
                suspension_name=suspension_name, service=service)
            motive.is_active = True
        except Motive.DoesNotExist:
            motive = Motive()
            motive.suspension_name = suspension_name.upper()
            motive.service = service

        motive.active_name = active_name.upper()
        motive.special_active = special_active

        motive._change_reason = json.dumps({
            "reason": "Add a new motive",
            "user": user
        })
        motive._history_date = datetime.now()
        motive.save()
        return motive

    def change(
        self,
        suspension_name: str,
        active_name: str,
        special_active: bool,
        user: str
    ):
        """ change motive """
        self.suspension_name = suspension_name.upper()
        self.active_name = active_name.upper()
        self.special_active = special_active

        self._change_reason = json.dumps({
            "reason": "Update motive",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete motive """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete motive",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active motive previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore motive",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
