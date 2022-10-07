import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home",
    component: () =>
      import(/* webpackChunkName: "Home" */ "../views/HomeView.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Login.vue"),
  },
  {
    path: "/register",
    name: "Registro",
    component: () =>
      import(/* webpackChunkName: "Registro" */ "../views/Register.vue"),
  },
  {
    path: "/user/:user_id/almacen",
    name: "Almacen",
    props: true,
    component: () =>
      import(/* webpackChunkName: "Almacen" */ "../views/Almacenes.vue"),
  },
  {
    path: "/user/:user_id/almacen/:almacen_id",
    name: "AlmacenDetails",
    props: true,
    component: () =>
      import(
        /* webpackChunkName: "AlmacenDetails" */ "../views/AlmacenDetails.vue"
      ),
  },
  {
    path: "/compras",
    name: "Compras",
    props: true,
    component: () =>
      import(
        /* webpackChunkName: "ComprasProductos" */ "../views/ComprasProductos.vue"
      ),
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () =>
      import(/* webpackChunkName: "NotFound" */ "../components/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
