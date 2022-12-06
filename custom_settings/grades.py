from django.db import models


class GradeChoices(models.TextChoices):
    NURSERY = ("Nursery","Nursery")
    LKG = ("LKG","L.K.G")
    UKG = ("UKG","U.K.G")
    ONE = ("One","One(1)")
    TWO = ("Two","Two(2)")
    THREE =("Three","Three(3)")
    FOUR = ("Four","Four(4)")
    FIVE = ("Five","Five(5)")
    SIX = ("Six","Six(6)")
    SEVEN = ("Seven","Seven(7)")
    EIGHT = ("Eight","Eight(8)")
    NINE = ("Nine","Nine(9)")
    TEN = ("Ten","Ten(10)")
    ELEVEN = ("Eleven","Eleven(11)")
    TWELVE = ("Twelve","Twelve(12)")