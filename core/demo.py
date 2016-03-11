import random

from django.contrib.auth.models import User

from core.models import Watching, Series

USERNAME = 'demouser'
PASSWORD = ''

def reset_demouser():
    demo_user, created = User.objects.get_or_create(username=USERNAME, defaults={
        'first_name': '',
        'last_name': '',
        'email': '',
    })
    demo_user.set_password(PASSWORD)
    demo_user.save()

    series_candidates = [
        73244,  # The Office
        73762,  # Grey's Anatomy
        75710,  # Criminal Minds
        78957,  # Deadliest catch
        79126,  # The Wire
        79169,  # Seinfeld
        79216,  # The IT Crowd
        79349,  # Dexter
        80348,  # Chuck
        84021,  # Better off Ted
        84947,  # Boardwalk Empire
        81189,  # Breaking Bad
        121361, # Game of Thrones
        247808, # Suits
        256227, # The Newsroom
        260586, # Cosmos: A Spacetime Odyssey
        262407, # Black Sails
        275274, # Rick and Morty
        282670, # Narcos
    ]

    statuses = [
        ('active', 4),
        ('default', 4),
        ('archived', 2),
    ]

    demo_user.watches.all().delete()
    for status in statuses:
        for i in range(status[1]):
            tvdbid = random.choice(series_candidates)
            series_candidates.remove(tvdbid) # Ensure no dupes
            series = Series.create_or_sync(tvdbid)
            last_seen = random.choice(['', '1x04', series.last_episode().episode_number()])
            watching = Watching.objects.create(
                user=demo_user,
                series=series,
                last_seen=last_seen,
                status=status[0],
            )
            demo_user.watches.add(watching)

    return demo_user
