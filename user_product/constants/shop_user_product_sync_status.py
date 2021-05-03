class ShopUserProductSyncStatus:
    SYNCING = '0'
    SYNCED = '1'
    ERROR = '2'
    NEW = '3'
    DELETED = '4'
    DELETING = '5'
    PENDING_DELETE = '6'


class VerboseShopUserProductSyncStatus:
    SYNCING = 'syncing'
    SYNCED = 'synced'
    ERROR = 'error'
    NEW = "new"
    DELETED = 'deleted'
    DELETING = 'deleting'
    PENDING_DELETE = 'pending_delete'


SHOP_USER_PRODUCT_SYNC_STATUS_CHOICES = [
    (ShopUserProductSyncStatus.SYNCING, VerboseShopUserProductSyncStatus.SYNCING),
    (ShopUserProductSyncStatus.SYNCED, VerboseShopUserProductSyncStatus.SYNCED),
    (ShopUserProductSyncStatus.ERROR, VerboseShopUserProductSyncStatus.ERROR),
    (ShopUserProductSyncStatus.NEW, VerboseShopUserProductSyncStatus.NEW),
    (ShopUserProductSyncStatus.DELETED, VerboseShopUserProductSyncStatus.DELETED),
    (ShopUserProductSyncStatus.DELETING, VerboseShopUserProductSyncStatus.DELETING),
    (ShopUserProductSyncStatus.PENDING_DELETE, VerboseShopUserProductSyncStatus.PENDING_DELETE)
]
