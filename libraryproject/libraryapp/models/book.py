from django.db import models

class Book(models.Model):

    title = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year_published = models.IntegerField()

    class Meta:
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"pk": self.pk})
