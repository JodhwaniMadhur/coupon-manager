class CouponError(Exception):
    """Base exception for coupon-related errors"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class CouponNotFoundError(CouponError):
    def __init__(self, message="Coupon not found"):
        super().__init__(message, status_code=404)

class CouponValidationError(CouponError):
    def __init__(self, message="Invalid coupon data"):
        super().__init__(message, status_code=400)

class CouponExpiredError(CouponError):
    def __init__(self, message="Coupon has expired"):
        super().__init__(message, status_code=400)

class CartValidationError(CouponError):
    def __init__(self, message="Invalid cart data"):
        super().__init__(message, status_code=400)