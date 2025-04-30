# Archivo principal de la aplicación Flask 
import os
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from config import config
from models import init_app, db, Medicamento, Transaccion

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    Bootstrap5(app)
    init_app(app)
    
    # Register routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register application routes."""
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}


    @app.route('/')
    def index():
        """Home page route."""
        return render_template('index.html')
    
    @app.route('/medicamentos', methods=['GET', 'POST'])
    def medicamentos():
        """Medications management route."""
        if request.method == 'POST':
            if 'importar' in request.form:
                # Handle CSV import
                if 'archivo_csv' not in request.files:
                    flash('No se seleccionó ningún archivo', 'error')
                    return redirect(request.url)
                
                archivo = request.files['archivo_csv']
                if archivo.filename == '':
                    flash('No se seleccionó ningún archivo', 'error')
                    return redirect(request.url)
                
                if archivo and '.' in archivo.filename and archivo.filename.rsplit('.', 1)[1].lower() == 'csv':
                    try:
                        stream = io.StringIO(archivo.stream.read().decode("UTF8"), newline=None)
                        csv_reader = csv.reader(stream)
                        
                        # Skip header if it exists
                        if request.form.get('tiene_encabezado'):
                            next(csv_reader)
                        
                        count = 0
                        for row in csv_reader:
                            if len(row) >= 2:  # At least code and name
                                codigo = row[0].strip()
                                nombre = row[1].strip()
                                
                                # Check if medication already exists
                                med = Medicamento.get_by_codigo(codigo)
                                if not med:
                                    med = Medicamento(codigo=codigo, nombre=nombre)
                                    db.session.add(med)
                                    count += 1
                        
                        db.session.commit()
                        flash(f'Se importaron {count} medicamentos correctamente', 'success')
                    except Exception as e:
                        db.session.rollback()
                        flash(f'Error al importar medicamentos: {str(e)}', 'error')
                else:
                    flash('Formato de archivo no permitido. Use CSV.', 'error')
                
                return redirect(url_for('medicamentos'))
            else:
                # Handle manual medication addition
                codigo = request.form.get('codigo')
                nombre = request.form.get('nombre')
                
                if not codigo or not nombre:
                    flash('Código y nombre son requeridos', 'error')
                    return redirect(url_for('medicamentos'))
                
                try:
                    # Check if the medication already exists
                    existing = Medicamento.get_by_codigo(codigo)
                    if existing:
                        flash(f'El medicamento con código {codigo} ya existe', 'error')
                        return redirect(url_for('medicamentos'))
                    
                    med = Medicamento(codigo=codigo, nombre=nombre)
                    db.session.add(med)
                    db.session.commit()
                    flash('Medicamento registrado correctamente', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error al registrar medicamento: {str(e)}', 'error')
                
                return redirect(url_for('medicamentos'))
        
        # GET request: display medications
        medicamentos = Medicamento.get_all()
        return render_template('medicamentos.html', medicamentos=medicamentos)
    
    @app.route('/entregas', methods=['GET', 'POST'])
    def entregas():
        """Deliveries registration route."""
        if request.method == 'POST':
            # Process delivery form
            codigo = request.form.get('codigo')
            cantidad = int(request.form.get('cantidad', 1))
            unidad = request.form.get('unidad', 'Unidad')
            estado = request.form.get('estado', 'Entregado')
            
            if not codigo:
                flash('Código de medicamento es requerido', 'error')
                return redirect(url_for('entregas'))
            
            try:
                # Find the medication
                med = Medicamento.get_by_codigo(codigo)
                if not med:
                    flash(f'No se encontró medicamento con código {codigo}', 'error')
                    return redirect(url_for('entregas'))
                
                # Create transaction
                transaccion = Transaccion(
                    medicamento_id=med.id,
                    cantidad=cantidad,
                    unidad=unidad,
                    estado=estado
                )
                
                db.session.add(transaccion)
                db.session.commit()
                flash('Entrega registrada correctamente', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al registrar entrega: {str(e)}', 'error')
            
            return redirect(url_for('entregas'))
        
        # GET request: show delivery form
        medicamentos = Medicamento.get_all()
        return render_template('entregas.html', medicamentos=medicamentos)
    
    @app.route('/informes')
    def informes():
        """Reports main page route."""
        return render_template('informes.html')
    
    @app.route('/informes/transacciones', methods=['GET', 'POST'])
    def transacciones():
        """Transactions report route."""
        # Get current month and year or use form values
        now = datetime.now()
        month = int(request.args.get('mes', now.month))
        year = int(request.args.get('anio', now.year))
        
        # If form was submitted via POST
        if request.method == 'POST':
            month = int(request.form.get('mes', now.month))
            year = int(request.form.get('anio', now.year))
            return redirect(url_for('transacciones', mes=month, anio=year))
        
        # Get transactions for the selected month/year
        transacciones = []
        try:
            # Get raw transactions
            raw_transactions = Transaccion.get_by_month_year(month, year)
            
            # Prepare data for display
            for t in raw_transactions:
                med = Medicamento.query.get(t.medicamento_id)
                transacciones.append({
                    'id': t.id,
                    'fecha': t.fecha,
                    'codigo': med.codigo if med else 'N/A',
                    'medicamento': med.nombre if med else 'Desconocido',
                    'cantidad': t.cantidad,
                    'unidad': t.unidad,
                    'estado': t.estado
                })
        except Exception as e:
            flash(f'Error al cargar transacciones: {str(e)}', 'error')
        
        # Month names in Spanish
        meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        # Available years (current year and the previous 5)
        anios = list(range(now.year - 5, now.year + 1))
        
        return render_template(
            'transacciones.html',
            transacciones=transacciones,
            mes_actual=month,
            anio_actual=year,
            meses=meses,
            anios=anios
        )
    
    @app.route('/informes/resumen', methods=['GET', 'POST'])
    def resumen():
        """Summary report route."""
        # Get current month and year or use form values
        now = datetime.now()
        month = int(request.args.get('mes', now.month))
        year = int(request.args.get('anio', now.year))
        
        # If form was submitted via POST
        if request.method == 'POST':
            month = int(request.form.get('mes', now.month))
            year = int(request.form.get('anio', now.year))
            return redirect(url_for('resumen', mes=month, anio=year))
        
        # Get summary data
        summary_data = {}
        total_por_estado = {
            'Entregado': 0,
            'Sin Existencia': 0,
            'No Reclamado': 0
        }
        
        try:
            # Get raw summary data
            raw_summary = Transaccion.get_summary_by_month_year(month, year)
            
            # Process data for display
            for med_id, estado, cantidad, _ in raw_summary:
                med = Medicamento.query.get(med_id)
                if med:
                    med_key = f"{med.codigo} - {med.nombre}"
                    if med_key not in summary_data:
                        summary_data[med_key] = {
                            'Entregado': 0,
                            'Sin Existencia': 0,
                            'No Reclamado': 0,
                            'Total': 0
                        }
                    
                    # Update counts
                    summary_data[med_key][estado] += cantidad
                    summary_data[med_key]['Total'] += cantidad
                    total_por_estado[estado] += cantidad
            
            # Calculate overall total
            total_general = sum(total_por_estado.values())
            
        except Exception as e:
            flash(f'Error al generar resumen: {str(e)}', 'error')
        
        # Month names in Spanish
        meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        # Available years (current year and the previous 5)
        anios = list(range(now.year - 5, now.year + 1))
        
        return render_template(
            'resumen.html',
            summary_data=summary_data,
            total_por_estado=total_por_estado,
            total_general=total_general if 'total_general' in locals() else 0,
            mes_actual=month,
            anio_actual=year,
            meses=meses,
            anios=anios
        )
    
    # API endpoint for medication search (used by autocomplete)
    @app.route('/api/medicamentos/buscar')
    def api_buscar_medicamentos():
        query = request.args.get('q', '')
        if len(query) < 2:
            return jsonify([])
        
        # Search by code or name
        medicamentos = Medicamento.query.filter(
            (Medicamento.codigo.ilike(f'%{query}%')) | 
            (Medicamento.nombre.ilike(f'%{query}%'))
        ).limit(10).all()
        
        results = [{'id': m.id, 'codigo': m.codigo, 'nombre': m.nombre} for m in medicamentos]
        return jsonify(results)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)