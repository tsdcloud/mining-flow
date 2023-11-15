from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel, BaseHistoryModel

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
    def insertHistory(tractor: "Tractor", user: str, operation: int):
        htractor = HTractor()
        htractor.tractor = tractor
        htractor.registration = tractor.registration
        htractor.serial_number = tractor.serial_number
        htractor.brand = tractor.brand
        htractor.model = tractor.model
        htractor.is_used = tractor.is_used
        htractor.is_active = tractor.is_active
        htractor.date = tractor.date
        htractor.operation = operation
        htractor.user = user

        htractor.save()

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

        try:
            with transaction.atomic():
                tractor.save()
                Tractor.insertHistory(
                    tractor=tractor, user=user, operation=1)
            return tractor
        except DatabaseError:
            return None

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

        try:
            with transaction.atomic():
                self.save()
                Tractor.insertHistory(
                    tractor=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete tractor """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Tractor.insertHistory(
                    tractor=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore tractor previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Tractor.insertHistory(
                    tractor=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None

    def status_used(self, user: str):
        """ change attribut is_used """
        self.is_used = not self.is_used

        try:
            with transaction.atomic():
                self.save()
                Tractor.insertHistory(
                    tractor=self, user=user, operation=6)
            return self
        except DatabaseError:
            return None


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
    def insertHistory(trailer: "Trailer", user: str, operation: int):
        htrailer = HTrailer()
        htrailer.trailer = trailer
        htrailer.registration = trailer.registration
        htrailer.serial_number = trailer.serial_number
        htrailer.brand = trailer.brand
        htrailer.model = trailer.model
        htrailer.empty_volume = trailer.empty_volume
        htrailer.is_used = trailer.is_used
        htrailer.is_active = trailer.is_active
        htrailer.date = trailer.date
        htrailer.operation = operation
        htrailer.user = user

        htrailer.save()

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

        try:
            with transaction.atomic():
                trailer.save()
                Trailer.insertHistory(
                    trailer=trailer, user=user, operation=1)
            return trailer
        except DatabaseError:
            return None

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

        try:
            with transaction.atomic():
                self.save()
                Trailer.insertHistory(
                    trailer=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete trailer """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Trailer.insertHistory(
                    trailer=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore trailer previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Trailer.insertHistory(
                    trailer=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None

    def status_used(self, user: str):
        """ change attribut is_used """
        self.is_used = not self.is_used

        try:
            with transaction.atomic():
                self.save()
                Trailer.insertHistory(
                    trailer=self, user=user, operation=6)
            return self
        except DatabaseError:
            return None


class HTractor(BaseHistoryModel):
    """ Tractor history """
    tractor = models.ForeignKey(
        Tractor,
        on_delete=models.RESTRICT,
        related_name="htractors",
        editable=False
    )
    registration = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    is_used = models.BooleanField(default=False)


class HTrailer(BaseHistoryModel):
    """ Trailer history """
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.RESTRICT,
        related_name="htrailers",
        editable=False
    )
    registration = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    empty_volume = models.FloatField()
    is_used = models.BooleanField(default=False)
