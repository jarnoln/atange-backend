from django.db import models
from django.contrib.auth.models import User


class Collective(models.Model):
    name = models.SlugField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}:{}'.format(self.name, self.title)


class QuestionnaireItem(models.Model):
    ITEM_TYPES = [
        ('Q', 'Question'),
        ('H', 'Header')
    ]
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE)
    name = models.SlugField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, default='')
    order = models.IntegerField(
        default=0, blank=True,
        help_text='Determines the order between items at same level.'
    )
    item_type = models.CharField(max_length=1, default='Q', choices=ITEM_TYPES)
    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}:{}:{}:{}'.format(self.collective.name, self.item_type, self.name, self.title)


class Answer(models.Model):
    ANSWER_CHOICES = (
        (-1, 'No'),
        (0, 'Abstain'),
        (1, 'Yes')
    )
    question = models.ForeignKey(QuestionnaireItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0, choices=ANSWER_CHOICES)
    comment = models.TextField(null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}:{}:{}:{}'.format(self.question.collective.name, self.user.username, self.question.title, self.vote)
