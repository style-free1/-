import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import LayoutView from '../views/LayoutView.vue'
import DashboardView from '../views/DashboardView.vue'
import UsersView from '../views/UsersView.vue'
import ProductsView from '../views/ProductsView.vue'
import BehaviorsView from '../views/BehaviorsView.vue'
import PredictView from '../views/PredictView.vue'
import RecommendView from '../views/RecommendView.vue'
import SystemView from '../views/SystemView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginView },
    {
      path: '/',
      component: LayoutView,
      children: [
        { path: '', component: DashboardView },
        { path: 'users', component: UsersView },
        { path: 'products', component: ProductsView },
        { path: 'behaviors', component: BehaviorsView },
        { path: 'predict', component: PredictView },
        { path: 'recommend', component: RecommendView },
        { path: 'system', component: SystemView }
      ]
    }
  ]
})

router.beforeEach((to, _, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) return next('/login')
  next()
})

export default router
