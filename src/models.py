from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Optional, Dict, Any


db = SQLAlchemy()

class Coupon(db.Model):
    __table_args__ = (
        db.Index('idx_coupon_type_active', 'type', 'is_active'),
        db.Index('idx_coupon_expires_at', 'expires_at'),
    )
    code: int = db.Column(db.String(10), primary_key=True)
    type: str = db.Column(db.String(20), nullable=False)
    description: Dict[str, Any] = db.Column(db.String(100), nullable=False)
    details: Optional[str] = db.Column(db.JSON, nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    is_active: bool = db.Column(db.Boolean, default=True)