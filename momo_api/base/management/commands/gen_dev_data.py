import os
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings

from momo_api.account.models import UserProfile, CompanyProfile
from momo_api.listing.models import Event, Listing

from momo_api.account.tests.helpers import create_test_user_profile, create_test_company_profile
from momo_api.listing.tests.helpers import create_test_event, create_test_listing


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
        print '.',

        company_westfield_mall = create_test_company_profile(
            username='westfield',
            password='test',
            name='Westfield San Francisco Centre',
            email='help@westfield.com',
        )
        print '.'

        #################### 3. LISTINGS ####################
        print 'Creating Listings',

        listing_kanye = create_test_listing(
            author=user_maurice.account,
            name='Kanye West',
            short_description='Kanye West is borked up',
            long_description='Kanye west is really really really really really really really really really really really really really really really really really borked up',
        )
        print '.',

        listing_dean = create_test_listing(
            author=user_alpha.account,
            name='Dean',
            short_description='Dean is a God',
            long_description='Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean! DEAN! DEAN!!! DEAN!!!!!!!!!!!!!!!! DEANNN!!!!!!!!!!!!!',
        )
        print '.',

        listing_metropolitan_musem = create_test_listing(
            author=user_maurice.account,
            name='The Metropolitan Museum of Art',
            short_description='The largest art museum in the United States',
            long_description='The Metropolitan Museum of Art, colloquially "the Met", is located in New York City and is the largest art museum in the United States, and is among the most visited art museums in the world. Its permanent collection contains over two million works, divided among seventeen curatorial departments. The main building, on the eastern edge of Central Park along Manhattan\'s Museum Mile, is by area one of the world\'s largest art galleries. A much smaller second location, The Cloisters at Fort Tryon Park in Upper Manhattan, contains an extensive collection of art, architecture, and artifacts from Medieval Europe.',
        )
        print '.',

        listing_westfield_mall = create_test_listing(
            author=company_westfield_mall.account,
            name='Westfield San Francisco Centre',
            short_description='An upsacle, urban shopping mall located in San Francisco, California.',
            long_description='Originally developed by Sheldon Gordon (co-developer of The Forum Shops at Caesars and Beverly Center) the center opened in October 1991 as San Francisco Shopping Centre with approximately 500,000 square feet (46,000 m2) of space, the then-largest Nordstrom store (350,000 square feet) on the top several floors, the first spiral escalators in the United States, and connecting through to the adjoining Emporium-Capwell flagship store.\nAfter a slow start, it soon became one of the top performing shopping centers in the country. In 1996, the adjoining Emporium (it had dropped the Capwell name by then) was shuttered in the wake of Federated Department Stores\' buyout of its parent, Broadway Stores. The vacated store was temporarily used as a Macy\'s furniture store while it renovated its Union Square flagship in 1997.',
        )
        print '.'

        #################### 4. EVENTS ####################
        print 'Creating Events',

        event_kanye = create_test_event(
            author=user_maurice.account,
            listing=listing_kanye,
            name='Kanye West',
            short_description='Kanye West is borked up',
            long_description='Kanye west is really really really really really really really really really really really really really really really really really borked up',
        )
        print '.',

        event_dean = create_test_event(
            author=user_alpha.account,
            listing=listing_dean,
            name='Dean',
            short_description='Dean is a God',
            long_description='Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean Dean! DEAN! DEAN!!! DEAN!!!!!!!!!!!!!!!! DEANNN!!!!!!!!!!!!!',
        )
        print '.'

        #################### FINAL OUTPUT ####################
        print '-------------------- Users --------------------'
        print 'There are {} test users:'.format(UserProfile.objects.count())
        for user in UserProfile.objects.all():
            print ' * User {}:'.format(user.id)
            print '     - username: {}'.format(user.account.username)
            print '     - name: {}'.format(user.full_name)

        print '------------------ Companies ------------------'
        print 'There are {} test companies:'.format(CompanyProfile.objects.count())
        for company in CompanyProfile.objects.all():
            print ' * Company {}:'.format(company.id)
            print '     - username: {}'.format(company.account.username)
            print '     - name: {}'.format(company.name)

        print '------------------- Listings -------------------'
        print 'There are {} test listings:'.format(Listing.objects.count())
        for listing in Listing.objects.all():
            print ' * Listing {}:'.format(listing.id)
            print '     - name: {}'.format(listing.name)
            print '     - author: {}'.format(listing.author.username)

        print '-------------------- Events --------------------'
        print 'There are {} test events:'.format(Event.objects.count())
        for event in Event.objects.all():
            print ' * Event {}:'.format(event.id)
            print '     - name: {}'.format(event.name)
            print '     - author: {}'.format(event.author.username)
