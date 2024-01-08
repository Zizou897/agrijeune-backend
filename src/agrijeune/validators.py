from django.core.exceptions import ValidationError

def valideta_image_size(image):
    file_size = image.size
    limit_md = 2

    if file_size > limit_md * 1024 * 1024:
        raise ValidationError(f"La taille de l'image ne doit pas dépasser {limit_md} MB")
    else:
        return image
    

def validate_image_extension(image):
    ext = image.name.split(".")[-1]
    valid_extension = ['png', 'jpg', 'jpeg']
    if not ext.lower() in valid_extension:
        raise ValidationError("Transférez une image valide. Le fichier que vous avez transféré n'est pas une image, ou il est corrompu")
    else:
        return image