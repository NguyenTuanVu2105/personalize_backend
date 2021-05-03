class RateLimitView:
    CREATE_USER_PRODUCT = "1"
    UPDATE_USER_PRODUCT = "2"
    PREVIEW_MOCKUP = "3"
    PUSH_ALL_USER_PRODUCT_TO_SHOP = "4"
    UPLOAD_ARTWORK_CHUNK = "5"


class VerboseRateLimitView:
    CREATE_USER_PRODUCT = "create_user_product"
    UPDATE_USER_PRODUCT = "update_user_product"
    PREVIEW_MOCKUP = "preview_mockup"
    PUSH_ALL_USER_PRODUCT_TO_SHOP = "push_all_user_product_to_shop"
    UPLOAD_ARTWORK_CHUNK = "upload_artwork_chunk"


RATE_LIMIT_VIEW_CHOICES = [
    (RateLimitView.CREATE_USER_PRODUCT, VerboseRateLimitView.CREATE_USER_PRODUCT),
    (RateLimitView.UPDATE_USER_PRODUCT, VerboseRateLimitView.UPDATE_USER_PRODUCT),
    (RateLimitView.PREVIEW_MOCKUP, VerboseRateLimitView.PREVIEW_MOCKUP),
    (RateLimitView.PUSH_ALL_USER_PRODUCT_TO_SHOP, VerboseRateLimitView.PUSH_ALL_USER_PRODUCT_TO_SHOP),
    (RateLimitView.UPLOAD_ARTWORK_CHUNK, VerboseRateLimitView.UPLOAD_ARTWORK_CHUNK),
]
