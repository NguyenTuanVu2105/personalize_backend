import logging
import traceback

from shop.models import Ecommerce, Shop

logger = logging.getLogger(__name__)


def create_user_printholo_store(user):
    try:
        printholo_ecommerce = Ecommerce.objects.filter(name__contains="PrintHolo").first()
        shop_name = "{}_printholo".format(user.email.split("@")[0], )
        printholo_store = Shop.objects.filter(owner_id=user.id, ecommerce=printholo_ecommerce).first()
        if not printholo_store:
            logger.info("CREATE USER PRINTHOLO STORE...")
            Shop.objects.create(owner_id=user.id, ecommerce=printholo_ecommerce, name=shop_name,
                                email=user.email, access_token=user.email)


    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(str(e))
