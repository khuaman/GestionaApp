<h1 align="center"> Gestiona App </h1>

## Almacenes-API-ProyectoDBP
Proyecto 2 del curso Desarrollo Basado en Plataformas a cargo del profesor Marvin Abisrror.

<img src="/images/readme/GestionaApp.jpg" alt="Logo"/>


### Integrantes
- Kevin Abraham Huaman Vega 100%
- Sebastián Loza Mendoza 100%
- Rubén Aaron Coorahua Peña 100%

## Descripción del proyecto


Gestiona App consiste en un gestor de almacenes web, es decir, una página web que sirve para la gestión de almacenes. Allí podrás registrar tus almacenes, lo que guardarás, lo que retirarás, etc. 
Gestiona App consiste en una página web que simule un gestor de almacenes, es decir, que permiteque los usuarios puedan tener un manejo de sus almacenes, lo que tienen allí, lo que sale de allí, lo que ellos ingresan, etc., desde nuestra página web. La página también permite que usuarios que no sean dueños de los almacenes que se tienen registrados puedan ingresar, pero como clientes, es decir, este tipo de usuarios podrán acceder a los almacenes para comprar o pedir información sobre los productos que los usuarios dueños tengan en sus almacenes y que permiten que sean visibles al público general. Para esto la página se encargará de registrar a las personas que ingresen a la misma, ya que deberán que tener una cuenta.

Este proyecto maneja la licencia MIT por lo que es libre de modificar este código siempre y cuando brinde las atribuciones correspondientes. 

### Mision:
Hacer sencilla la gestión de almacenes. 

### Vision:
Ser la app más importante y utilizada para la gestión de almacenes a nivel mundial.

## Estructura de archivos
```
Almacenes-API-ProyectoDBP/
|__ backend/
|   |__ __pycache__/
|   |__ server/
|   |   |__ __pycache__/
|   |__ models.py
|   |__ testcase_almacenesapp.py 
|__ frontend/
|   |__ almacenesapp/
|   |   |__ node_modules/
|   |   |__ public/
|   |   |   |__ favicon.ico
|   |   |   |__ index.html
|   |   |__ src/
|   |   |   |__ assets/
|   |   |       |__ cajas.png
|   |   |       |__ CAJASFILA.jgp
|   |   |       |__ fondo-registro.jgp
|   |   |       |__ GestionaAPP.jpg
|   |   |       |__ GestionaAPP.png
|   |   |       |__ logo.png
|   |   |       |__ PEOPLE.jpg
|   |   |       |__ persona.jpg
|   |   |       |__ ware.jpg
|   |   |       |__ WAREHOUSE.jpeg
|   |   |__ components/
|   |   |   |__ NotFound.vue
|   |   |__ router/
|   |   |   |__ index.js
|   |   |__ views/
|   |       |__ AlmacenesDetails.vue
|   |       |__ Almacenes.vue
|   |       |__ ComprasProductos.vue
|   |       |__ HomeView.vue
|   |       |__ Login.vue
|   |       |__ Register.vue
|   |__ app.vue
|   |__ .gitignore
|   |__ babel.config.js
|   |__ jsconfig.json
|   |__ package-lock.json
|   |__ packege.json
|   |__ README.md
|   |__ vue.config.js
|__ images/
|   |__ GestionaApp.jpg    
|__ .gitignore
|__ README.md
|__ requirements.txt					
```
## Tecnologías usadas:
_Fronend_ : Vue js

_Backend_ : Flask, SQLAlchemy, Werkzeug, JWT

_Testing_ : Unittest

#### **Vue js**
Es un framework de JavaScript de _código abierto_ para la construcciń de interfases de usuario y aplicaciones. 

Maneja la licencia MIT y su creador es Evan You. Puedes leer más acerca de [Vue](https://vuejs.org) en su web oficial.

#### **Flask**
**Flask** es un *microframework* que está escrito en python y nos ayuda a poder crear un servidor para páginas web con python. **Flask** funciona bajo el patrón *MVC* (Modelo Vista Controlador) y nos presta muchas funcionalidades para nuestra página web. También te da la opción de agregarle muchas funcionalidades con extensiones o plugins que, si bien no vienen integradas con Flask, las puedes integrar externamente y seguir trabajando con el mismo Flask pero con más funcionalidades.  Una de estas extensiones es SQLAlchemy. 

Puedes buscar más información acerca de [Flask](https://flask.palletsprojects.com/en/2.1.x/) en su página oficial.

#### **SQLAlchemy:**
Esta es la ORM (*Object Relational Mapper)* que se usa en Python para poder trabajar desde python e interactuar con nuestra base de datos. Es muy flexible con SQL, es decir, que nos permite usar cualquier dialecto de SQL, ya sea **Postgres**, **MySQL**, **SQLLite**, etc. 

Para más información puedes visitar la página de [SQLAlchemy](https://www.sqlalchemy.org/).

#### **Werkzeug:**
Werkzeug es una colección de librerias que se pueden usar para crear una aplicación web compatible con WSGI (Web Server Gateway Interface) en Python.Se necesita un servidor WSGI (Web Server Gateway Interface) para las aplicaciones web de Python, ya que un servidor web no puede comunicarse directamente con Python. WSGI es una interfaz entre un servidor web y una aplicación web hecha en Python. Werkzeug proporciona la siguiente funcionalidad (que utiliza Flask):
- Procesamiento de solicitudes
- Manejo de respuestas
- Enrutamiento de URL
- software intermedio
- Utilidades HTTP
- Manejo de excepciones

Para más información puede revisar la documentacion de [Werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/).

#### **JWT**
JWT (JSON Web Token) es un estándar qué está dentro del documento RFC 7519. En el mismo se define un mecanismo para poder propagar entre dos partes, y de forma segura, la identidad de un determinado usuario, además con una serie de claims o privilegios. Estos privilegios están codificados en objetos de tipo JSON, que se incrustan dentro de del payload o cuerpo de un mensaje que va firmado digitalmente. y dependiendo del tipo de cuenta podrán ingresar con un rol u otro.

Para más información puede revisar la documentación de [JWT](https://jwt.io)

#### **Unittest**
Unittest es un framework que ofrece marco de pruebas de código automatizado. El motivo de su utilización es que "Ningún buen desarrollador implementa código sin realizar pruebas exhaustivas". 

Para más información puede revisar la documentación de [Unittest](https://docs.python.org/3/library/unittest.html)

## **Modelos usados**
En el archivos _models.py_ tenemos las siguientes los modelos usados representados en las siguientes clases:

#### Class User
Esta clase representa al usuario y a las operaciones que podemos hacer con este dato como:
##### set_password
Set_password hashea la contraseña dada por el usuario y la almacena en la base de datos.
##### check_password
Check_password compara la contraseña dada con la contraseña haseada y guardada en la base de datos.
##### format
Retorna un diccionario con algunos datos del usuario.
##### insert
Inserta un usuario en la base de datos. Retorna error si es que el usuario se encuentra registrado previamente.
##### update
Actualiza los datos del usuario.
##### get_by_id
Retorna el usuario buscado por id.
##### get_by_usuario
Retorna el usuario buscado por username.

#### Class Almacen
Esta clase representa al almacen y a las operaciones que podemos hacer con este dato como:
##### format
Retorna un diccionario con algunos datos del almacén.
##### insert
Inserta un almacen en la base de datos.
##### update
Actualiza los datos del almacén.
##### delete
Elimina un almacén y su contenido, es decir, los elementos que contiende.
##### get_almacen_by_id
Retorna el almacen buscado por id.

#### Class Producto
Esta clase representa al producto que se encuentra dentro de un almacén y a las operaciones que podemos hacer con este dato como:
##### insert 
Inserta un producto dentro de un almacén en la base de datos.
##### update
Actualiza los datos del producto (cantidad).
##### delete
Elimina un determinado producto, es decir, todas las unidades de un producto que se encuentren dentro de un determinado almacén.
##### format
Retorna un diccionario con algunos datos del producto. y dependiendo del tipo de cuenta podrán ingresar con un rol u otro.
##### get_producto_by_nombre
Retorna el producto buscado por el nombre del producto.

#### Class Transaccion
Esta clase representa las transacciones que se pueden generar como los ingresos y salidas de productos. Tiene los siguientes métodos.
##### format
Retorna un diccionario con algunos datos de la transacción.
##### insert
Inserta una transacción dentro de la base de datos.
##### update
Actualiza los datos de la transacción.
##### delete
Elimina una determinada transacción.

## **API**
La API, hecha en el archivo **__init__.py**  contiene todas las funciones que permiten el funcionamiento de nuestra app.
#### paginate
Devuelve la data por página con el fin de poder listar de una manera más amigable los datos a presentarse en pantalla.
#### create_app
Permite crear la app
#### token_required
Si la sesión ya expiró, retorna que la sesión ha concluído. Si la sesión continúa activa, devuelvela data

## **Testing** 

Usando la librería _unittest_ de python, en el archivo __testcase_almacenesapp.py__ creamos el testing de los endpoints que usamos en nuestra app. 

### class TestCaseTodoApp(unittest.TestCase):
#### def setUp(self):
Con esta función creamos la app y la conectamos a nuestra base de datos de PostgresQL. 
#### def test_get_users_success(self):
Con esta función probamos la obtención de usuario con una entrada correcta se está ejecutando correctamente.
#### def test_get_users_failed(self):
Con esta función probamos la obtención de usuario con una entrada incorrecta se está ejecutando correctamente, es decir, retorna el error esperado.
#### def test_get_almacenes(self):
Con esta función probamos la obtención de almacenes con una entrada correcta se está ejecutando correctamente.
#### def test_get_almacenes_failed(self):
Con esta función probamos la obtención de almacenes con una entrada incorrecta se está ejecutando correctamente, es decir, retorna el error esperado.
#### def test_create_user_success(self):
Con esta función probamos la creación de usuarios con una entrada correcta se está ejecutando correctamente.
#### def test_create_user_failed(self):
Con esta función probamos la creación de usuarios con una entrada incorrecta se está ejecutando correctamente, es decir, retorna el error esperado.
#### def test_create_user_failed_existente(self):
Con esta función probamos la creación de usuarios con una entrada incorrecta se está ejecutando correctamente, es decir, retorna el error esperado, pues el usuario ingresa un username ya registrado en nuestra base de datos.
#### def test_get_almacenes_by_user_unauthorized(self):
Con esta función probamos la obtención de almacenes con un usuario no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### def test_get_productos_unauthorized(self):
Con esta función probamos la obtención de productos con un usuario y almacén no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### def test_get_productos_by_almacen_unauthorized(self):
Con esta función probamos la obtención de productos por almacén no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### def test_get_transacciones_unauthorized(self):
Con esta función probamos la obtención de transacciones por un producto no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### def test_create_almacen_unauthorized(self):
Con esta función probamos la creación de almacenes por usuario no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### test_create_product_unauthorized(self):
Con esta función probamos la creación de productos para un almacén no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 
#### def test_create_transaccion_unauthorized(self):
Con esta función probamos la creación de transacciones para un productoc no autorizado se está ejecutando correctamente, es decir, retorna el error esperado. 

### Manejo de errores
#### Error 500
Internal server error. Quiere decir que ha sucedido un error al intentar acceder al servidor, pero no se puede dar mas detalles sobre lo que ha ocurrido.
#### Error 406
Not Acceptable. Quiere decir que el cliente ha enviado una petición válida al servidor, pero la petición incluía un requisito especial que el servidor debía seguir. Ese requisito especial en la solicitud inicial estaba en la forma de una cabecera HTTP Accept-.
#### Error 404
Not found. Quiere decir que la URL a acceder no existe.
#### Error 422
Unprocessable Entity. Quiere decir que el servidor entiende tu petición, pero no puede cumplirla debido a un problema de tu parte. Si solucionas ese problema, deberías poder recargar la página y el error desaparecerá.
#### Error 401
Unauthorized. Quiere decir que el usuario no está autorizado para acceder a la página solicitada.
### Status code
#### 200
Ok. Quiere decir que la solicitud se ha generado con éxito.


## Frontend
### HomeView.vue
Esta es la página de presentación del proyecto donde contiene el propósito del mismo y redirecciones al login y register.
### Login.vue
Esta página contiene un formulario de ingreso a la app donde se obtendrá el usuario y contraseña para accerder a la misma.
### Register.vue
Esta página contiene un formulario de registro a la app donde se obtendrá datos como nombres, apellidos, edad, género, usuario y contraseña.
### Almacenes.vue
Esta página lista los almacenes que posee el usuario logeado. Permite agregar un nuevo almacén y eliminar los existentes, así como ingresar a la página _AlmacenesDetails.vue_ para ver el contenido de cada almacén.
### AlmacenesDetails.vue
En esta página se logra ver los productos que contienen un almacén y realizar operaciones como insertar productos, agregar o disminuir productos, y eliminar productos.
### ComprasProductos.vue
Esta página funciona como marketplace donde se podrá observar los productos de los almacenes de otro usuario. El usuario tendrá que habilitar el almacén que se busca agregar al marketplace para hacerlo visible en el mismo. 
### App.vue
Esta página conecta las anteriormente listadas para ser utilizada por vue. Recordemos que vue procesa la página web en forma de una sola página, como si estuviese contenido en el mismo archivo.

## License

The MIT License (MIT)

MIT License

Copyright (c) [2021] [Gestiona Team]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Made with &#10084; by GestionaTeam


_Proyecto terminado_
