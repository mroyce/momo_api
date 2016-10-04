from rest_framework import serializers

from .models import Account, UserProfile, CompanyProfile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = (
            'id',
            'username',
            'password',
            'account_type',
            'is_active',
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

        read_only_fields = (
            'account_type',
            'is_active',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    # account = AccountSerializer()

    class Meta:
        model = UserProfile

        fields = (
            # 'account',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'gender',
            'phone_number',
        )


class CompanyProfileSerializer(serializers.ModelSerializer):
    # account = AccountSerializer()

    class Meta:
        model = CompanyProfile

    	fields = (
            # 'account',
            'name',
            'email',
            'avatar',
            'phone_number',
        )

