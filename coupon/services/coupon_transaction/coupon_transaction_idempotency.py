class CouponTransactionIdempotencyService:
    USER_PREFIX = "U"
    COUPON_PREFIX = "C"
    ORDER_PREFIX = "O"

    def __init__(self, user_id, coupon_id, order_id):
        self.user_id = user_id
        self.coupon_id = coupon_id
        self.order_id = order_id

    def get_key_by_user(self):
        assert self.user_id
        assert self.coupon_id

        return f"{self.COUPON_PREFIX}{self.coupon_id}_{self.USER_PREFIX}{self.user_id}"

    def get_key_by_order(self):
        assert self.user_id
        assert self.coupon_id
        assert self.order_id

        return f"{self.COUPON_PREFIX}{self.coupon_id}_{self.USER_PREFIX}{self.user_id}_{self.ORDER_PREFIX}{self.order_id}"
