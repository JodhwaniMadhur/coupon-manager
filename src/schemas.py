from marshmallow import Schema, fields, validates, ValidationError

class CartItemSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

class CartContentSchema(Schema):
    items = fields.List(fields.Nested(CartItemSchema), required=True)

class CartSchema(Schema):
    cart = fields.Nested(CartContentSchema, required=True)

class CartWiseCouponSchema(Schema):
    threshold = fields.Float(required=True, validate=lambda x: x > 0)
    discount = fields.Float(required=True, validate=lambda x: 0 < x <= 100)

class ProductWiseCouponSchema(Schema):
    product_id = fields.Int(required=True, validate=lambda x: x > 0)
    discount = fields.Float(required=True, validate=lambda x: 0 < x <= 100)

class BxGyProductSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda x: x > 0)

class BxGyCouponSchema(Schema):
    buy_products = fields.List(fields.Nested(BxGyProductSchema), required=True)
    get_products = fields.List(fields.Nested(BxGyProductSchema), required=True)
    repetition_limit = fields.Int(required=True, validate=lambda x: x > 0)

class CouponSchema(Schema):
    code = fields.Str(required=True)
    type = fields.Str(required=True)
    description = fields.Str(required=True)
    details = fields.Dict(required=True)
    created_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime()
    is_active = fields.Boolean()

    @validates('type')
    def validate_type(self, value):
        valid_types = ['cart-wise', 'product-wise', 'bxgy']
        if value not in valid_types:
            raise ValidationError(f'Invalid coupon type. Must be one of: {valid_types}')

    @validates('details')
    def validate_details(self, value):
        type_schema_map = {
            'cart-wise': CartWiseCouponSchema(),
            'product-wise': ProductWiseCouponSchema(),
            'bxgy': BxGyCouponSchema()
        }
        