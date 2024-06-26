from django.db import connection, models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Fakultas(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class DosenGrade(models.Model):
    name = models.CharField(max_length=2)
    percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Dosen(models.Model):
    name = models.CharField(max_length=200)
    fakultas = models.ForeignKey(Fakultas, on_delete=models.SET_NULL, null=True)
    matakuliah = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(DosenGrade, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.body[0:50]

    def clean_body(self):
        with connection.cursor() as cursor:
            query = """
                SELECT (regexp_replace(%s::text, '\\u0000', '', 'g'))::text;
            """
            cursor.execute(query, [self.body])
            result = cursor.fetchone()
            self.body = result[0] if result else self.body

    def save(self, *args, **kwargs):
        self.clean_body()
        super(Review, self).save(*args, **kwargs)
