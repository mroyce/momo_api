import os
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings

from momo_api.account.models import UserProfile, CompanyProfile
from momo_api.account.tests.helpers import create_test_user_profile, create_test_company_profile


class Command(BaseCommand):
    """
    gen_dev_data command
    Generate data for our local development environments.
    """
    def handle(self, *args, **kwargs):
        # Only run this command in development environment
        if not settings.DEBUG:
            print 'Only run this command in development environment'
            return

        # Delete previous files in `/media/`
        print 'Deleting existing media files'
        folder = settings.MEDIA_ROOT
        if os.path.isdir(folder):
            shutil.rmtree(folder)

        #################### 1. USERS ####################
        print 'Creating Users',

        user_maurice = create_test_user_profile(
            username='maurice',
            password='test',
            first_name='Maurice',
            last_name='Royce',
            email='maurice.royce@gmail.com',
        )
        print '.',

        user_scott = create_test_user_profile(
            username='scott',
            password='test',
            first_name='Scott',
            last_name='Kwang',
            email='scott@zanbato.com',
        )
        print '.',

        user_michael = create_test_user_profile(
            username='michael',
            password='test',
            first_name='Michael',
            last_name='Chen',
            email='michael@zanbato.com',
        )
        print '.',

        user_alpha = create_test_user_profile(
            username='alpha',
            password='test',
            first_name='Alpha',
            last_name='Smith',
            email='alpha@example.com',
        )
        print '.',

        user_bravo = create_test_user_profile(
            username='bravo',
            password='test',
            first_name='Bravo',
            last_name='Smith',
            email='bravo@example.com',
        )
        print '.'

        #################### 2. COMPANIES ####################
        print 'Creating Companies',

        company_mcdonalds = create_test_company_profile(
            username='mcdonalds',
            password='test',
            name='McDonalds',
            email='help@mcdonalds.com',
        )
        print '.',

        company_circle = create_test_company_profile(
            username='circle',
            password='test',
            name='Circle',
            email='help@circle.com',
        )
        print '.'

        #################### FINAL OUTPUT ####################
        print '-------------------- Users --------------------'
        print 'There are {} test users:'.format(UserProfile.objects.count())
        for user in UserProfile.objects.all():
            print ' * User {}:'.format(user.id)
            # print '     - username: {}'.format(user.get_account.username)
            print '     - name: {}{}'.format(user.first_name, user.last_name)

        print '------------------ Companies ------------------'
        print 'There are {} test companies:'.format(CompanyProfile.objects.count())
        for company in CompanyProfile.objects.all():
            print ' * Company {}:'.format(company.id)
            # print '     - username: {}'.format(company.get_account.username)
            print '     - name: {}'.format(company.name)
