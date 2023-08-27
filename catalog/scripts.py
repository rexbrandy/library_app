import pycountry
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from catalog.models import Language, Genre

def populate_languages():
    '''
    Will populate Language model
    To run open django shell and import module
    '''
    for lang in pycountry.languages:
        try:
            Language.objects.get(language_code=lang.alpha_3)
        except ObjectDoesNotExist:
            Language.objects.create(
                language_code=lang.alpha_3,
                name=lang.name,
            )

def populate_genres():
    '''
    Will populate Genre model
    To run open django shell and import module
    '''
    genres = [
        'Arts & Photography', 'Biographies & Memoirs', 'Business & Money', 'Calendars', 'Children\'s Books', 
        'Comics & Graphic Novels', 'Computers & Technology', 'Cookbooks, Food & Wine', 'Crafts, Hobbies & Home',
        'Christian Books & Bibles', 'Engineering & Transportation', 'Health, Fitness & Dieting', 'History', 
        'Humor & Entertainment', 'Law','Literature & Fiction', 'Medical Books', 'Mystery, Thriller & Suspense', 
        'Parenting & Relationships', 'Politics & Social Sciences', 'Reference', 'Religion & Spirituality', 'Romance',
        'Science & Math', 'Science Fiction & Fantasy', 'Self-Help', 'Sports & Outdoors', 'Teen & Young Adult', 
        'Test Preparation', 'Travel', 'Gay & Lesbian', 'Education & Teaching',
    ]

    for genre in genres:
        try: 
            Genre.objects.get(name=genre)
        except ObjectDoesNotExist:
            Genre.objects.create(
                name=genre
            )