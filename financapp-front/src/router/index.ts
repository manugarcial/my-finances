import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SingleStockView from "../views/SingleStockView.vue";
import UserLogin from "../components/UserLogin.vue";
// import { getCurrentUser } from "../api/api";
import store from "../store";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    component: UserLogin,
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/net-salary",
    name: "net-salary",
    component: () => import("../views/NetSalaryView.vue"),
  },
  {
    path: "/mortgage",
    name: "mortgage",
    component: () => import("../views/MortgageView.vue"),
  },
  {
    path: "/stocks",
    name: "stocks",
    component: () => import("../views/StocksView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/stocks-search",
    name: "stocks-search",
    component: () => import("../views/StockSearchView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/global-economy-data",
    name: "global-economy-data",
    component: () => import("../views/GlobalEconomyDataView.vue"),
  },
  {
    path: "/item/:ticker",
    component: SingleStockView,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/:catchAll(.*)",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const user = store.state.user; // This should retrieve the user from the store

  if (requiresAuth && !user) {
    next("/login");
  } else {
    next();
  }
});

export default router;
