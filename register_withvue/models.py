from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    is_senior = models.BooleanField(default=False)
    penalty_limit = models.IntegerField(default=0)  # 0 = limitsiz
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    SCHEDULE_CHOICES = [
        ("odd", "Du-Chor-Juma"),
        ("even", "Se-Pay-Shan"),
    ]

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255, blank=True)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    stage = models.IntegerField(default=1)
    schedule = models.CharField(
        max_length=10,
        choices=SCHEDULE_CHOICES,
        default="odd",
    )
    is_admin = models.BooleanField(default=False)
    is_excellence = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class StudentPenalty(models.Model):
    REASON_CHOICES = [
        ("late", "Kech kelish"),
        ("absent", "Darsga kelmadi"),
        ("behavior", "Xulq-atvor"),
        ("other", "Boshqa"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="penalties",
    )
    given_by = models.ForeignKey(  # kim kiritdi
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name="given_penalties",
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default="other")
    description = models.TextField(blank=True)
    amount = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} — {self.get_reason_display()} — {self.amount}"


class StagePrice(models.Model):
    stage = models.IntegerField(unique=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stage}-etap: {self.price}"


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name="lessons"
    )
    date = models.DateField()

    def __str__(self):
        return self.title


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Keldi"),
        ("absent", "Kelmadi"),
        ("late", "Kech keldi"),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendances"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attendances"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="absent")

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} — {self.lesson} — {self.status}"


class Payment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="payments"
    )
    month = models.CharField(max_length=7)
    stage = models.IntegerField()
    amount_due = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "month")

    def __str__(self):
        return f"{self.student} — {self.month} — {self.amount_due}"
