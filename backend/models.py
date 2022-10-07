from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
#database_name = 'almacenes_api'
database_name = 'almacenes_vue'


#cloud_db_password=os.getenv('CLOUD_DB_PASSWORD')
#db_password = os.getenv('DB_PASSWORD')
db_password='123'
database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', db_password, 'localhost:5432', database_name) #local database
#database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', db_password, '20.127.2.247:5432', database_name) #cloud db
secret_key=os.getenv('SECRET_KEY')

def setup_db(app, database_path = database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=secret_key
    db.app = app
    db.init_app(app)
    db.create_all()



class User (
    db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column (
        db.Integer,
        primary_key = True)
    nombre = db.Column (
        db.String(),
        nullable = False)
    apellido = db.Column (
        db.String(),
        nullable = False)
    edad = db.Column (
        db.Integer,
        nullable = False)
    sexo = db.Column (
        db.String(),
        nullable = False)
    usuario= db.Column (
        db.String(),
        unique = True,
        nullable = False)
    contraseña = db.Column (
        db.String(),
        nullable = False)
    date_created = db.Column (
        db.Date, 
        nullable = False)
    almacenes = db.relationship(
        'Almacen', 
        cascade="all,delete", 
        backref = 'usuario')

    def __repr__(self):
        return f'Usuario: id = {self.id}, nombre = {self.nombre}, apellido = {self.apellido}, edad = {self.edad}'

    #Set_password hashea la contraseña dada por el usuario.
    def set_password(
        self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    #Check_password compara la contraseña dada con la contraseña haseada y guardada en la base de datos
    def check_password (
        self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def format(self):
        return {
            'id':self.id,
            'nombre':self.nombre,
            'apellido':self.apellido,
            'edad':self.edad,
            'sexo':self.sexo,
            'usuario':self.usuario
        }
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Existente"
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_usuario(usuario):
        return User.query.filter_by(usuario=usuario).first()


#Entidad de los almacenes
class Almacen(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column(
        db.Integer, primary_key=True)
    user_id= db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    nombre= db.Column(
        db.String(),        
        unique=True,
        nullable=False)
    descripcion= db.Column(
        db.Text,
        nullable=False)
    capacidad= db.Column(
        db.Integer,
        nullable=False)
    date_created=db.Column(
        db.String(),
        nullable=False)
    date_modified=db.Column(
        db.String(),
        nullable=False)
    productos=db.relationship(
        'Producto',
        cascade = "all,delete",
        backref='almacen')

    def __repr__(self) -> str:
        return f'id: {self.id}, Nombre: {self.nombre}, Dueño:{self.user_id}'

    def format(self):
        return {
                'id':self.id,
                'user_id':self.user_id,
                'nombre':self.nombre,
                'descripcion':self.descripcion,
                'capacidad':self.capacidad,
                'date_created':self.date_created
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Existente"
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()        
            
    #Método para obtener el almacén
    @staticmethod
    def get_almacen_by_id(user_id):
        return Almacen.query.filter_by(user_id=user_id).first()

#Entidad de los Productos
class Producto(db.Model):
    __tablename__='productos'
    id=db.Column(
        db.Integer,
        primary_key=True)
    nombre = db.Column(
        db.String(),
        nullable=False)
    almacen_id = db.Column(
        db.Integer,
        db.ForeignKey('almacenes.id'), nullable=False)
    descripción = db.Column(
        db.Text,
        nullable=False)
    tipo= db.Column(
        db.String(),
        nullable=False)
    cantidad=db.Column(
        db.Integer,
        nullable=False)
    fecha_ingreso=db.Column(
        db.Date,
        nullable=False)
    venta = db.Column(
        db.Boolean, 
        nullable = False)
    transacciones=db.relationship(
        'Transaccion',
        cascade="all, delete" ,
        backref='producto' 
        )

    def __repr__(self) -> str:
        return f'id: {self.id}, nombre: {self.nombre}, tipo_ {self.tipo}, almacen_id: {self.almacen_id}'

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return{
                'id':self.id,
                'nombre':self.nombre,
                'almacen_id':self.almacen_id,
                'descripcion':self.descripción,
                'tipo':self.tipo,
                'cantidad':self.cantidad,
                'fecha_ingreso':self.fecha_ingreso,
                'en_venta':self.venta,
                }        
    @staticmethod
    def get_producto_by_nombre(nombre):
        return Producto.query.filter_by(nombre=nombre).first()

class Transaccion(db.Model):
    __tablename__="transacciones"
    id = db.Column(
        db.Integer,
        primary_key=True)
    tipoDocumento = db.Column(
        db.String(),
        nullable=False)
    fechaDoc=db.Column(
        db.Date, 
        nullable=False)
    idProducto = db.Column(
        db.Integer, 
        db.ForeignKey('productos.id'), nullable=False)
    cantidad=db.Column(
        db.Integer, 
        nullable=False)

    def repr(self) -> str:
        return f'id: {self.id}, tipoDocumento: {self.tipoDocumento}, fecha doumento: {self.fechaDoc}, cantidad: {self.cantidad}'

    def format(self):
        return {
                'tipoDocumento':self.tipoDocumento,
                'fechaDoc':self.fechaDoc,
                'idProducto':self.idProducto
                }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


