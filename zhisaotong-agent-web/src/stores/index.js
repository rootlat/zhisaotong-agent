import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Chat from '../views/Chat.vue'
import Upload from '../views/Upload.vue'

const routes = [
   { path: '/', redirect: '/chat' },
   { path: '/login', component: Login },
   { path: '/register', component: Register },
   { path: '/chat', component: Chat },
   { path: '/upload', component: Upload }
]

const router = createRouter({
   history: createWebHistory(),
   routes
})

router.beforeEach((to, from, next) => {
   const token = localStorage.getItem('token')
   if (to.path === '/login' || to.path === '/register') {
      next()
   } else {
      token ? next() : next('/login')
   }
})

export default router