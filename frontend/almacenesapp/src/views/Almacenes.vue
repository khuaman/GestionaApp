<template>
  <body>
    <div class="logout">
      <form @submit.prevent="logout">
        <button type="submit">Logout</button>
      </form>
    </div>
    <h1>Bienvenido a tus almacenes {{ usuario_nombre }}</h1>
    <div class="container">
      <table class="table table-hover table-dark">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">NOMBRE</th>
            <th scope="col">DESCRIPCION</th>
            <th scope="col">CAPACIDAD</th>
            <th scope="col">FECHA_CREACION</th>
            <th scope="col">ACCESO</th>
            <th scope="col">ELIMINAR</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="almacen in almacenes" :key="almacen.id">
            <th scope="row">{{ almacen.id }}</th>
            <td>{{ almacen.nombre }}</td>
            <td>{{ almacen.descripcion }}</td>
            <td>{{ almacen.capacidad }}</td>
            <td>{{ almacen.date_created }}</td>
            <td @click="evento">
              <router-link
                :to="{
                  name: 'AlmacenDetails',
                  params: { user_id: user_id, almacen_id: almacen.id },
                }"
                :key="almacen.id"
              >
                edit
              </router-link>
            </td>
            <td id="opciones">
              <button @click="eliminar">
                <i class="bi bi-trash3-fill"></i>
              </button>
            </td>
          </tr>
          <tr class="paginate">
            <td class="paginate-col" colspan="6">
              <button @click="paginar">Previus</button>
              <button v-for="pagina in paginas" :key="pagina" @click="paginar">
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
      <h4>Ingreso de Almacen</h4>
      <form @submit.prevent="ingresar_almacen">
        <input
          v-model="registro_almacen.nombre"
          class="controls"
          type="text"
          name="nombre"
          id="nombre"
          placeholder="Ingrese el nombre del almacen"
        />
        <p v-if="almacen_existente">
          Este nombre ya ha sido tomado por otro almacen
        </p>
        <p v-if="form_message.nombre_message">Ingrese el nombre del almacen</p>
        <input
          v-model="registro_almacen.descripcion"
          class="controls"
          type="text"
          name="descripcion"
          id="descripcion"
          placeholder="Ingrese descripción del almacen"
        />
        <p v-if="form_message.descripcion_message">Ingrese descripcion</p>
        <input
          v-model="registro_almacen.capacidad"
          class="controls"
          type="number"
          name="capacidad"
          id="capacidad"
          placeholder="Ingrese la capacidad del almacen"
        />
        <p v-if="message_limite">{{ message_limite_content }}</p>
        <p v-if="form_message.capacidad_message">
          Ingrese la capacidad del almacen
        </p>
        <p v-if="message_capacidad_negativa">
          Por favor ingrese una tamaño mayor a 0
        </p>
        <input class="botons" type="submit" value="Ingresar" />
      </form>
    </div>
  </body>
</template>

<script>
//import Login from "@/views/Login.vue";
export default {
  name: "Almacenes",
  /*components: {
    Login,
  },*/
  data() {
    return {
      almacenes: {},
      user_id: "",
      usuario_nombre: "",
      registro_almacen: {
        nombre: undefined,
        descripcion: undefined,
        capacidad: undefined,
      },
      form_message: {
        nombre_message: false,
        descripcion_message: false,
        capacidad_message: false,
      },
      page: 1,
      paginas: [1, 2, 3, 4, 5],
      message_cantidad_negativa: false,
      almacen_eliminar_id: undefined,
      almacen_existente: false,
    };
  },
  async created() {
    this.user_id = this.$route.params.user_id;
    const url = "http://127.0.0.1:5000/users/" + this.user_id + "/almacenes";
    let response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": localStorage.token,
      },
    });
    let data = await response.json();
    console.log("data:", data);
    if (data["message"] === "Unauthorized") {
      this.$router.push({ name: "Login" });
    } else if (data["message"] === "Token expired") {
      localStorage.token = "";
      this.$router.push({ name: "Login" });
    }
    this.almacenes = data["almacenes"];
    this.usuario_nombre = data.nombre_usuario;
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
    async ingresar_almacen() {
      if (this.registro_almacen.capacidad < 1) {
        this.message_cantidad_negativa = true;
      } else {
        this.message_cantidad_negativa = false;
        const url =
          "http://127.0.0.1:5000/users/" +
          this.user_id +
          "/almacenes" +
          "?page=" +
          String(this.page);
        let response = await fetch(url, {
          method: "POST",
          body: JSON.stringify({
            nombre: this.registro_almacen["nombre"],
            descripcion: this.registro_almacen["descripcion"],
            capacidad: this.registro_almacen["capacidad"],
          }),
          headers: {
            "Content-Type": "application/json",
            "x-access-token": localStorage.token,
          },
        });
        let data = await response.json();
        console.log("created:", data);
        if (data["message"] === "Unprocesable") {
          let claves = Object.keys(this.registro_almacen);
          for (const clave of claves) {
            if (this.registro_almacen[clave] === undefined) {
              let dato = clave + "_message";
              this.form_message[dato] = true;
            } else {
              let dato = clave + "_message";
              this.form_message[dato] = false;
            }
          }
        } else if (data.message === "Not accepted") {
          this.almacen_existente = true;
        } else {
          this.almacenes = data["almacenes"];
          this.message_limite = false;
          this.message_limite_content = "";
          this.registro_almacen["nombre"] = undefined;
          this.registro_almacen["descripcion"] = undefined;
          this.registro_almacen["capacidad"] = undefined;
          let claves = Object.keys(this.registro_almacen);
          for (const clave of claves) {
            let dato = clave + "_message";
            this.form_message[dato] = false;
          }
          this.almacen_existente = false;
        }
      }
    },
    async eliminar() {
      //onsole.log(event);
      this.almacen_eliminar_id = event.path[3].__vnode.key;
      console.log(this.almacen_eliminar_id);
      const url =
        "http://127.0.0.1:5000/users/" +
        this.user_id +
        "/almacen/" +
        this.almacen_eliminar_id +
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
        this.almacenes = data["almacenes"];
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
      console.log("page: ", page);
      this.user_id = this.$route.params.user_id;
      const path =
        "http://127.0.0.1:5000/users/" +
        this.user_id +
        "/almacenes?page=" +
        String(page);
      let response = await fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.token,
        },
      });
      let data = await response.json();
      console.log("data: ", data);
      if (data["message"] != "resource not found") {
        this.almacenes = data["almacenes"];
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
    },
    evento() {
      console.log(event);
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Open Sans", sans-serif;
  font-weight: 300;
  line-height: 1.42em;
  color: #a7a1ae;
  background-color: #1f2739;
  height: 100%;
  background-size: 100% 100%;
}

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

.table table-hover table-dark {
  position: fixed;
  padding-top: 90px;
  padding-left: 90px;
  width: 200px;
  height: 100%;
  text-align: left;
}

.container_almacenes {
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

button #edit {
  margin-top: 30px;
}

i {
  padding-left: 20px;
  padding-right: 20px;
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

.paginate-col {
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

.logout {
  display: flex;
  flex-direction: row-reverse;
}
</style>
