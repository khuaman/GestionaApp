<template>
  <div class="barra">
    <div class="navegacion">
      <div class="logo">
        <img
          class="logo-image"
          v-bind:src="require('./assets/GestionaApp.png')"
          alt="Logo"
        />
      </div>
      <div class="links">
        <nav>
          <router-link to="/">Home</router-link>
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Regístrate</router-link>
          <router-link to="/compras">Compras</router-link>
        </nav>
      </div>
    </div>
    <div class="barra"></div>
  </div>
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.barra {
  background-color: #1f2739;
  margin: 0px;
  margin-left: 0px;
  margin-right: 0px;
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 100%;
}

.navegacion {
  background-color: #53b287;
  display: flex;
  justify-content: space-between;
  border-end-end-radius: 8px;
  border-bottom-left-radius: 8px;
  box-shadow: 7px 13px 37px #000;
}

.links {
  text-align: right;
  max-block-size: 10px;
}
nav {
  padding: 17px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: cyan;
  padding-left: 10px;
  padding-right: 10px;
}

nav a.router-link-exact-active {
  color: #5b5be8;
}

.logo-image {
  height: 60px;
  width: auto;
  padding: 10px;
  opacity: 1;
}
</style>
