<template>
  <body>
    <div class="pagina">
      <div class="container-fluid px-1 py-5 mx-auto">
        <div class="row d-flex justify-content-center">
          <div class="col-xl-7 col-lg-8 col-md-9 col-11 text-center">
            <h1>Regístrate Aquí!</h1>
            <div class="card">
              <h5 class="text-center mb-4">
                Gestiona App, el mejor gestor de almacenes
              </h5>
              <form class="form-card" @submit.prevent="register">
                <div class="row justify-content-between text-left">
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Nombre<span class="text-danger"> *</span></label
                    >
                    <input
                      type="text"
                      id="fname"
                      name="fname"
                      placeholder="Ingresa tu nombre"
                      v-model="registro_values.nombre"
                    />
                    <p v-if="registro_message.nombre_message">
                      Falta rellenar este campo
                    </p>
                  </div>
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Apellido<span class="text-danger"> *</span></label
                    >
                    <input
                      type="text"
                      id="lname"
                      name="lname"
                      placeholder="Ingresa tu apellido"
                      v-model="registro_values.apellido"
                    />
                    <p v-if="registro_message.apellido_message">
                      Falta rellenar este campo
                    </p>
                  </div>
                </div>
                <div class="row justify-content-between text-left">
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Usuario<span class="text-danger"> *</span></label
                    >
                    <input
                      type="text"
                      id="usuario"
                      name="usuario"
                      placeholder="Ingresa tu suario"
                      v-model="registro_values.username"
                    />
                    <p v-if="registro_message.username_message">
                      Falta rellenar este campo
                    </p>
                    <p v-if="usuario_existente_message">
                      Este usuario ya existe
                    </p>
                  </div>
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Edad<span class="text-danger"> *</span></label
                    >
                    <input
                      type="number"
                      id="edad"
                      name="edad"
                      placeholder=""
                      v-model="registro_values.edad"
                    />
                    <p v-if="registro_message.edad_message">
                      Falta rellenar este campo
                    </p>
                  </div>
                </div>
                <div class="row justify-content-between text-left">
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Contraseña<span class="text-danger"> *</span></label
                    >
                    <input
                      type="password"
                      id="contraseña"
                      name="contraseña"
                      placeholder="Ingresa tu contraseña"
                      v-model="registro_values.password"
                    />
                    <p v-if="registro_message.password_message">
                      Falta rellenar este campo
                    </p>
                  </div>
                  <div class="form-group col-sm-6 flex-column d-flex">
                    <label class="form-control-label px-3"
                      >Confirma tu contraseña<span class="text-danger">
                        *</span
                      ></label
                    >
                    <input
                      type="password"
                      id="contraseña_confirmacion"
                      name="contraseña_confirmacion"
                      placeholder="Confirma tu contraseña"
                      v-model="registro_values.confirmacion_password"
                      @input.prevent="verificacion_contraseña;"
                    />
                    <p v-if="registro_message.confirmacion_password_message">
                      Falta rellenar este campo
                    </p>
                    <p v-if="password_no_correcto">
                      Las contraseñas no coinciden
                    </p>
                  </div>
                </div>
                <div class="row justify-content-between text-left">
                  <div class="form-group col-12 flex-row d-flex">
                    <label class="form-control-label px-3"
                      >Sexo<span class="text-danger"> *</span></label
                    >
                    <input
                      class="checkbox"
                      type="radio"
                      id="masculino"
                      value="masculino"
                      v-model="registro_values.sexo"
                    />
                    <label for="masculino">Masculino</label>
                    <input
                      class="checkbox"
                      type="radio"
                      id="femenino"
                      value="femenino"
                      v-model="registro_values.sexo"
                    />
                    <label for="femenino">Femenino</label>
                  </div>
                  <p v-if="registro_message.sexo_message">
                    Tiene que marcar algo
                  </p>
                </div>
                <div class="row justify-content-end">
                  <button type="submit" class="btn-block btn-primary">
                    Regístrate
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  name: "Registro",
  data() {
    return {
      registro_values: {
        nombre: undefined,
        apellido: undefined,
        edad: undefined,
        sexo: undefined,
        username: undefined,
        password: undefined,
        confirmacion_password: undefined,
      },
      registro_message: {
        nombre_message: false,
        apellido_message: false,
        edad_message: false,
        sexo_message: false,
        username_message: false,
        password_message: false,
        confirmacion_password_message: false,
      },
      image: "@/assets/fondo-registro.jpg",
      password_no_correcto: false,
      usuario_existente_message: false,
    };
  },
  methods: {
    async register() {
      if (
        this.registro_values["password"] ===
        this.registro_values["confirmacion_password"]
      ) {
        this.password_no_correcto = false;
      } else {
        this.password_no_correcto = true;
      }
      const url = "http://127.0.0.1:5000/users";
      if (!this.password_no_correcto) {
        let response = await fetch(url, {
          method: "POST",
          body: JSON.stringify({
            nombre: this.registro_values["nombre"],
            apellido: this.registro_values["apellido"],
            edad: this.registro_values["edad"],
            sexo: this.registro_values["sexo"],
            usuario: this.registro_values["username"],
            contraseña: this.registro_values["password"],
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        let data = await response.json();
        console.log("data: ", data);
        if (data["message"] === "Unprocesable") {
          let claves = Object.keys(this.registro_values);
          for (const clave of claves) {
            if (
              this.registro_values[clave] === undefined ||
              this.registro_values[clave] == ""
            ) {
              let dato = clave + "_message";
              this.registro_message[dato] = true;
            } else {
              let dato = clave + "_message";
              this.registro_message[dato] = false;
            }
          }
        } else if (data.message === "Not accepted") {
          this.usuario_existente_message = true;
          let claves = Object.keys(this.registro_message);
          for (const clave of claves) {
            this.registro_message[clave] = false;
          }
          this.registro_values.username = "";
        } else {
          const user_id = data["created"]["id"];
          localStorage.token = data.token;
          this.$router.push({
            name: "Almacen",
            params: { user_id: user_id },
          });
        }
      }
    },
  },
};
</script>

<style scoped>
p {
  color: red;
}

h1 {
  color: white;
  font-weight: bold;
  padding-top: 70px;
}

.form-group col-12 flex-row d-flex {
  display: flex;
  flex-direction: row;
  text-align: center;
}
.btn-block btn-primary {
  text-align: center;
  justify-content: center;
}
.checkbox {
  display: flex;
  flex-direction: row;
  margin-right: 10px;
  margin-left: 70px;
}

.form-container {
  display: flex;
}

.form-registro {
  display: flex;
}
body {
  color: #000;
  background-image: url("@/assets/fondo-registro.jpg");
  overflow-x: hidden;
  height: 1000px;
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.card {
  padding: 30px 40px;
  margin-top: 60px;
  margin-bottom: 60px;
  border: none !important;
  box-shadow: 0 6px 12px 0 rgba(0, 0, 0, 0.2);
}
.blue-text {
  color: #00bcd4;
}
.form-control-label {
  margin-bottom: 0;
}
input,
textarea,
button {
  padding: 8px 15px;
  border-radius: 5px !important;
  margin: 5px 0px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  font-size: 18px !important;
  font-weight: 300;
}
input:focus,
textarea:focus {
  -moz-box-shadow: none !important;
  -webkit-box-shadow: none !important;
  box-shadow: none !important;
  border: 1px solid #00bcd4;
  outline-width: 0;
  font-weight: 400;
}
.btn-block {
  text-transform: uppercase;
  font-size: 15px !important;
  font-weight: 400;
  height: 43px;
  cursor: pointer;
}
.btn-block:hover {
  color: #fff !important;
}
button:focus {
  -moz-box-shadow: none !important;
  -webkit-box-shadow: none !important;
  box-shadow: none !important;
  outline-width: 0;
}
</style>
