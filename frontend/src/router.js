import {
  createWebHistory,
  createRouter
} from 'vue-router'
import RegisterPage from "./RegisterPage.vue"
import LoginPage from "./LoginPage.vue"
// import Tasks from "./Tasks.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      component: LoginPage
    },
    {
      path: "/register",
      component: RegisterPage
    },
    {
      path: "/tasks",
      component: () => import('./Tasks.vue')
    },
    {
      path: "/",
      component: () => import('./Tasks.vue')
    }
  ]

})

export { router }