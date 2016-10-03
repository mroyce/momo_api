from rest_framework import serializers

from .models import Account, User, Company

# TODO: Create factory implementation to create either User/Company serializer
# that already includes these Account model fields
"""
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
	    'is_active': {'read_only': True},
        }
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

	fields = (
            'id',
	    'username',
	    'password',
	    'account_type',
	    'is_active',

            'first_name',
	    'last_name',
	    'email',
	    'avatar',
	    'gender',
	    'phone_number',
        )

	extra_kwargs = {
            'password': {'write_only': True},
	    'is_active': {'read_only': True},
        }


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

	fields = (
            'id',
	    'username',
	    'password',
	    'account_type',
	    'is_active',

	    'name',
	    'email',
	    'avatar',
	    'phone_number',
	)

	extra_kwargs = {
            'password': {'write_only': True},
	    'is_active': {'read_only': True},
        }

