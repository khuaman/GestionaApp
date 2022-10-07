<template>
  <div id="main-banner">
    <h1>No te compliques<br />Gestiona</h1>
  </div>
  <section class="inicio" id="inicio">
    <div class="content">
      <h3>GESTION DE<span> ALMACENES</span></h3>
      <p>
        Gestiona App consiste en una página web que simule un gestor de
        almacenes, es decir, permite que los usuarios puedan tener un manejo de
        sus almacenes, lo que tienen allí, lo que sale de allí, lo que ellos
        ingresan, etc., desde nuestra página web.
      </p>
      <a href="#" class="btn">INICIO</a>
    </div>
  </section>
  <body>ejecuta
    <!--BannerPrincipal-->
    <section class="banner">
      <div>
        <div class="contenedor llamada-accion">
          <p>Tus almacenes de confianza</p>
          <h2>GESTIONA APP</h2>
          <a href="#">CONTACTANOS</a>
        </div>
      </div>
    </section>
ejecuta
    <!--Seccion Sobre Nostros-->
    <section class="nosotros">
      <div class="contenedor">
        <div class="foto-equipo">
          <img src="../assets/GestionaApp.png" alt="Foto de clientes" />
        </div>
        <div class="conocenos">
          <p>ÁREA PARA COMERCIANTES</p>
          <h3>Negocia y Gestiona en tiempo record</h3>
          <p>Manten control de tus transacciones</p>
          <p>
            Si eres comerciante de algun producto, tienes tu tienda y buscas un
            lugar donde poder gestionar tu stock... Estás en el lugar adecuado,
            contamos con un sistema de manejo de almacenes para que que puedas
            proveer a tus clientes con una línea completa de productos y obtener
            mayores márgenes de ganancias. Nos caracterizamos por tenerte
            informado siempre sobre los stocks, y sobre todo una rápida
            atención. Obten ahora un precio ESPECIAL de subscripcion inicial,
            dando click en el siguiente botón
          </p>
          <router-link class="btn" to="/login">EMPEZAR</router-link>
        </div>
      </div>
    </section>
    <div class="image">
      <img src="../assets/cajas.png" alt="" />
    </div>

    <!--Seccion Pie de pagina-->
    <footer>
      <div class="top-footer"></div>
      <div class="center-footer">
        <div class="contenedor">
          <div class="widget">
            <h4>MANEJO DE ALMACENES</h4>
            <p>
              Crea almacenes para tu empresa, los cuales podras eliminar y
              editar en el momento que desees. Es importante que respetes la
              cantidad de productos que habrá en tu almacen.
            </p>
          </div>
          <div class="widget">
            <h4>MANEJO DE PRODUCTOS</h4>
            <p>
              Puedes llevar un control de los productos que tengas en los
              diferentes almacenes que hayas creado. Podras editar la cantidad
              de los mismos cuando sea necesario e incluso eliminarlos.
            </p>
          </div>
          <div class="widget">
            <h4>TRANSACCIONES</h4>
            <p>
              lleva control de las transacciones que realizes en los productos
              de tus almacenes. Siempre es importante tener un historial de
              entrada y salida de productos.
            </p>
          </div>
          <div class="widget">
            <h4>Compras</h4>
            <p>
              Tendrás una pestaña de compras, donde podrás negociar con otros
              proveedores e inclusive poner tus propios productos en venta y
              generar más ganancias.
            </p>
          </div>
        </div>
      </div>
      <div class="bottom-footer">
        <p>&copy; Todos los derechos reservados</p>
      </div>
    </footer>
  </body>
</template>

<style scoped>
:root {
  --verde: #0c443a;
  --limon: #25d1b2;
  --red: red;
  --degradado: linear-gradiend(90deg, var(--limon), var(--verde));
}

#main-banner {
  background-image: url("../assets/ware.jpg");
  background-position: 0 -250px;
  background-size: cover;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

#main-banner h1 {
  color: #fff;
  text-align: left;
  font-size: 60 px;
  background-color: #222;
  padding: 20px 40px;
}

section {
  min-height: 100vh;
  padding: 0 9%;
  padding-top: 7.5rem;
  padding-bottom: 2rem;
}

.btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.8rem 3rem;
  border-radius: 5rem;
  background: black;
  font-size: 1.8rem;
  color: white;
  cursor: pointer;
  box-shadow: 0.5rem 1rem rgba(0, 0, 0, 0.1);
  transition: all 0.3s linear;
}

.btn:hover {
  transform: scale(1.1);
}

.inicio {
  display: flex;
  align-items: left;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.inicio .image img {
  width: 40vh;
  animation: float 3s linear infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0rem);
  }
  50% {
    transform: translateY(-3.5rem);
  }
}

.inicio .content h3 {
  font-size: 5.5rem;
  color: #333;
  text-transform: uppercase;
}

.inicio .content h3 span {
  color: #25d1b2;
  text-transform: uppercase;
}

.inicio .content p {
  font-size: 1.7rem;
  color: #666;
  padding: 1rem 0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Open Sans", sans-serif;
}

.contenedor {
  width: 100%;
  max-width: 1170px;

  margin: auto;
}

/*CABECERA*/

header {
  width: 100%;
  height: 200 px;
  background-color: #82b199;
}

.logo {
  padding: 25px 0;
}

.logo img {
  width: 100px;
  display: block;
  margin: auto;
}

.menu {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
  max-width: 430px;
  margin: auto;
}

.menu a {
  text-decoration: none;
  color: #ffffff;
  font-size: 14px;
  padding-bottom: 40px;
}

.menu a:hover {
  color: #00a3ca;
}

/*Fin de CABECERA*/

/*Banner Principal*/

.banner {
  width: 100%;
  height: 500px;
  background-image: url(../assets/PEOPLE.jpg);
  background-position: center;
  background-size: cover;
}

.banner > div {
  width: 100%;
  height: 100%;
}

.llamada-accion {
  text-align: center;
  display: flex;
  flex-flow: column wrap;
  justify-content: center;
  align-items: center;

  height: 100%;
}

.llamada-accion p {
  font-size: 18px;
  color: white;
  text-transform: uppercase;
  margin-top: 150px;
}

.llamada-accion h2 {
  font-size: 42px;
  color: white;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.4);
  max-width: 600px;
  margin: auto;
}

.llamada-accion a {
  font-size: 18px;
  text-decoration: none;
  color: white;
  padding: 10px 50px;
  background-color: rgba(39, 198, 0, 1);
  margin-bottom: 80px;
  transition: all 0.3s ease-in-out;
}

.llamada-accion a:hover {
  background-color: rgba(24, 120, 0, 0.8);
}

/*Bienvenida*/

.bienvenida {
  width: 100%;
  background-color: #3e606f;
  margin-top: 2 px;
  color: #ffffff;
  text-align: center;
}

.bienvenida h3 {
  font-size: 16px;
  padding-top: 40px;
  padding-bottom: 35px;
}

.bienvenida p {
  font-size: 16px;
  padding-bottom: 35px;
  line-height: 1.7em;
  max-width: 370;
  margin: 0 auto;
}

/*Fin Bienvenida*/

.nosotros > .contenedor {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}

.foto-equipo {
  width: 100%;
  max-width: 500px;
}

.foto-equipo img {
  width: 100%;
}

.conocenos {
  text-align: center;
  padding: 15px 0px;
  max-width: 570px;
}

.conocenos p:nth-child(1) {
  font-size: 14px;
  color: #3c1c22;
  padding-bottom: 20px;
  border-bottom: 1px solid #a2a2a2;
}

.conocenos h3 {
  padding-top: 20px;
  padding-bottom: 30px;
  color: #0e96dd;
  font-size: 18px;
}

.conocenos p:nth-child(3) {
  font-size: 14px;
  color: #3c1c22;
  padding-bottom: 25px;
}

.conocenos p:nth-child(4) {
  font-size: 14px;
  color: #646464;
  padding-bottom: 20px;
}

.conocenos a {
  font-size: 15px;
  color: #0e96dd;
}

@media all and(min-width:769px) {
  .nosotros {
    padding-top: 80px;
  }
  .foto-equipo {
    margin-right: 30px;
  }
  .conocenos {
    margin-left: 30px;
    text-align: left;
  }
}

/*Pied de pagina*/

.top-footer {
  background-color: #193441;
  height: 25px;
}

.center-footer {
  background-color: #152d37;
}

.center-footer .contenedor {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.center-footer .widget {
  text-align: center;
  padding-top: 20px;
  padding-bottom: 35px;
  color: #7a7a7a;
  max-width: 270px;
  margin: 0 auto;
}

.center-footer .widget h4 {
  padding-bottom: 35px;
  font-size: 18px;
}

.center-footer .widget p {
  font-size: 14px;
}

.bottom-footer {
  background-color: #193441;
  height: 25px;
}

.bottom-footer p {
  color: #7a7a7a;
  font-size: 12px;
  text-align: center;
}
</style>

<script>
// @ is an alias to /src

export default {
  name: "HomeView",
};
</script>
