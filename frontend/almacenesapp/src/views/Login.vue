<template>
  <body>
    <div class="container-login">
      <div>
        <div class="login-form-1">
          <h3>Login</h3>
          <form @submit.prevent="login">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                placeholder="Your Username *"
                v-model="username"
              />
            </div>
            <div class="form-group">
              <input
                type="password"
                class="form-control"
                placeholder="Your Password *"
                v-model="password"
              />
            </div>
            <div class="form-input">
              <input type="checkbox" id="remember_me" v-model="remember_me" />
              <label id="remember_me" for="remember_me">Remember me: </label>
            </div>
            <div class="registro-link">
              <router-link :to="{ name: 'Registro' }">
                No tienes cuenta? Regístrate aquí
              </router-link>
            </div>
            <div class="form-group">
              <input type="submit" class="btnSubmit" value="Login" />
            </div>
            <p v-if="redirect" class="error-msg">Los datos son inválidos</p>
          </form>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: undefined,
      password: undefined,
      user_id: undefined,
      remember_me: false,
      redirect: false,
    };
  },
  async beforeMount() {
    const url = "http://127.0.0.1:5000/user";
    let response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": localStorage.token,
      },
    });
    let data = await response.json();
    console.log("data:", data);
    if (data.success == true) {
      this.$router.push({
        name: "Almacen",
        params: { user_id: data.profile.id },
      });
    }
  },
  methods: {
    async login() {
      const url = "http://127.0.0.1:5000/login";
      let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({
          usuario: this.username,
          contraseña: this.password,
          remember_me: this.remember_me,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      let data = await response.json();
      console.log("data: ", data);
      this.redirect = !data["success"];
      if (data["success"]) {
        this.user_id = data["profile"]["id"];
        localStorage.token = data.token;
        this.$router.push({
          name: "Almacen",
          params: { user_id: this.user_id },
        });
      }
    },
  },
};
</script>

<style scoped>
body {
  background-image: url("@/assets/FONDOLOGIN.jpg");
  height: 1000px;
}

.error-msg {
  color: red;
}

.registro-link {
  color: lightblue;
}
.registro-link:hover {
  text-decoration: underline;
  text-decoration-color: red;
}

.container-login {
  margin-top: 0px;
  padding-top: 80px;
  margin-bottom: 5%;
  padding-right: 600px;
  padding-left: 600px;
  border-right: 5px;
}
.login-form-1 {
  padding: 9%;
  background: #282726;
  box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.2), 0 9px 26px 0 rgba(0, 0, 0, 0.19);
  border-radius: 5px;
  margin: 3rem auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.login-form-1 h3 {
  text-align: center;
  margin-bottom: 12%;
  color: #fff;
}

.btnSubmit {
  font-weight: 600;
  width: 50%;
  color: #282726;
  background-color: #fff;
  border: none;
  border-radius: 1.5rem;
  padding: 2%;
}
.form-input {
  margin: 0.5rem auto;
  text-align: left;
}
.form-group {
  margin: 0.5rem auto;
}
#remember_me {
  color: white;
  padding: 8px;
}
</style>
