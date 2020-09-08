from django.core import validators
from django.utils.translation import gettext_lazy as _
import re


MORE_THAN_ONE_PERIOD = _("You can't have more than one period in a row")
END_WITH_PERIOD = _("You can't end your username with period")
START_WITH_PERIOD = _("You can't start your username with period")


username_base_validator = validators.RegexValidator(
    regex=r'^[\w.]+\Z',
    message=_('Only English letters, numbers, characters . or _'),
    flags=re.ASCII,
)


def username_period_validate(value):
    if value.startswith('.'):
        raise validators.ValidationError(START_WITH_PERIOD, code=username_base_validator.code)
    if value.endswith('.'):
        raise validators.ValidationError(END_WITH_PERIOD, code=username_base_validator.code)
    if '..' in value:
        raise validators.ValidationError(MORE_THAN_ONE_PERIOD, code=username_base_validator.code)


def username_validate(value):
    username_base_validator(value)
    username_period_validate(value)
