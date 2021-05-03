class ArtworkStatus:
    ACTIVE = '1'
    INACTIVE = '2'
    ERROR = '3'
    UPLOADED = '4'
    AD_CLONED = '5' # AD is artwork default
    SP_CLONED = '6' # SP is sample product


class VerboseArtworkStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ERROR = "error"
    UPLOADED = 'uploaded'
    AD_CLONED = 'artwork_default_cloned'
    SP_CLONED = 'sample_product_cloned'


ARTWORK_STATUS_CHOICES = [
    (ArtworkStatus.UPLOADED, VerboseArtworkStatus.UPLOADED),
    (ArtworkStatus.ACTIVE, VerboseArtworkStatus.ACTIVE),
    (ArtworkStatus.ERROR, VerboseArtworkStatus.ERROR),
    (ArtworkStatus.INACTIVE, VerboseArtworkStatus.INACTIVE),
    (ArtworkStatus.AD_CLONED, VerboseArtworkStatus.AD_CLONED),
    (ArtworkStatus.SP_CLONED, VerboseArtworkStatus.SP_CLONED)
]
