from exceptions import *
from datetime import datetime
from flask import current_app
from typing import Optional, Dict, Any, Union, List

class CouponService:
    @staticmethod
    def validate_cart(cart_data: Union[List[Dict], Dict[str, Any]]) -> None:
        # Extract items list regardless of input format
        if isinstance(cart_data, dict) and 'items' in cart_data:
            items = cart_data['items']
        elif isinstance(cart_data, list):
            items = cart_data
        else:
            raise CartValidationError("Invalid cart format. Expected list of items or dict with 'items' key")
            
        if not items:
            raise CartValidationError("Cart must contain items")
        
        for item in items:
            if not isinstance(item, dict):
                raise CartValidationError("Invalid cart item format")
                
            required_keys = {'product_id', 'quantity', 'price'}
            if not all(key in item for key in required_keys):
                raise CartValidationError(f"Cart item must contain: {required_keys}")
                
            if not isinstance(item['product_id'], int):
                raise CartValidationError("Product ID must be an integer")
                
            if not isinstance(item['quantity'], (int, float)) or item['quantity'] <= 0:
                raise CartValidationError("Quantity must be a positive number")
                
            if not isinstance(item['price'], (int, float)) or item['price'] < 0:
                raise CartValidationError("Price must be a non-negative number")

    # Update other methods to handle the normalized cart format
    @staticmethod
    def calculate_cart_wise_discount(cart_data, coupon_details):
        try:
            items = cart_data['items'] if isinstance(cart_data, dict) and 'items' in cart_data else cart_data
            cart_total = sum(item['price'] * item['quantity'] for item in items)
            if cart_total > coupon_details['threshold']:
                return (cart_total * coupon_details['discount']) / 100
            return 0
        except KeyError as e:
            current_app.logger.error(f"Missing key in coupon details: {str(e)}")
            raise CouponValidationError("Invalid coupon details format")
        except Exception as e:
            current_app.logger.error(f"Error calculating cart-wise discount: {str(e)}")
            raise CouponError("Error calculating discount")

    @staticmethod
    def calculate_product_wise_discount(cart_data, coupon_details):
        try:
            items = cart_data['items'] if isinstance(cart_data, dict) and 'items' in cart_data else cart_data
            discount = 0
            for item in items:
                if item['product_id'] == coupon_details['product_id']:
                    discount += (item['price'] * item['quantity'] * coupon_details['discount']) / 100
            return discount
        except KeyError as e:
            current_app.logger.error(f"Missing key in coupon details: {str(e)}")
            raise CouponValidationError("Invalid coupon details format")
        except Exception as e:
            current_app.logger.error(f"Error calculating product-wise discount: {str(e)}")
            raise CouponError("Error calculating discount")

    @staticmethod
    def calculate_bxgy_discount(cart_data, coupon_details):
        try:
            items = cart_data['items'] if isinstance(cart_data, dict) and 'items' in cart_data else cart_data
            buy_products = {item['product_id']: item['quantity'] for item in coupon_details['buy_products']}
            get_products = {item['product_id']: item['quantity'] for item in coupon_details['get_products']}
            repetition_limit = coupon_details.get('repetition_limit', 1)

            cart_products = {}
            for item in items:
                cart_products[item['product_id']] = item['quantity']

            possible_applications = float('inf')
            for prod_id, required_qty in buy_products.items():
                if prod_id not in cart_products:
                    return 0
                possible_applications = min(
                    possible_applications,
                    cart_products[prod_id] // required_qty
                )

            applications = min(possible_applications, repetition_limit)

            discount = 0
            for prod_id, qty in get_products.items():
                for item in items:
                    if item['product_id'] == prod_id:
                        free_qty = qty * applications
                        discount += item['price'] * free_qty
                        break

            return discount
        except KeyError as e:
            current_app.logger.error(f"Missing key in coupon details: {str(e)}")
            raise CouponValidationError("Invalid coupon details format")
        except Exception as e:
            current_app.logger.error(f"Error calculating BxGy discount: {str(e)}")
            raise CouponError("Error calculating discount")

    @staticmethod
    def apply_coupon(cart_data, coupon):
        try:
            # Validate cart structure
            CouponService.validate_cart(cart_data)
            
            # Normalize cart data to use items consistently
            items = cart_data['items'] if isinstance(cart_data, dict) and 'items' in cart_data else cart_data

            # Check coupon validity
            if not coupon.is_active:
                raise CouponError("Coupon is not active")
            
            if coupon.expires_at and coupon.expires_at < datetime.utcnow():
                raise CouponExpiredError()

            discount_calculators = {
                'cart-wise': CouponService.calculate_cart_wise_discount,
                'product-wise': CouponService.calculate_product_wise_discount,
                'bxgy': CouponService.calculate_bxgy_discount
            }

            calculator = discount_calculators.get(coupon.type)
            if not calculator:
                raise CouponValidationError(f"Invalid coupon type: {coupon.type}")

            total_discount = calculator({'items': items}, coupon.details)
            total_price = sum(item['price'] * item['quantity'] for item in items)
            
            updated_cart = {
                'items': items,
                'total_price': total_price,
                'total_discount': total_discount,
                'final_price': total_price - total_discount
            }

            current_app.logger.info(
                f"Successfully applied coupon {coupon.code} of type {coupon.type}. "
                f"Discount: {total_discount}"
            )

            return updated_cart

        except Exception as e:
            current_app.logger.error(f"Error applying coupon {coupon.code}: {str(e)}")
            raise