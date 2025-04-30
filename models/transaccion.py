# Modelo de transacciones 
from datetime import datetime
from .database import db

class Transaccion(db.Model):
    """Transaction model representing a medication transaction (delivery, etc.)."""
    
    __tablename__ = 'transacciones'
    
    id = db.Column(db.Integer, primary_key=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    unidad = db.Column(db.String(20), nullable=False, default='Unidad')
    estado = db.Column(db.String(20), nullable=False, default='Entregado')
    
    def __repr__(self):
        return f"<Transaccion {self.id}: {self.medicamento_id}, {self.cantidad}, {self.estado}>"
    
    @classmethod
    def get_by_month_year(cls, month, year):
        """Get transactions for a specific month and year."""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
            
        return cls.query.filter(cls.fecha >= start_date, cls.fecha < end_date).order_by(cls.fecha.desc()).all()
    
    @classmethod
    def get_summary_by_month_year(cls, month, year):
        """Get summary statistics for a specific month and year."""
        from sqlalchemy import func
        
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Group by medication and status, count transactions and sum quantities
        result = db.session.query(
            cls.medicamento_id,
            cls.estado,
            func.sum(cls.cantidad).label('total_cantidad'),
            func.count().label('transacciones')
        ).filter(
            cls.fecha >= start_date,
            cls.fecha < end_date
        ).group_by(
            cls.medicamento_id,
            cls.estado
        ).all()
        
        return result