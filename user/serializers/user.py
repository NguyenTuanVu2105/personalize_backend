from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from billing.sub_apps.combine_payment.models import GeneralPaymentMethod

User = get_user_model()


class BriefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')


class BriefUserWithPaymentSerializer(BriefUserSerializer):
    class Meta(BriefUserSerializer.Meta):
        fields = BriefUserSerializer.Meta.fields + ('is_valid_payment',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'birthday', 'tax_code', 'group', 'address')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'birthday', 'tax_code', 'address')


class AdminUserSerializer(serializers.ModelSerializer):
    from user.serializers.user_tag_serializer import UserTagWithoutUserIdSerializer

    tags = UserTagWithoutUserIdSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'tags', 'last_login', 'is_superuser', 'is_staff', 'is_lock',
                  'is_email_confirmed', 'is_test_user', 'is_valid_payment', 'create_time', 'account_type',
                  'country_code', 'client_ip')


class UserDetailSerializer(serializers.ModelSerializer):
    payment_methods = SerializerMethodField()

    def get_payment_methods(self, obj):
        payments = GeneralPaymentMethod.objects.active().by_user(obj.id)
        return [payment.payment_gateway_method_data for payment in payments if payment]

    class Meta:
        model = User
        fields = ('id', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'is_test_user',
                  'name', 'date_joined', 'avatar', 'phone_number', 'gender', 'tax_code', 'birthday',
                  'address', 'is_email_confirmed', 'is_valid_payment', 'account_type', 'country_code', 'client_ip',
                  'payment_methods')


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(source="avatar")

    class Meta:
        model = User
        fields = ["id", "name", "avatar_url", "phone_number", "last_change_password", "email", "gender", "tax_code",
                  "birthday", "address", "is_email_confirmed", "is_valid_payment", "account_type"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
