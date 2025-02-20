from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# from PIL import Image


class MobileValidator(RegexValidator):
    regex = r"^0[0-9]{10}$"
    message = _(
        'شماره موبایل باید شامل 11 عدد باشد'
        'برای مثال  09171234567'
    )


def validate_avatar_size(image):
    max_size_mb = 2
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(_(f"حجم عکس پروفایل نباید بیشتر از  {max_size_mb}مگابایت باشد ."))
    

# def validate_avatar_dimensions(image):
#     max_width = 200
#     max_height = 200

#     with Image.open(image) as img:
#         width, height = img.size
#         if width > max_width or height > max_height:
#             raise ValidationError(_(
#                 f'The image dimensions should not exceed {max_width}x{max_height} pixels.'))