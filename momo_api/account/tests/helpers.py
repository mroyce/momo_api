from datetime import datetime, timedelta

from momo_api.base.tests.helpers import create_test_image
from momo_api.account.models import Account, UserProfile, CompanyProfile


def create_test_account(username='test', password='test', **kwargs):
    """
    Create and return a test `Account` object
    """
    create_kwargs = {
        'username': username,
        'password': password,
    }

    create_kwargs.update(kwargs)
    return Account.objects.create_user(**create_kwargs)


def create_test_user_profile(username='test user', password='test', first_name='test', last_name='user', **kwargs):
    """
    Create and return a test `UserProfile` object
    """
    # create an account for this profile
    account_create_kwargs = {
        'account_type': Account.USER,
    }
    account = create_test_account(username, password, **account_create_kwargs)

    # update the user profile associated with this account
    user_profile = account.profile

    profile_update_kwargs = {
        'avatar': create_test_image(),
        'first_name': first_name,
        'last_name': last_name,
    }
    profile_update_kwargs.update(kwargs)

    for attr, value in profile_update_kwargs.items():
        setattr(user_profile, attr, value)
    user_profile.save()

    return user_profile


def create_test_company_profile(username='test company', password='test', name='test company', **kwargs):
    """
    Create and return a test `CompanyProfile` object
    """
    # create an account for this profile
    account_create_kwargs = {
        'account_type': Account.COMPANY,
    }
    account = create_test_account(username, password, **account_create_kwargs)

    # update the company profile associated with this account
    company_profile = account.profile

    profile_update_kwargs = {
        'avatar': create_test_image(),
        'name': name,
    }
    profile_update_kwargs.update(kwargs)

    for attr, value in profile_update_kwargs.items():
        setattr(company_profile, attr, value)
    company_profile.save()

    return company_profile
