from django.core.exceptions import ValidationError


def validate_name(text):
    if all(True if letter.isalpha() else False for letter in text) is False:
        raise ValidationError('Только буквы.')
