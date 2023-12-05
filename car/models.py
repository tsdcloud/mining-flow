from django.db import models
from common.models import BaseUUIDModel
import json
from datetime import datetime
# Create your models here.


class Tractor(BaseUUIDModel):
    registration = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    is_used = models.BooleanField(default=False)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_active", "-is_used", "registration", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.registration)

    @staticmethod
    def create(
        registration: str,
        serial_number: str,
        brand: str,
        model: str,
        user: str
    ):
        """ add tractor """
        try:
            tractor = Tractor.objects.get(
                registration=registration.upper(),
            )
            tractor.is_active = True
            tractor.is_used = False
        except Tractor.DoesNotExist:
            tractor = Tractor()
            tractor.registration = registration.upper()
            tractor.serial_number = serial_number.upper()

        tractor.brand = brand.upper()
        tractor.model = model.upper()

        tractor._change_reason = json.dumps({
            "reason": "Add a new tractor",
            "user": user
        })
        tractor._history_date = datetime.now()
        tractor.save()
        return tractor

    def change(
        self,
        registration: str,
        serial_number: str,
        brand: str,
        model: str,
        user: str
    ):
        """ change tractor """
        self.registration = registration.upper()
        self.serial_number = serial_number.upper()
        self.brand = brand.upper()
        self.model = model.upper()

        self._change_reason = json.dumps({
            "reason": "Update tractor",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete tractor """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete tractor",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore tractor previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore tractor",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def status_used(self, user: str):
        """ change attribut is_used """
        self.is_used = not self.is_used

        self._change_reason = json.dumps({
            "reason": "Change the tractor's operating state",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Trailer(BaseUUIDModel):
    registration = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    empty_volume = models.FloatField()
    is_used = models.BooleanField(default=False)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_active", "-is_used", "registration", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.registration)

    @staticmethod
    def create(
        registration: str,
        serial_number: str,
        brand: str,
        model: str,
        empty_volume: float,
        user: str
    ):
        """ add trailer """
        try:
            trailer = Trailer.objects.get(
                registration=registration.upper(),
            )
            trailer.is_active = True
            trailer.is_used = False
        except Trailer.DoesNotExist:
            trailer = Trailer()
            trailer.registration = registration.upper()
            trailer.serial_number = serial_number.upper()

        trailer.brand = brand.upper()
        trailer.model = model.upper()
        trailer.empty_volume = empty_volume

        trailer._change_reason = json.dumps({
            "reason": "Add a new trailer",
            "user": user
        })
        trailer._history_date = datetime.now()
        trailer.save()
        return trailer

    def change(
        self,
        registration: str,
        serial_number: str,
        brand: str,
        model: str,
        empty_volume: str,
        user: str
    ):
        """ change trailer """
        self.registration = registration.upper()
        self.serial_number = serial_number.upper()
        self.brand = brand.upper()
        self.model = model.upper()
        self.empty_volume = empty_volume

        self._change_reason = json.dumps({
            "reason": "Update trailer",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete trailer """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete trailer",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore trailer previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore trailer",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def status_used(self, user: str):
        """ change attribut is_used """
        self.is_used = not self.is_used

        self._change_reason = json.dumps({
            "reason": "Change the trailer's operating state",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
