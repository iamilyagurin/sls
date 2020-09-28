from django.core import validators
from django.core.exceptions import ValidationError
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


def username_period_validate(value: str) -> None:
    if value.startswith('.'):
        raise ValidationError(START_WITH_PERIOD, code=username_base_validator.code)
    if value.endswith('.'):
        raise ValidationError(END_WITH_PERIOD, code=username_base_validator.code)
    if '..' in value:
        raise ValidationError(MORE_THAN_ONE_PERIOD, code=username_base_validator.code)


def username_validate(value: str) -> None:
    username_base_validator(value)
    username_period_validate(value)
