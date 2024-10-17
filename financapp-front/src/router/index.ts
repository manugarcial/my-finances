import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
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
  },
  {
    path: "/global-economy-data",
    name: "global-economy-data",
    component: () => import("../views/GlobalEconomyDataView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
