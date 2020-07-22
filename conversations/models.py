from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    """  """

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        usernames = []
        # dir()를 통해, participants라는 method 가 있다는게 확인가느ㅏㅇ
        # participants는 몇명이 포함되어있는지 확인 가능
        for user in self.participants.all():
            usernames.append(user.username)
        # " & ".join을 통해 usernames 폴더안에 있는 리스트르 쭉 조합 가능
        return " & ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"

