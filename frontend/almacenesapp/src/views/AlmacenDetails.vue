<template>
  <body>
    <div class="container_body">
      <div class="container_links">
        <h4>Links</h4>
        <ul>
          <li class="links">
            <router-link :to="{ name: 'home' }">Home</router-link>
          </li>
          <li class="links"><a href="#" @click="logout">Logout</a></li>
          <li class="links">
            <router-link :to="{ name: 'Almacen', params: { user_id: user_id } }"
              >Almacenes</router-link
            >
          </li>
        </ul>
      </div>
      <div class="container_page">
        <div class="container">
          <h1>Bienvenido a tu almacen "{{ almacen.nombre }}"</h1>
          <table class="container-table">
            <thead>
              <tr>
                <td scope="col"><h6>#</h6></td>
                <td scope="col"><h6>NOMBRE</h6></td>
                <td scope="col"><h6>DESCRIPCION</h6></td>
                <td scope="col"><h6>TIPO</h6></td>
                <td scope="col"><h6>CANTIDAD</h6></td>
                <td scope="col"><h6>FECHA_INGRESO</h6></td>
                <td scope="col"><h6>EN VENTA</h6></td>
                <td scope="col"><h6>EDITAR</h6></td>
                <td scope="col"><h6>ELIMINAR</h6></td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="producto in productos" :key="producto.id">
                <td class="producto_id">{{ producto.id }}</td>
                <td class="nombre">{{ producto.nombre }}</td>
                <td class="descripcion">{{ producto.descripcion }}</td>
                <td>{{ producto.tipo }}</td>
                <td ref="{{producto.id}}">{{ producto.cantidad }}</td>
                <td>{{ producto.fecha_ingreso }}</td>
                <td
                  class="venta_t"
                  @click="cambiar_venta"
                  v-if="producto.en_venta"
                >
                  <i id="venta_t" class="bi bi-circle-fill"></i>En venta
                </td>
                <td class="venta_t" @click="cambiar_venta" v-else>
                  <i id="venta_f" class="bi bi-circle-fill"></i>No en venta
                </td>
                <td class="opciones">
                  <button @click="eliminar">
                    <i class="bi bi-trash3-fill"></i>
                  </button>
                </td>
                <td class="opciones">
                  <button @click="abrir_editar()">
                    <i class="bi bi-pencil"></i>
                  </button>
                </td>
                <div
                  v-if="!editar"
                  id="modal-container"
                  class="modal_container"
                >
                  <div class="container_box">
                    <h3>Edita el producto {{ producto.nombre }}</h3>
                    <input
                      type="text"
                      class="cantidad"
                      placeholder="Ingresa la cantidad"
                    />
                  </div>
                </div>
                <div v-else id="modal-container" class="modal_container_show">
                  <div class="container_box">
                    <i
                      @click="cerrar"
                      id="bttn-cerrar"
                      class="bi bi-x-circle-fill"
                    ></i>
                    <h3>Edita el producto {{ producto.nombre }}</h3>
                    <form @submit.prevent="ejecutar_transaccion">
                      <label for="tipo_operacion"
                        >Seleccione el tipo de operación</label
                      >
                      <select
                        class="controls"
                        v-model="tipo_transaccion"
                        placeholder="Seleccione el tipo de operación"
                      >
                        <option disabled value="">
                          Porfavor seleccione una opción
                        </option>
                        <option>Agregar</option>
                        <option>Retirar</option>
                      </select>
                      <p v-if="transaccion_message">
                        Por favor ingrese un tipo de operación
                      </p>
                      <input
                        v-model="cantidad"
                        class="controls"
                        type="number"
                        placeholder="Ingresa la cantidad"
                      />
                      <p v-if="cantidad_message">
                        Por favor ingrese una cantidad
                      </p>
                      <p v-if="message_limite">{{ message_limite_content }}</p>
                      <p v-if="message_cantidad_negativa">
                        Por favor ingrese una cantidad mayor a 0.
                      </p>
                      <button id="edit" type="submit">Editar</button>
                    </form>
                  </div>
                </div>
              </tr>
              <tr class="paginate">
                <td class="paginate-col" colspan="8">
                  <button @click="paginar">Previus</button>
                  <button
                    v-for="pagina in paginas"
                    :key="pagina"
                    @click="paginar"
                  >
                    {{ pagina }}
                  </button>
                  <button @click="paginar">Next</button>
                </td>
                <td>Page: {{ page }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="form-register">
          <h4>Ingreso de producto</h4>
          <form @submit.prevent="ingresar_producto">
            <input
              v-model="registro_producto.nombre"
              class="controls"
              type="text"
              name="nombre"
              id="nombre"
              placeholder="Ingrese el nombre del producto"
            />
            <p v-if="form_message.nombre_message">
              Ingrese el nombre el producto
            </p>
            <input
              v-model="registro_producto.tipo"
              class="controls"
              type="text"
              name="tipo"
              id="tipo"
              placeholder="Ingrese el tipo de producto"
            />
            <p v-if="form_message.tipo_message">Ingrese el tipo del producto</p>
            <input
              v-model="registro_producto.cantidad"
              class="controls"
              type="number"
              name="cantidad"
              id="cantidad"
              placeholder="Ingrese la cantidad del producto"
            />
            <p v-if="message_limite_form">{{ message_limite_content }}</p>
            <p v-if="form_message.cantidad_message">
              Ingrese la cantidad del producto
            </p>
            <p v-if="message_cantidad_negativa_form">
              Por favor ingrese una cantidad mayor a 0
            </p>
            <input
              v-model="registro_producto.descripcion"
              class="controls"
              type="textarea"
              name="descripcion"
              id="descripcion"
              placeholder="Descripción del producto"
            />
            <p v-if="form_message.descripcion_message">
              Ingrese alguna descripción
            </p>
            <input class="botons" type="submit" value="Ingresar" />
          </form>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  name: "AlmacenDetails",
  data() {
    return {
      productos: {},
      almacen_id: "",
      user_id: "",
      almacen: {},
      registro_producto: {
        nombre: undefined,
        tipo: undefined,
        cantidad: undefined,
        descripcion: undefined,
      },
      form_message: {
        nombre_message: false,
        tipo_message: false,
        cantidad_message: false,
        descripcion_message: false,
      },
      editar: false,
      tipo_transaccion: undefined,
      transaccion_message: false,
      cantidad: undefined,
      cantidad_message: false,
      producto_editar_id: undefined,
      producto_eliminar_id: undefined,
      message_limite: false,
      message_limite_content: "",
      message_limite_form: false,
      page: 1,
      paginas: [1, 2, 3, 4, 5],
      message_cantidad_negativa: false,
      message_cantidad_negativa_form: false,
    };
  },
  async created() {
    this.almacen_id = this.$route.params.almacen_id;
    this.user_id = this.$route.params.user_id;
    const path =
      "http://127.0.0.1:5000/almacenes/" +
      this.almacen_id +
      "/productos?page=" +
      String(this.page);
    let response = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": localStorage.token,
      },
    });
    let data = await response.json();
    if (data["message"] === "Unauthorized") {
      this.$router.push({ name: "Login" });
    } else if (data["message"] === "Token expired") {
      localStorage.token = "";
      this.$router.push({ name: "Login" });
    }
    this.productos = data["productos"];
    console.log("data: ", data);
  },
  async beforeMount() {
    const path =
      "http://127.0.0.1:5000/users/" +
      this.$route.params.user_id +
      "/almacenes";
    let response = await fetch(path, {
      method: "POST",
      body: JSON.stringify({
        search: this.$route.params.almacen_id,
      }),
      headers: {
        "Content-Type": "application/json",
        "x-access-token": localStorage.token,
      },
    });
    let data = await response.json();
    if (data["message"] === "Unauthorized") {
      this.$router.push({ name: "Login" });
    } else if (data["message"] === "Token expired") {
      localStorage.token = "";
      this.$router.push({ name: "Login" });
    }
    this.almacen = data["almacen"];
    console.log("data: ", data);
  },
  methods: {
    async logout() {
      const url = "http://127.0.0.1:5000/logout";
      let response = await fetch(url);
      let data = await response.json();
      if (data["success"]) {
        localStorage.token = "";
        this.$router.push({ name: "home" });
      }
    },
    async ingresar_producto() {
      if (this.registro_producto.cantidad < 1) {
        this.message_cantidad_negativa_form = true;
      } else {
        this.message_cantidad_negativa_form = false;
        const url =
          "http://127.0.0.1:5000/almacenes/" +
          this.almacen_id +
          "/productos" +
          "?page=" +
          String(this.page);
        let response = await fetch(url, {
          method: "POST",
          body: JSON.stringify({
            nombre: this.registro_producto["nombre"],
            tipo: this.registro_producto["tipo"],
            cantidad: this.registro_producto["cantidad"],
            descripcion: this.registro_producto["descripcion"],
          }),
          headers: {
            "Content-Type": "application/json",
            "x-access-token": localStorage.token,
          },
        });
        let data = await response.json();
        console.log("created:", data);
        if (data["message"] === "Unprocesable") {
          let claves = Object.keys(this.registro_producto);
          for (const clave of claves) {
            if (this.registro_producto[clave] === undefined) {
              let dato = clave + "_message";
              this.form_message[dato] = true;
            } else {
              let dato = clave + "_message";
              this.form_message[dato] = false;
            }
          }
        } else if (data.message === "Not accepted") {
          this.message_limite_form = true;
          this.message_limite_content =
            "La cantidad del producto excede la capacidad del almacen";
          let claves = Object.keys(this.registro_producto);
          for (const clave of claves) {
            let dato = clave + "_message";
            this.form_message[dato] = false;
          }
        } else {
          this.productos = data["productos"];
          this.message_limite_form = false;
          this.message_limite_content = "";
          this.registro_producto["nombre"] = undefined;
          this.registro_producto["tipo"] = undefined;
          this.registro_producto["cantidad"] = undefined;
          this.registro_producto["descripcion"] = undefined;
        }
      }
    },
    async ejecutar_transaccion() {
      if (this.cantidad < 1) {
        this.message_cantidad_negativa = true;
      } else {
        this.message_cantidad_negativa = false;
        const url_patch =
          "http://127.0.0.1:5000/almacenes/" +
          this.almacen_id +
          "/productos/" +
          this.producto_editar_id +
          "?page=" +
          String(this.page);
        const url_post =
          "http://127.0.0.1:5000/productos/" +
          this.producto_editar_id +
          "/transacciones";
        let response_patch = await fetch(url_patch, {
          method: "PATCH",
          body: JSON.stringify({
            cantidad: this.cantidad,
            tipo_transaccion: this.tipo_transaccion,
          }),
          headers: {
            "Content-Type": "application/json",
            "x-access-token": localStorage.token,
          },
        });
        let data_patch = await response_patch.json();
        console.log("data_patch: ", data_patch);
        if (data_patch["success"]) {
          let response_post = await fetch(url_post, {
            method: "POST",
            body: JSON.stringify({
              tipoDocumento: this.tipo_transaccion,
              idProducto: this.producto_editar_id,
              cantidad: this.cantidad,
            }),
            headers: {
              "Content-Type": "application/json",
              "x-access-token": localStorage.token,
            },
          });
          let data_post = await response_post.json();
          console.log("data_post: ", data_post);
          this.productos = data_patch["productos"];
          this.message_limite = false;
          this.message_limite_content = "";
          this.editar = false;
          this.cantidad = undefined;
          this.tipo_transaccion = undefined;
        } else if (data_patch.message == "Not accepted") {
          this.message_limite = true;
          if (this.tipo_transaccion === "Agregar") {
            this.message_limite_content =
              "No puede ingresar dicha cantidad ya que excede la capacidad del almacen";
          } else {
            this.message_limite_content =
              "No puede retirar más cantidad de la que tiene disponible";
          }
          this.transaccion_message = false;
          this.cantidad_message = false;
        } else {
          if (
            this.tipo_transaccion == "" ||
            this.tipo_transaccion == undefined
          ) {
            this.transaccion_message = true;
          } else {
            this.transaccion_message = false;
          }
          if (this.cantidad == "" || this.cantidad == undefined) {
            this.cantidad_message = true;
          } else {
            this.cantidad_message = false;
          }
        }
      }
    },
    async eliminar() {
      this.producto_eliminar_id =
        event.target.parentElement.parentElement.parentElement.__vnode.key;
      const url =
        "http://127.0.0.1:5000/almacenes/" +
        this.almacen_id +
        "/productos/" +
        this.producto_eliminar_id +
        "?page=" +
        String(this.page);
      let response = await fetch(url, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.token,
        },
      });
      let data = await response.json();
      if (data["success"] === true) {
        this.productos = data["productos"];
      }
    },
    abrir_editar() {
      this.producto_editar_id =
        event.target.parentElement.parentElement.parentElement.__vnode.key;
      this.editar = true;
    },
    cerrar() {
      this.editar = false;
      this.tipo_transaccion = undefined;
      this.cantidad = undefined;
    },
    async cambiar_venta() {
      this.producto_editar_id = event.path["1"].__vnode.key;
      const url_patch =
        "http://127.0.0.1:5000/almacenes/" +
        this.almacen_id +
        "/productos/" +
        this.producto_editar_id +
        "?page=" +
        String(this.page);
      let response_patch = await fetch(url_patch, {
        method: "PATCH",
        body: JSON.stringify({
          venta: "cambiar_venta",
        }),
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.token,
        },
      });
      let data_patch = await response_patch.json();
      if (data_patch.success == true) {
        this.productos = data_patch["productos"];
      }
    },
    async paginar() {
      let page = event.target.innerHTML;
      if (page === "Next") {
        page = this.page + 1;
      } else if (page === "Previus") {
        page = this.page - 1;
      } else {
        page = parseInt(page);
      }
      this.almacen_id = this.$route.params.almacen_id;
      this.user_id = this.$route.params.user_id;
      const path =
        "http://127.0.0.1:5000/almacenes/" +
        this.almacen_id +
        "/productos?page=" +
        String(page);
      let response = await fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.token,
        },
      });
      let data = await response.json();
      if (data["message"] != "resource not found") {
        this.productos = data["productos"];
        this.page = page;
        if (this.page > this.paginas[4]) {
          this.paginas[0] += 5;
          this.paginas[1] += 5;
          this.paginas[2] += 5;
          this.paginas[3] += 5;
          this.paginas[4] += 5;
        } else if (this.page < this.paginas[0]) {
          this.paginas[0] -= 5;
          this.paginas[1] -= 5;
          this.paginas[2] -= 5;
          this.paginas[3] -= 5;
          this.paginas[4] -= 5;
        }
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Poppins&display=swap");

ul {
  padding: 0px;
  text-align: left;
}

.links {
  padding-bottom: 30px;
  padding-top: 20px;
  list-style: none;
  text-align: left;
}
ul a {
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  color: purple;
  text-decoration: underline;
}

.container_links {
  position: fixed;
  padding-top: 90px;
  padding-left: 20px;
  width: 200px;
  height: 100%;
  text-align: left;
}

.container_page {
  padding-left: 110px;
}

form p {
  color: red;
  margin-block-end: 0px;
}

label {
  text-align: left;
  font-weight: bold;
  color: black;
}

.opciones {
  text-align: center;
  width: 100px;
}

select {
  margin-top: 1px;
}

#bttn-cerrar {
  display: flex;
  flex-direction: row-reverse;
  text-align: right;
  transition: 0.3s ease all;
  padding: 0px;
}

#bttn-cerrar:hover {
  color: black;
}

button #edit {
  margin-top: 30px;
}

i {
  padding-left: 20px;
  padding-right: 20px;
}

.venta_t {
  cursor: pointer;
}

td #venta_t {
  color: lightgreen;
  padding-left: 10px;
  padding-right: 10px;
}

td #venta_f {
  color: red;
  padding-left: 10px;
  padding-right: 10px;
}

button {
  border-radius: 4px;
  background-color: #238155;
}
tfoot,
nav {
  margin: 0px;
  padding: 0px;
}
body {
  font-family: "Open Sans", sans-serif;
  font-weight: 300;
  line-height: 1.42em;
  color: #a7a1ae;
  background-color: #1f2739;
  height: 1500px;
  background-size: 100% 100%;
}

h1 {
  font-size: 3em;
  font-weight: 300;
  line-height: 1em;
  text-align: center;
  color: #4dc3fa;
  margin: 0 9px 9px 9px;
  padding: 30px;
  padding-top: 90px;
}

h2 {
  font-size: 1em;
  font-weight: 300;
  text-align: center;
  display: block;
  line-height: 1em;
  padding-bottom: 2em;
  color: #fb667a;
}

h2 a {
  font-weight: 700;
  text-transform: uppercase;
  color: #fb667a;
  text-decoration: none;
}

.blue {
  color: #185875;
}
.yellow {
  color: #fff842;
}

.container-table th h1 {
  font-weight: bold;
  font-size: 1em;
  text-align: left;
  color: #185875;
}

.container table {
  border-radius: 4px;
  box-shadow: 7px 13px 37px #000;
}

.container-table td {
  font-weight: normal;
  font-size: 1em;
  -webkit-box-shadow: 0 2px 2px -2px #0e1119;
  -moz-box-shadow: 0 2px 2px -2px #0e1119;
  box-shadow: 0 2px 2px -2px #0e1119;
}

.container-table {
  text-align: left;
  overflow: hidden;
  width: 93%;
  margin: 0 auto;
  display: table;
  padding: 0 0 3em 0;
}

.container-table td,
.container-table th {
  padding-bottom: 2%;
  padding-top: 2%;
  padding-left: 2%;
}

/* Background-color of the odd rows */
.container-table tr:nth-child(odd) {
  background-color: #323c50;
}

/* Background-color of the even rows */
.container-table tr:nth-child(even) {
  background-color: #2c3446;
}

.container-table th {
  background-color: #1f2739;
}

.container-table td:first-child {
  color: #fb667a;
}

.container-table tr:hover {
  background-color: #464a52;
  -webkit-box-shadow: 0 6px 6px -6px #0e1119;
  -moz-box-shadow: 0 6px 6px -6px #0e1119;
  box-shadow: 0 6px 6px -6px #0e1119;
}

.container-table td:hover {
  background-color: #fff842;
  color: #403e10;
  font-weight: bold;

  box-shadow: #7f7c21 -1px 1px, #7f7c21 -2px 2px, #7f7c21 -3px 3px,
    #7f7c21 -4px 4px, #7f7c21 -5px 5px, #7f7c21 -6px 6px;
  transform: translate3d(6px, -6px, 0);

  transition-delay: 0s;
  transition-duration: 0.4s;
  transition-property: all;
  transition-timing-function: line;
}

@media (max-width: 900px) {
  .container-table td:nth-child(4),
  .container-table th:nth-child(4) {
    display: none;
  }
}
.descripcion {
  max-width: 200px;
}

.producto_id {
  min-width: 40px;
  text-align: left;
}
.form-register {
  width: 400px;
  background: #24303c;
  padding: 50px;
  margin: auto;
  margin-top: 100px;
  /*margin-bottom: 100px;*/
  border-radius: 4px;
  font-family: "calibri";
  color: white;
  box-shadow: 7px 13px 37px #000;
}

.form-register h4 {
  font-size: 22px;
  margin-bottom: 20px;
}

.controls {
  width: 100%;
  background: #24303c;
  padding: 10px;
  border-radius: 4px;
  margin-top: 16px;
  border: 1px solid #1f53c5;
  font-family: "calibri";
  font-size: 18px;
  color: white;
}

.form-register p {
  height: 40px;
  text-align: center;
  font-size: 18px;
  line-height: 25px;
}

.form-register a {
  color: white;
  text-decoration: none;
}

.form-register a:hover {
  color: white;
  text-decoration: underline;
}

.form-register .botons {
  width: 100%;
  background: #1f53c5;
  border: none;
  padding: 12px;
  color: white;
  margin: 16px 0;
  font-size: 16px;
}

.modal_container {
  display: flex;
  flex-direction: row;
  background-color: rgba(0, 0, 0, 0.3);
  align-items: center;
  justify-content: center;
  position: fixed;
  pointer-events: none;
  opacity: 0;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  transition: opacity 0.3s ease;
}

.modal_container_show {
  display: flex;
  flex-direction: row;
  background-color: rgba(0, 0, 0, 0.2);
  align-items: center;
  justify-content: center;
  position: fixed;
  pointer-events: auto;
  opacity: 1;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  transition: opacity 0.3s ease;
}
.container_box {
  background-color: #fff;
  width: 600px;
  max-width: 100%;
  padding: 30px 50px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.container_box h3 {
  margin: 30px;
}

.container_box p {
  font-size: 14px;
}
</style>
