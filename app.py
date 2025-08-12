from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura la conexión a tu base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Minion10@localhost:5432/historial_clientes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo que representa la tabla historial_clientes
class HistorialCliente(db.Model):
    __tablename__ = 'historial_clientes'
    id_registro = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    especialista = db.Column(db.String(100), nullable=False)
    servicio = db.Column(db.String(200), nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)

@app.route('/')
def home():
    return "API Podología funcionando", 200

@app.route('/historial', methods=['GET'])
def get_historial():
    registros = HistorialCliente.query.all()
    resultado = []
    for r in registros:
        resultado.append({
            'id_registro': r.id_registro,
            'nombre_cliente': r.nombre_cliente,
            'fecha': r.fecha.isoformat(),
            'hora': r.hora.strftime('%H:%M:%S'),
            'especialista': r.especialista,
            'servicio': r.servicio,
            'costo': float(r.costo)
        })
    return jsonify(resultado)

@app.route('/historial', methods=['POST'])
def agregar_registro():
    data = request.get_json()
    try:
        nuevo = HistorialCliente(
            nombre_cliente=data['nombre_cliente'],
            fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
            hora=datetime.strptime(data['hora'], '%H:%M').time(),
            especialista=data['especialista'],
            servicio=data['servicio'],
            costo=float(data['costo'])
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Registro agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
