import Vue from 'vue'
import Router from 'vue-router'
import Matches from '@/components/Matches.vue'
import Login from '@/components/Login.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Matches',
      component: Matches
    }
  ]
})
