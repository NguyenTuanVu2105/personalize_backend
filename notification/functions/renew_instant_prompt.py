from django.contrib.auth import get_user_model

from notification.enums.message_statuses import MessageStatus
from notification.models import InstantPrompt

User = get_user_model()


def renew_instant_prompt(instant_id):
    instant_prompt_to_create = []
    instant_prompt_to_update = []
    for user in User.objects.all():
        user_instant_prompts = InstantPrompt.objects.filter(owner=user, type=instant_id)
        if len(user_instant_prompts) == 0:
            instant_prompt_to_create.append(InstantPrompt(owner=user, type=instant_id, status=MessageStatus.UNREAD))
        else:
            for user_instant_prompt in user_instant_prompts:
                user_instant_prompt.status = MessageStatus.UNREAD
                instant_prompt_to_update.append(user_instant_prompt)

    InstantPrompt.objects.bulk_create(instant_prompt_to_create)
    InstantPrompt.objects.bulk_update(instant_prompt_to_update, ['status'])
