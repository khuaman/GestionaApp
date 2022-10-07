from lib2to3.pgen2 import token
import unittest
import json

from flask_login import current_user
from server import create_app
from models import setup_db, User, Almacen, Producto,Transaccion
import os
from dotenv import load_dotenv
import datetime
from requests.auth import _basic_auth_str

load_dotenv()


class TestCaseAlamacenesApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'almacenes_test'
        #self.database_password = os.getenv('DB_PASSWORD')
        self.database_password = '123'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', self.database_password, 'localhost:5432', self.database_name) #local database
        setup_db(self.app, self.database_path)

        self.new_user = {
                'id':2,
                'nombre':'sebastian',
                'apellido':'loza',
                'edad':18,
                'sexo':'masculino',
                'usuario':'loza051',
                'contraseña':'1234',
                'date_created':datetime.date.today()
                }

        self.new_user2={
                'nombre':'aaron',
                'apellido':'coorahua',
                'edad':18,
                'sexo':'masculino',
                'usuario':'aaron124',
                'contraseña':'1234',
                'date_created':datetime.date.today()
                }

        self.new_user3={
                'nombre':'aaron',
                'apellido':'coorahua',
                'usuario':'aaronnuevo',
                'edad':18,
                'sexo':'masculino',
                'contraseña':'1234',
                'date_created':datetime.date.today()
                }
        
        self.new_almacen = {
                'user_id':69,
                'nombre' :'almacen test',
                'descripcion' : 'almacen de prueba',
                'capacidad' : 30,
                'date_created':datetime.date.today(),
                'date_modified':datetime.date.today(),    
        }

        self.new_producto ={
                'nombre':'prendarandom',
                'almacen_id':1,
                'descripcion':'almacennuevo',
                'tipo':'deporte',
                'cantidad':1,
                'fecha_ingreso':datetime.date.today(), 
        }


        self.new_transaccion = {

        }

        token = 'stringtoken'

        self.headers = {
            "X-Access-Token": token
        }

    
    def test_create_user_success(self):
        res = self.client().post('/users',json=self.new_user3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_user'])

    def test_get_users_success(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_users'])
        self.assertTrue(len(data['users']))



    def test_get_users_failed(self):
        res = self.client().get('/users/?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    

    
    def test_get_almacenes_success(self):
        self.client().post('/almacenes',json=self.new_almacen)
        res=self.client().get('/almacenes')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_almacenes'])
        self.assertTrue(len(data['almacenes']))
    
    def test_get_almacenes_failed(self):
        res = self.client().get('/almacenes/?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
 
    

    def test_create_user_failed(self):
        res = self.client().post('/users',json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocesable')

    def test_create_user_failed_existente(self):
        res = self.client().post('/users',json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,406)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not accepted')
    
    def test_get_almacenes_by_user(self):
        res=self.client().get('/users/69/almacenes',headers={"X-Access-Token": token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
     
 
    
    def test_get_almacenes_by_user_failed(self):
        res = self.client().get('users/1/almacenes/?page=10000',headers={"X-Access-Token": token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_get_almacenes_by_user_unauthorized(self):
        self.client().get('/users/1/almacenes', json = self.new_almacen)
        res = self.client().get('/users/1/almacenes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_get_productos(self):
        res = self.client().get('/productos',headers={"X-Access-Token": token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_get_productos_unauthorized(self):
        self.client().post('/productos', json = self.new_producto)
        res = self.client().get('/productos')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_get_productos_failed(self):
        res = self.client().get('/productos/?page=10000',headers={"X-Access-Token": token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_productos_by_almacen_unauthorized(self):
        self.client().post('/almacenes/1/productos', json = self.new_producto)
        res = self.client().get('/almacenes/1/productos')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_get_transacciones_unauthorized(self):
        res = self.client().get('/productos/1/transacciones')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')


    def test_create_almacen_succes(self):
        res = self.client().post('/users/69/almacenes',json=self.new_almacen,headers={"X-Access-Token": token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_create_almacen_failed(self):
        res = self.client().post('/users/1/hola',headers={"X-Access-Token": token})
        data = json.loads(res.data)


        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_create_almacen_unauthorized(self):
        res = self.client().post('/users/69/almacenes',json=self.new_almacen)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')


    def test_create_product_success(self):
        res = self.client().post('/almacenes/1/productos',json=self.new_producto,headers={"X-Access-Token": token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
     

    def test_create_product_unauthorized(self):
        res = self.client().post('/almacenes/1/productos',json=self.new_producto)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_create_transaccion_unauthorized(self):
        res = self.client().post('/productos/1/transacciones',json=self.new_transaccion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_patch_producto(self):
        res = self.client().patch("/almacenes/1/productos/1", json = {'cantidad':2},headers={"X-Access-Token": token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_patch_producto_unauthorized(self):
        res = self.client().patch("/almacenes/1/productos/3", json = {'cantidad':10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')
       

    def test_delete_producto_from_almacen_unauthorized(self):
        res = self.client().delete('/almacenes/1/productos/2')
        data = json.loads(res.data)
        almacen = Almacen.query.filter(Almacen.id==1).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unauthorized')

    def test_post_user_unprocesable(self):
        res = self.client().post("/users", json={'data':'data1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unprocesable')

    def test_delete_success(self):
        deleted_id=4
        res = self.client().delete('/users/'+str(deleted_id)) 
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted_user_id'])
        self.assertTrue(data['users'])

    def test_delete_users_failed(self):
        res = self.client().delete('/users/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
  
    def tearDown(self):
        return super().tearDown()


