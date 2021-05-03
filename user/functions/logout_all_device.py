from django.contrib.auth import get_user_model
from user.models.auth_token import AuthToken
User = get_user_model()

def logout_all_device(user_id): 
	AuthToken.objects.filter(user_id=user_id, is_revoked=False).update(is_revoked=True)
	