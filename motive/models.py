from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel, BaseHistoryModel

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
    def insertHistory(motive: "Motive", user: str, operation: int):
        hmotive = HMotive()
        hmotive.motive = motive
        hmotive.suspension_name = motive.suspension_name
        hmotive.active_name = motive.active_name
        hmotive.service = motive.service
        hmotive.special_active = motive.special_active
        hmotive.is_active = motive.is_active
        hmotive.date = motive.date
        hmotive.operation = operation
        hmotive.user = user

        hmotive.save()

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

        try:
            with transaction.atomic():
                motive.save()
                Motive.insertHistory(motive=motive, user=user, operation=1)
            return motive
        except DatabaseError:
            return None

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

        try:
            with transaction.atomic():
                self.save()
                Motive.insertHistory(motive=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete motive """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Motive.insertHistory(motive=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active motive previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Motive.insertHistory(motive=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None


class HMotive(BaseHistoryModel):
    """ motive history """
    motive = models.ForeignKey(
        Motive,
        on_delete=models.RESTRICT,
        related_name="hmotive",
        editable=False
    )
    suspension_name = models.CharField(max_length=100)
    active_name = models.CharField(max_length=100)
    service = models.CharField(max_length=1000)
    special_active = models.BooleanField(default=False)
