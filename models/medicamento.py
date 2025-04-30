# Modelo de medicamentos 
from datetime import datetime
from .database import db

class Medicamento(db.Model):
    """Medication model representing a medication in the inventory."""
    
    __tablename__ = 'medicamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with transactions
    transacciones = db.relationship('Transaccion', backref='medicamento', lazy=True)
    
    def __repr__(self):
        return f"<Medicamento {self.codigo}: {self.nombre}>"
    
    @classmethod
    def get_by_codigo(cls, codigo):
        """Find a medication by its code."""
        return cls.query.filter_by(codigo=codigo).first()
    
    @classmethod
    def get_all(cls):
        """Get all medications ordered by name."""
        return cls.query.order_by(cls.nombre).all()