<template>
  <body>
    <div v-if="!datos">
      <h1>
        Lo sentimos por el momento no hay ningún producto disponible a la venta
      </h1>
    </div>
    <div class="container" v-else>
      <div class="container_links">
        <h4>Links</h4>
        <ul>
          <li>
            <router-link :to="{ name: 'home' }">Home</router-link>
          </li>
          <li><a href="#" @click="logout">Logout</a></li>
          <li>
            <router-link :to="{ name: 'Almacen', params: { user_id: user_id } }"
              >Almacenes</router-link
            >
          </li>
        </ul>
      </div>
      <div class="container_productos">
        <h1>Bienvenido a la zona de compras</h1>
        <h3>Productos:</h3>
        <div
          class="container_card"
          v-for="producto in productos.productos"
          :key="producto.id"
        >
          <div class="container_tittle">
            <h1>{{ producto.nombre }}</h1>
            <button class="adquirir" @click="abrir_comprar">Adquirir</button>
          </div>
          <div class="container_info">
            <p>Stock: {{ producto.cantidad }}</p>
            <p>Tipo: {{ producto.tipo }}</p>
            <p>Descipción: {{ producto.descripcion }}</p>
          </div>
        </div>
        <div class="paginate">
          <button @click="paginar" class="bttn-paginar">Previus</button>
          <button
            class="bttn-paginar"
            v-for="pagina in paginas"
            :key="pagina"
            @click="paginar"
          >
            {{ pagina }}
          </button>
          <button @click="paginar" class="bttn-paginar">Next</button>
        </div>
      </div>
      <div v-if="!comprar" class="container_modal">
        <div class="container_box">
          <h3>Edita el producto {{ producto_comprar_nombre }}</h3>
        </div>
      </div>
      <div v-else class="container_modal_show">
        <div class="container_box">
          <i @click="cerrar" id="bttn-cerrar" class="bi bi-x-circle-fill"></i>
          <h3>Estás por adquirir el {{ producto_comprar_nombre }}</h3>
          <form @submit.prevent="generar_adquisicion">
            <label for="almacen"
              >A que almacen quiere agregar su producto</label
            >
            <p v-if="almacen_id_message" class="error_message">
              Por favor seleccione un almacen
            </p>
            <select
              v-model="almacen_user_id"
              name="almacen"
              placeholder="Seleccione un almacen"
            >
              <option disabled value="">Porfavor seleccione una opción</option>
              <option
                v-for="almacen in almacenes"
                :key="almacen.id"
                v-bind:value="almacen.id"
              >
                {{ almacen.nombre }}
              </option>
            </select>
            <label for="cantidad"
              >Ingrese la cantidad a adquirir (Stock máximo
              {{ stock_producto_comprar }} unidades)</label
            >
            <input
              type="number"
              name="cantidad"
              v-model="registro_compra.cantidad_adquirir"
            />
            <p v-if="cantidad_adquirir_message" class="error_message">
              Por favor ingrese una cantidad
            </p>
            <p class="error_message" v-if="message_limite">
              No puede comprar más productos de los que hay en stock
            </p>
            <p class="error_message" v-if="message_cantidad_negativa">
              Por favor ingrese un valor positivo
            </p>
            <h4>¿Estás seguro que quieres adiquirir este producto ?</h4>
            <button id="edit" type="submit">Aceptar</button>
          </form>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  name: "Compras",
  data() {
    return {
      page: 1,
      paginas: [1, 2, 3, 4, 5, 6],
      datos: true,
      user_id: 0,
      productos: {},
      almacenes: {},
      comprar: false,
      producto_comprar_id: undefined,
      producto_comprar_nombre: undefined,
      stock_producto_comprar: undefined,
      registro_compra: {
        cantidad_adquirir: undefined,
        almacen_id: undefined,
      },
      almacen_user_id: undefined,
      cantidad_adquirir_message: false,
      almacen_id_message: false,
      message_limite: false,
      message_cantidad_negativa: false,
    };
  },
  async beforeMount() {
    const url_productos =
      "http://127.0.0.1:5000/productos?page=" + String(this.page);
    let response_productos = await fetch(url_productos, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": localStorage.token,
      },
    });
    let data_productos = await response_productos.json();
    if (data_productos.message === "Unauthorized") {
      this.$router.push({ name: "Login" });
    } else if (data_productos["message"] === "Token expired") {
      localStorage.token = "";
      this.$router.push({ name: "Login" });
    } else {
      this.productos = data_productos;
      this.user_id = data_productos.user_id;
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
    abrir_comprar() {
      console.log(this.almacenes[0]);
      this.producto_comprar_nombre =
        event.target.parentElement.__vnode.children["0"].children;
      this.producto_comprar_id = event.path["2"].__vnode.key;
      for (let producto of this.productos.productos) {
        if (producto.id == this.producto_comprar_id) {
          this.stock_producto_comprar = producto.cantidad;
          this.registro_compra.almacen_id = producto.almacen_id;
        }
      }
      this.comprar = true;
    },
    cerrar() {
      this.comprar = false;
    },
    async generar_adquisicion() {
      console.log(this.almacen_user_id);
      if (
        this.registro_compra.cantidad_adquirir > this.stock_producto_comprar
      ) {
        this.message_limite = true;
        this.cantidad_adquirir_message = false;
        this.message_cantidad_negativa = false;
      } else {
        this.message_limite = false;
        if (this.registro_compra.cantidad_adquirir < 1) {
          this.message_cantidad_negativa = true;
          this.cantidad_adquirir_message = false;
        } else {
          this.message_cantidad_negativa = false;
          const url_patch =
            "http://127.0.0.1:5000/almacenes/" +
            this.registro_compra.almacen_id +
            "/productos/" +
            this.producto_comprar_id +
            "?page=" +
            String(this.page);
          const url_post =
            "http://127.0.0.1:5000/productos/" +
            this.producto_comprar_id +
            "/transacciones";
          let response_patch = await fetch(url_patch, {
            method: "PATCH",
            body: JSON.stringify({
              cantidad: this.registro_compra.cantidad_adquirir,
              tipo_transaccion: "Retirar",
            }),
            headers: {
              "Content-Type": "application/json",
              "x-access-token": localStorage.token,
            },
          });
          let data_patch = await response_patch.json();
          console.log("data_patch: ", data_patch);
          if (data_patch.message === "Unprocesable") {
            if (this.almacen_user_id == undefined) {
              this.almacen_id_message = true;
            } else {
              this.almacen_id_message = false;
            }
            if (this.registro_compra.cantidad_adquirir == undefined) {
              this.cantidad_adquirir_message = true;
            } else {
              this.cantidad_adquirir_message = false;
            }
          } else {
            let response_post = await fetch(url_post, {
              method: "POST",
              body: JSON.stringify({
                tipoDocumento: "Retirar",
                idProducto: this.producto_comprar_id,
                cantidad: this.registro_compra.cantidad_adquirir,
              }),
              headers: {
                "Content-Type": "application/json",
                "x-access-token": localStorage.token,
              },
            });
            let data_post = await response_post.json();
            console.log("data_post: ", data_post);
            this.productos = data_patch;

            const url =
              "http://127.0.0.1:5000/almacenes/" +
              this.almacen_user_id +
              "/productos" +
              "?page=" +
              String(this.page);
            let response = await fetch(url, {
              method: "POST",
              body: JSON.stringify({
                nombre: data_patch.producto.nombre,
                tipo: data_patch.producto.tipo,
                cantidad: this.registro_compra.cantidad_adquirir,
                descripcion: data_patch.producto.descripcion,
              }),
              headers: {
                "Content-Type": "application/json",
                "x-access-token": localStorage.token,
              },
            });
            let data = await response.json();
            console.log("created:", data);
            if (data_patch.producto.cantidad == 0) {
              const url =
                "http://127.0.0.1:5000/almacenes/" +
                this.registro_compra.almacen_id +
                "/productos/" +
                this.producto_comprar_id +
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
              console.log("data: ", data);
            }
            this.comprar = false;
            this.registro_compra.cantidad_adquirir = undefined;
            this.almacen_user_id = undefined;

            const url_productos =
              "http://127.0.0.1:5000/productos?page=" + String(this.page);
            let response_productos = await fetch(url_productos, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                "x-access-token": localStorage.token,
              },
            });
            let data_productos = await response_productos.json();
            this.productos = data_productos;
          }
        }
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
      const path = "http://127.0.0.1:5000/productos?page=" + String(page);
      let response = await fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.token,
        },
      });
      let data = await response.json();
      if (data.message != "resource not found") {
        this.productos = data;
        this.page = page;
        if (this.page > this.paginas[5]) {
          this.paginas[0] += 6;
          this.paginas[1] += 6;
          this.paginas[2] += 6;
          this.paginas[3] += 6;
          this.paginas[4] += 6;
          this.paginas[5] += 6;
        } else if (this.page < this.paginas[0]) {
          this.paginas[0] -= 6;
          this.paginas[1] -= 6;
          this.paginas[2] -= 6;
          this.paginas[3] -= 6;
          this.paginas[4] -= 6;
          this.paginas[5] -= 6;
        }
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Open Sans", sans-serif;
  font-weight: bold;
  background-color: #1f2739;
  height: auto;
  background-size: 100% 100%;
}

.paginate {
  padding-bottom: 30px;
}

.bttn-paginar {
  margin-left: 5px;
  margin-right: 5px;
  padding-left: 10px;
  padding-right: 10px;
}

ul {
  padding: 0px;
  text-align: left;
}

ul li {
  padding-bottom: 10px;
  padding-top: 10px;
}
ul a {
  text-decoration: none;
}

.error_message {
  color: red;
  font-weight: 100;
  font-size: 15px;
}

h1 {
  font-size: 3em;
  font-weight: bold;
  line-height: 1em;
  text-align: left;
  color: #4dc3fa;
  margin: 20px 0px 25px 0px;
}

.container {
  display: flex;
  justify-content: flex-start;
  padding: 0px;
  margin: 0px;
  margin-right: 0px;
}

select {
  margin-bottom: 10px;
  padding-bottom: 7px;
}

h3,
h4 {
  text-align: left;
  font-weight: 200;
  color: white;
}

.container_links {
  position: fixed;
  padding-top: 70px;
  padding-left: 20px;
  width: 200px;
  height: 100%;
}

.container_productos {
  width: 100%;
  padding-left: 40px;
  padding-top: 60px;
  margin-left: 250px;
}

.container_tittle {
  background-color: #86868d;
  min-width: 270px;
  max-width: 270px;
  border-bottom-left-radius: 8px;
  border-top-left-radius: 8px;
  text-align: left;
}
.container_card {
  display: flex;
  max-width: 700px;
  justify-content: flex-start;
  background-color: white;
  margin: 60px;
  border-radius: 8px;
  box-shadow: 5px 11px 30px rgba(0, 0, 0, 0.4);
  transition: all 400ms ease;
}

.container_card:hover {
  box-shadow: 7px 30px 50px rgba(0, 0, 0, 1);
  transform: translateY(-6%);
}

.container_card div {
  padding: 10px;
  text-align: left;
}

.container_productos .container_info {
  color: #6a6a6a;
  font-weight: 200;
  padding-left: 40px;
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

i {
  padding-left: 30px;
  padding-right: 30px;
}

button {
  border-radius: 4px;
  background-color: #238155;
}

.adquirir {
  background-color: #86868d;
  transition: 0.3s ease all;
}
.adquirir:hover {
  background-color: #238155;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 1);
}

.container_modal {
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

.container_modal_show {
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
  color: black;
  margin: 30px;
  text-align: center;
}

.container_box h4 {
  color: black;
  font-size: 14px;
  text-align: center;
}

.container_box input {
  padding-bottom: 8px;
  margin-bottom: 10px;
}
</style>
