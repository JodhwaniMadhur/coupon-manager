from flask import Blueprint, request, jsonify, current_app
from models import Coupon, db
from schemas import CouponSchema, CartSchema
from services import CouponService
from exceptions import *
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


api = Blueprint('api', __name__)
coupon_schema = CouponSchema()
cart_schema = CartSchema()

@api.errorhandler(CouponError)
def handle_coupon_error(error):
    response = {
        'error': error.message,
        'status_code': error.status_code
    }
    current_app.logger.error(f"Coupon error: {error.message}")
    return jsonify(response), error.status_code

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    response = {
        'error': 'Validation error',
        'messages': error.messages
    }
    current_app.logger.error(f"Validation error: {error.messages}")
    return jsonify(response), 400

@api.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    response = {
        'error': 'Database error occurred'
    }
    current_app.logger.error(f"Database error: {str(error)}")
    return jsonify(response), 500

@api.route('/coupons', methods=['POST'])
def create_coupon():
    try:
        data = coupon_schema.load(request.json)
        existing_coupon = Coupon.query.get(data['code'])
        if existing_coupon:
            raise CouponValidationError("Coupon with this code already exists")
        
        coupon = Coupon(**data)
        db.session.add(coupon)
        db.session.commit()
        
        current_app.logger.info(f"Created new coupon with code {coupon.code}")
        return coupon_schema.dump(coupon), 201
        
    except ValidationError as e:
        current_app.logger.error(f"Validation error creating coupon: {e.messages}")
        raise
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error creating coupon: {str(e)}")
        db.session.rollback()
        raise

@api.route('/coupons', methods=['GET'])
def get_coupons():
    try:
        coupons = Coupon.query.all()
        current_app.logger.info(f"Retrieved {len(coupons)} coupons")
        return jsonify(coupon_schema.dump(coupons, many=True))
    except Exception as e:
        current_app.logger.error(f"Error retrieving coupons: {str(e)}")
        raise

@api.route('/coupons/<string:code>', methods=['GET'])
def get_coupon(code):
    try:
        coupon = Coupon.query.get(code)
        if not coupon:
            raise CouponNotFoundError(f"Coupon with code {code} not found")
        
        current_app.logger.info(f"Retrieved coupon {code}")
        return coupon_schema.dump(coupon)
    except Exception as e:
        current_app.logger.error(f"Error retrieving coupon {code}: {str(e)}")
        raise

@api.route('/coupons/<string:code>', methods=['PUT'])
def update_coupon(code):
    try:
        coupon = Coupon.query.get(code)
        if not coupon:
            raise CouponNotFoundError(f"Coupon with code {code} not found")

        data = coupon_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(coupon, key, value)
        
        db.session.commit()
        
        current_app.logger.info(f"Updated coupon {code}")
        return coupon_schema.dump(coupon)
        
    except ValidationError as e:
        current_app.logger.error(f"Validation error updating coupon {code}: {e.messages}")
        raise
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error updating coupon {code}: {str(e)}")
        db.session.rollback()
        raise

@api.route('/coupons/<string:code>', methods=['DELETE'])
def delete_coupon(code):
    try:
        coupon = Coupon.query.get(code)
        if not coupon:
            raise CouponNotFoundError(f"Coupon with code {code} not found")

        db.session.delete(coupon)
        db.session.commit()
        
        current_app.logger.info(f"Deleted coupon {code}")
        return '', 204
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error deleting coupon {code}: {str(e)}")
        db.session.rollback()
        raise

@api.route('/applicable-coupons', methods=['POST'])
def get_applicable_coupons():
    try:
        # Remove many=True and properly load the cart object
        cart_data = cart_schema.load(request.json)
        # Extract the items from the cart structure
        cart_items = cart_data['cart']['items']
        
        coupons = Coupon.query.filter_by(is_active=True).all()
        
        applicable_coupons = []
        for coupon in coupons:
            try:
                updated_cart = CouponService.apply_coupon(cart_items, coupon)
                if updated_cart and updated_cart['total_discount'] > 0:
                    applicable_coupons.append({
                        'coupon_code': coupon.code,
                        'type': coupon.type,
                        'discount': updated_cart['total_discount']
                    })
            except CouponError as e:
                current_app.logger.warning(f"Coupon {coupon.code} not applicable: {str(e)}")
                continue
        
        current_app.logger.info(f"Found {len(applicable_coupons)} applicable coupons")
        return jsonify({'applicable_coupons': applicable_coupons})
        
    except ValidationError as e:
        current_app.logger.error(f"Validation error checking applicable coupons: {e.messages}")
        raise
    except Exception as e:
        current_app.logger.error(f"Error checking applicable coupons: {str(e)}")
        raise

@api.route('/apply-coupon/<string:code>', methods=['POST'])
def apply_coupon(code):
    try:
        cart_data = cart_schema.load(request.json)
        cart_items = cart_data['cart']['items']
        
        coupon = Coupon.query.get(code)
        if not coupon:
            raise CouponNotFoundError(f"Coupon with code {code} not found")
        
        updated_cart = CouponService.apply_coupon({'items': cart_items}, coupon)
        
        current_app.logger.info(f"Successfully applied coupon {code}")
        return jsonify({'updated_cart': updated_cart})
        
    except ValidationError as e:
        current_app.logger.error(f"Validation error applying coupon {code}: {e.messages}")
        raise
    except Exception as e:
        current_app.logger.error(f"Unexpected error applying coupon {code}: {str(e)}")
        raise

@api.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500