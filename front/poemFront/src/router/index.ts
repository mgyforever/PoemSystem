import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'poetry',
      component: () => import('../views/PoetryView.vue'),
    },
    {
      path: '/chain',
      name: 'chain',
      component: () => import('../views/ChainView.vue'),
    },
    {
      path: '/feihua',
      name: 'feihua',
      component: () => import('../views/FeihuaView.vue'),
    },
  ],
})

export default router
