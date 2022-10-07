import datetime
from sqlalchemy.sql import func
from dotenv import load_dotenv
from flask import (
        Flask,
        request,
        jsonify,
        abort
        )
from flask_cors import CORS
from models import setup_db, User, Almacen, Producto, Transaccion, db
from functools import wraps
import jwt
from models import secret_key

DATA_PER_PAGE = 5

def paginate(request, selection):
    page = request.args.get('page', 1, type = int)
    start = (page - 1)*DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    data = [data.format() for data in selection]
    current_data = data[start:end]
    return current_data


def create_app(test_config = None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=['http://localhost:8080'])

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            error_401 = False
            print(request.headers)
            if 'X-Access-Token' in request.headers:
                token = request.headers['X-Access-Token']

            if not token:
                error_401 = True
                abort(401)

            try:
                #data = jwt.decode(token, secret_key, algorithms=["HS256"])
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

                current_user = User.query.filter(User.id==data['user_id']).one_or_none()
            except Exception as e:
                print('error:',e)
                if error_401:
                    abort(401)
                else:
                    return jsonify({
                        'success':False,
                        'message':"Token expired"
                        })
            return f(current_user, *args, **kwargs)

        return decorated
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/user', methods = ['GET'])
    def get_user_by_token():
        token = None
        error_401 = False
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        if not token:
            error_401 = True
            abort(401)

        try:
            #data = jwt.decode(token, secret_key, algorithms=["HS256"])
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter(User.id==data['user_id']).one_or_none()
            if current_user is None:
                error_401=True
                abort(401)

            return jsonify({
                'success':True,
                'profile':current_user.format()
                })

        except Exception as e:
            print(e)
            if e == "Signature has expired":
                return jsonify({
                    'success':False,
                    'message':"Token expired"
                    })
            if error_401:
                abort(401)
            else:
                abort(500)

    @app.route('/login', methods=['POST'])
    def login():
        error_403=False
        try:
            
            data = request.get_json()
            usuario = data.get('usuario', None)
            contraseña = data.get('contraseña', None)
            remember_me = data.get('remember_me', None)

            user = User.query.filter(User.usuario==usuario).one_or_none()
            if user is None:
                error_403=True
                abort(403)

            if user.check_password(contraseña):
                #token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, secret_key)
                token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config["SECRET_KEY"])
                return jsonify({
                    'success':True,
                    'profile':user.format(),
                    'token':token
                    })
            else:
                error_403=True
                abort(403)

        except Exception as e:
            print(e)
            if error_403:
                abort(403)
            else:
                abort(500)

    @app.route("/logout", methods=['GET'])
    def logout():
        return jsonify({
            'success':True
            })

    
    @app.route('/users', methods=['GET'])
    def get_users():
        error_404=False
        try:
            users = User.query.order_by('id').all()

            if len(users) == 0:
                error_404 = True
                abort(404)
            
            users = [user.format() for user in users]
            return jsonify({
                'success': True,
                'users': users,
                'total_users':len(users)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/almacenes', methods=['GET'])
    def get_almacenes():
        error_404 = False
        try:
            almacenes = {almacen.id:almacen.format() for almacen in Almacen.query.order_by('id').all()}

            if len(almacenes) ==0:
                error_404 = True
                abort(404)

            return jsonify({
                'success':True,
                'almacenes':almacenes,
                'total_almacenes':len(almacenes)
                })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/users/<user_id>/almacenes', methods=['GET'])
    
    @token_required
    def get_almacen_by_user(current_user, user_id):
        error_404=False
        nombre = current_user.nombre
        try:
            user=User.query.filter(User.id==user_id).one_or_none()
            selection = user.almacenes
            almacenes = paginate(request, selection)
            if len(almacenes) ==0:
                error_404 = True
                abort(404)
            
            return jsonify({
                'success':True,
                'user_id':user_id,
                'nombre_usuario':nombre,
                'almacenes':almacenes,
                'total_almacenes':len(almacenes)
                })


        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/productos', methods=['GET'])
    @token_required
    def get_productos(current_user):
        error_404 = False
        try:
            almacenes = []
            subquery = Almacen.query.filter(Almacen.user_id == current_user.id).all()
            for almacen in subquery:
                almacenes.append(almacen.id)
            selection = Producto.query.filter(Producto.almacen_id.not_in(almacenes)).filter(Producto.venta).order_by('id').all()
            productos = paginate(request, selection)

            if len(productos) == 0:
                error_404 = True
                abort(404)

            return jsonify({
                'success':True,
                'user_id':current_user.id,
                'productos':productos,
                'total_productos':len(selection)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/almacenes/<almacen_id>/productos', methods=['GET'])
    @token_required
    def get_productos_by_almacen(current_user, almacen_id):
        error_404=False
        try:
            almacenes=Almacen.query.filter(Almacen.id==almacen_id).one_or_none()
            selection = almacenes.productos
            productos = paginate(request, selection)

            if len(productos) ==0:
                error_404 = True
                abort(404)
            
            return jsonify({
                'success':True,
                'almacen_id':almacen_id,
                'productos':productos,
                'total_productos':len(selection)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/productos/<producto_id>/transacciones', methods=['GET'])
    @token_required
    def get_transacciones(producto_id):
        error_404=False
        try:
            producto = Producto.query.filter(Producto.id==producto_id).one_or_none()
            transacciones = {transaccion.id:transaccion.format() for transaccion in producto.transacciones}
            if producto is None or len(transacciones)==0:
                error_404=True
                abort(404)

            return jsonify({
                'success':True,
                'producto_id':producto_id,
                'transacciones':transacciones,
                'total_transacciones':len(transacciones)
                })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)



    ##POSTS
    
    #POST para la creación de un nuevo usuario
    @app.route('/users', methods=['POST'])
    def create_user():
        error_422 = False
        error_406 = False
        try:
            users=request.get_json()
            nombre=users.get('nombre',None)
            apellido=users.get('apellido',None)
            usuario=users.get('usuario', None)
            edad=users.get('edad',None)
            sexo = users.get('sexo',None)
            contraseña =users.get('contraseña', None)
            search = users.get('search', None)
            date_created = datetime.date.today()
            if search is not None:
                user = User.query.filter(User.id==search).one_or_none()
                return jsonify({
                    'success':True,
                    'user':user.format()
                    })

            if nombre is None or apellido is None or edad is None or sexo is None or usuario is None:
                error_422 = True
                abort(422)
            user=User(nombre=nombre,apellido=apellido,edad=edad,sexo=sexo, usuario=usuario,date_created=date_created)
            user.set_password(contraseña)
            user_id = user.insert()
            if user_id == "Existente":
                error_406 = True 
                abort(406)
            new_user = User.query.filter(User.id==user_id).one_or_none()
            selection = User.query.order_by('id').all()
            print("antes del toquen")
            token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, secret_key)
            print(token)
            #token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])
            return jsonify({
                'success':True,
                'created':new_user.format(),
                'total_user':len(selection),
                'token':token
            })
        except Exception as e:
            if error_422:
                abort(422)
            elif error_406:
                abort(406)
            else:
                abort(500)


    
    #POST para la creación de un nuevo almacen de un usuario
    @app.route('/users/<user_id>/almacenes', methods=['POST'])
    @token_required
    def create_almacen(current_user, user_id):
        error_406 = False
        error_422 = False
        try:
            almacenes=request.get_json()
            nombre=almacenes.get('nombre',None)
            descripcion=almacenes.get('descripcion',None)
            capacidad=almacenes.get('capacidad',None)
            search = almacenes.get('search', None)
            date_created = datetime.date.today()
            if search is not None:
                almacen = Almacen.query.filter(Almacen.id==search).one_or_none()
                return jsonify({
                    'success':True,
                    'almacen':almacen.format()
                    })
            if descripcion is None or nombre is None or capacidad is None:
                error_422 = True
                abort(422)
            almacen=Almacen(user_id=user_id,nombre=nombre,descripcion=descripcion,capacidad=capacidad,date_created=date_created, date_modified=date_created)
            almacen_id = almacen.insert()
            if almacen_id == "Existente":
                error_406 = True 
                abort(406)
            new_almacen = Almacen.query.filter(Almacen.id==almacen_id).one_or_none()
            user = User.query.filter(User.id == user_id).one_or_none()
            selection = user.almacenes
            almacenes = paginate(request, selection)
            
            return jsonify({
                'success':True,
                'created':new_almacen.format(),
                'almacenes':almacenes
            })

        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            elif error_406:
                abort(406)
            else:
                abort(500)



    #POST para la creación de un nuevo producto de un almacen
    @app.route('/almacenes/<almacen_id>/productos', methods=['POST'])
    @token_required
    def create_producto(current_user, almacen_id):
        error_422 = False
        error_406 = False
        try:
            producto=request.get_json()
            nombre=producto.get('nombre',None)
            descripcion=producto.get('descripcion',None)
            tipo=producto.get('tipo',None)
            cantidad = producto.get('cantidad',None)
            search = producto.get('search', None)
            date_created = datetime.date.today()
            if search is not None:
                producto = Producto.query.filter(Producto.id==search).one_or_none()
                return jsonify({
                    'success':True,
                    'almacen':producto.format()
                    })
            if descripcion is None or nombre is None or cantidad is None or tipo is None:
                error_422 = True
                abort(422)

            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()

            capacidad = db.session.query(func.sum(Producto.cantidad)).filter(Producto.almacen_id==almacen_id).scalar()
            print(capacidad)
            if capacidad is None:
                if cantidad <=almacen.capacidad:
                    producto=Producto(almacen_id=almacen_id,nombre=nombre,descripción=descripcion,cantidad=cantidad,tipo=tipo,fecha_ingreso=date_created, venta=False)
                else:
                    error_406 = True
                    abort(406)
            elif capacidad+cantidad <= almacen.capacidad:
                producto=Producto(almacen_id=almacen_id,nombre=nombre,descripción=descripcion,cantidad=cantidad,tipo=tipo,fecha_ingreso=date_created, venta=False)
            else:
                error_406 = True
                abort(406)
            producto_id = producto.insert()
            new_producto = Producto.query.filter(Producto.id==producto_id).one_or_none()
            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()
            selection = almacen.productos
            productos = paginate(request, selection)
            return jsonify({
                'success':True,
                'created':new_producto.format(),
                'productos':productos
            })
        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            elif error_406:
                abort(406)
            else:
                abort(500)


      
    #POST para la creación de una nueva transacción de un producto
    @app.route('/productos/<producto_id>/transacciones', methods=['POST'])
    @token_required
    def create_transaccion(current_user, producto_id):
        error_422=False
        error_404=False
        try:
            producto=Producto.query.filter(Producto.id==producto_id).one_or_none()
            if producto is None:
                error_404=True
                abort(404)
            transaccion=request.get_json()
            tipoDocumento=transaccion.get('tipoDocumento',None)
            idProducto=transaccion.get('idProducto',None)
            cantidad=transaccion.get('cantidad',None)
            if tipoDocumento is None or idProducto is None:
                error_422=True
                abort(422)
            fechaDoc = datetime.date.today()
            if tipoDocumento == "Agregar":
                tipoDocumento = 'NI'
            else:
                tipoDocumento = 'NS'
            transaccion = Transaccion(tipoDocumento=tipoDocumento, fechaDoc=fechaDoc, producto=producto, cantidad=cantidad)
            transaccion_id = transaccion.insert()
            new_transaccion = Transaccion.query.filter(Transaccion.id==transaccion_id).one_or_none()
            selection = Transaccion.query.order_by('id').all()
            return jsonify({
                'success':True,
                'created':new_transaccion.format(),
                'total_transacciones':len(selection)
            })
        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            elif error_404:
                abort(404)
            else:
                abort(500)


    
    ##DELETES's


    @app.route('/users/<user_id>',methods=['DELETE'])
    def delete_users(user_id):
        error_404=False
        try:
            user=User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                error_404=True
                abort(404)
            user.delete()
            users = {user.id:user.format() for user in User.query.order_by('id').all()}
            return jsonify({
                'success':True,
                'deleted_user_id':user_id,
                'users':users,
                'total_users':len(users)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/users/<user_id>/almacen/<almacen_id>', methods = ['DELETE'])
    @token_required
    def delete_almacen_from_user(create_user, user_id, almacen_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                error_404 = True
                abort(404)
            almacen = Almacen.query.filter(Almacen.user_id ==user_id).filter(Almacen.id == almacen_id).one_or_none()
            if almacen is None:
                error_404 = True
                abort(404)
            nombre_user= user.nombre
            almacen.delete()

            user = User.query.filter(User.id == user_id).one_or_none()
            selection = user.almacenes
            almacenes = paginate(request, selection)

            return jsonify({
                'success':True,
                'deleted_almacen_id':almacen_id,
                'nombre_user':nombre_user,
                'almacenes': almacenes,
                'total_almacens':len(selection)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/almacenes/<almacen_id>/productos/<producto_id>', methods = ['DELETE'])
    @token_required
    def delete_producto_from_almacen(current_user, producto_id, almacen_id):
        error_404 = False
        try:
            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()
            if almacen is None:
                error_404 = True
                abort(404)
            producto = Producto.query.filter(Producto.almacen_id ==almacen_id).filter(Producto.id == producto_id).one_or_none()
            if producto is None:
                error_404 = True
                abort(404)
            nombre_almacen = almacen.nombre
            producto.delete()

            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()
            selection = almacen.productos
            productos = paginate(request, selection)

            return jsonify({
                'success':True,
                'deleted_producto_id':producto_id,
                'nombre_almacen':nombre_almacen,
                'productos': productos,
                'total_productos':len(selection)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/productos/<producto_id>/transacciones/<transaccion_id>', methods = ['DELETE'])
    @token_required
    def delete_transaccion_from_producto(current_user, producto_id, transaccion_id):
        error_404 = False
        try:
            producto = Producto.query.filter(Producto.id == producto_id).one_or_none()
            if producto is None:
                error_404 = True
                abort(404)
            transaccion = Transaccion.query.filter(Transaccion.idProducto ==producto_id).filter(Transaccion.id == transaccion_id).one_or_none()
            if transaccion is None:
                error_404 = True
                abort(404)

            nombre_producto = producto.nombre
            transaccion.delete()

            transacciones = {transaccion.id:transaccion.format() for transaccion in Transaccion.query.order_by('id').all()}

            return jsonify({
                'success':True,
                'deleted_producto_id':producto_id,
                'nombre_producto':nombre_producto,
                'transacciones': transacciones,
                'total_productos':len(transacciones)
                })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #Update User
    @app.route('/users/<user_id>', methods = ['PATCH'])
    @token_required
    def Update_user(current_user, user_id):
        error_404 = False
        error_422 = False
        updated=False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if(user is None):
                error_404 = True
            input_json = request.get_json(force = True)
            if('usuario' in input_json):
                updated=True
                user.usuario = input_json['usuario']

            if not updated:
                error_422=True
                abort(422)
             
            user.update()
            usuario = User.query.filter(User.id == user_id).one_or_none()
 
            return jsonify({
                'success': True,  
                'usuario':usuario.format()
                })
        except Exception as e:
            print(e)
            if(error_404):
                abort(404)
            elif error_422:
                abort(422)
            else:
                abort(500)

#   Update Producto específico
    @app.route('/almacenes/<almacen_id>/productos/<producto_id>', methods = ['PATCH'])
    @token_required
    def Update_product(current_user, almacen_id,producto_id):
        error_404 = False
        error_422=False
        error_406=False
        updated = False
        user_id = current_user.id
        try:
            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none() 
            producto = Producto.query.filter(Producto.id == producto_id).filter(Producto.almacen_id == almacen_id).one_or_none()
            if(almacen is None):
                error_404 = True

            if(producto is None):
                error_404 = True

            input_json = request.get_json(force = True)
            if ('venta' in input_json):
                print(producto.venta)
                venta = producto.venta
                producto.venta = not venta
                updated = True
                    
                almacen.date_modified = datetime.date.today()
                almacen.update()
                producto.update()
                
                almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()
                producto = Producto.query.filter(Producto.id == producto_id).filter(Producto.almacen_id == almacen_id).one_or_none()
                selection = almacen.productos
                productos = paginate(request, selection)
                return jsonify({
                    'success': True,
                    'user_id':user_id,
                    'almacen_id' : almacen_id,
                    'producto' : producto.format(),
                    'productos':productos
                })

            if('tipo_transaccion' in input_json):
                tipo_transaccion = input_json['tipo_transaccion']
            else:
                error_422 = True
                abort(422)
            if('cantidad' in input_json):
                print("cantidad: ",input_json['cantidad'])
                updated=True
                if tipo_transaccion == "Agregar":
                    cantidad = input_json['cantidad']
                    capacidad = db.session.query(func.sum(Producto.cantidad)).filter(Producto.almacen_id==almacen_id).scalar()
                    if capacidad+cantidad <= almacen.capacidad:
                        producto.cantidad += cantidad
                    else:
                        error_406 = True
                        abort(406)
                else:
                    nueva_cantidad = producto.cantidad - input_json['cantidad']
                    if nueva_cantidad >= 0:
                        producto.cantidad = nueva_cantidad
                    else:
                        error_406 = True
                        abort(406)

            if not updated:
                error_422=True
                abort(422)
                
            almacen.date_modified = datetime.date.today()
            almacen.update()
            producto.update()
            
            almacen = Almacen.query.filter(Almacen.id == almacen_id).one_or_none()
            producto = Producto.query.filter(Producto.id == producto_id).filter(Producto.almacen_id == almacen_id).one_or_none()
            selection = almacen.productos
            productos = paginate(request, selection)
            return jsonify({
                'success': True,
                'user_id':user_id,
                'almacen_id' : almacen_id,
                'producto' : producto.format(),
                'productos':productos
            })

        except Exception as e:
            print(e)
            if(error_422):
                abort(422)
            elif(error_404):
                abort(404)
            elif(error_406):
                abort(406)
            else:
                abort(500)

    #Update Almacenes
    @app.route('/users/<user_id>/almacenes/<almacenes_id>', methods = ['PATCH'])
    @token_required
    def Update_storage(create_user, almacen_id,user_id):
        error_404 = False
        error_422=False
        updated=False
        try:
            user = User.query.filter(User.id == user_id).one_or_none() 
            almacen = Almacen.query.filter(Almacen.id == almacen_id).filter(Almacen.user_id == user_id).one_or_none()
            if(user is None):
                error_404 = True
            if(almacen is None):
                error_404 = True

            input_json = request.get_json(force = True)
            if('capacidad' in input_json):
                updated=True
                almacen.capacidad = input_json['capacidad']
            if('descripcion' in input_json):
                updated=True
                almacen.descricion = input_json['descripcion']
            if('nombre' in input_json):
                updated=True
                almacen.nombre = input_json['nombre']

            if not updated:
                error_422=True
                abort(422)

            almacen.date_modified=datetime.date.today()
            almacen.update()
            
            almacen = Almacen.query.filter(Almacen.id == almacen_id).filter(Almacen.user_id == user_id).one_or_none()
            user = User.query.filter(User.id == user_id).one_or_none()
            selection = user.almacenes
            almacenes = paginate(request, selection)

            return jsonify({
                'success': True,
                'almacen' : almacen.format(),
                'almacenes':almacenes
            })

        except Exception as e:
            if(error_404):
                abort(404)
            else:
                abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'code':404,
            'message':'resource not found'
            }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success':False,
            'code':401,
            'message':'Unauthorized'
            }), 401

    @app.errorhandler(403)
    def forbbiden(error):
        return jsonify({
            'success':False,
            'code':403,
            'message':'Forbiden'
            }), 403

    @app.errorhandler(406)
    def not_accepted(error):
        return jsonify({
            'success':False,
            'code':406,
            'message':'Not accepted'
            }), 406

    @app.errorhandler(422)
    def unprocesable(error):
        return jsonify({
            'success':False,
            'code':422,
            'message':'Unprocesable'
            }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success':False,
            'code':500,
            'message':'Internal server error'
            }), 500

    return app
