import type { RouteRecordRaw } from 'vue-router'
import chatappRouter from './chatapp'
import modelControlDeskRouters from "./modelControlDesk";
const modules: any = import.meta.glob('./modules/*.ts', { eager: true })
const rolesRoutes: RouteRecordRaw[] = [...Object.keys(modules).map((key) => modules[key].default)]
export const routes: Array<RouteRecordRaw> = [
  // 兼容从 /ui/index.html 直接进入的场景（开发服务器只在 index.html 上有回退）
  {
    path: '/index.html',
    redirect: '/'
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/layout/app-layout/index.vue'),
    redirect: '/chatapp/medicalConsult',
    children: [...rolesRoutes]
  },
  ...chatappRouter, // chatapp页面路由
  modelControlDeskRouters,
  {
    path: '/gateway-page',
    name: 'GatewayPage',
    redirect: '/chatapp/medicalConsult'
  },
  {
    path: '/gateway-application-digitalChat',
    name: 'GatewayApplicationDigitalChat',
    component: () => import('@/views/gateway-page/pages/digitalChat/index.vue')
  },
  {
    path: '/gateway-application-scenarios-visualModel',
    name: 'GatewayApplicationScenariosVisualModel',
    component: () => import('@/views/gateway-page/pages/visualModel/index.vue')
  },
  {
    path: '/gateway-application-overview',
    name: 'GatewayApplicationOverview',
    component: () => import('@/views/gateway-page/pages/overviewPage/index.vue')
  },
  {
    path: '/gateway-application-scenarios',
    name: 'GatewayApplicationScenarios',
    component: () => import('@/views/gateway-page/pages/applicationScenarios/index.vue')
  },
  {
    path: '/audioCall',
    name: 'audioCall',
    meta: { type: 'audioCall' },
    component: () => import('@/views/audioCall/index.vue')
  },

  // 高级编排
  {
    path: '/application/:id/workflow',
    name: 'ApplicationWorkflow',
    meta: { activeMenu: '/application' },
    component: () => import('@/views/application-workflow/index.vue')
  },

  {
    path: '/chat/:accessToken',
    name: 'Chat',
    component: () => import('@/views/chat/index.vue')
  },

  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/login/register/index.vue')
  },
  {
    path: '/forgot_password',
    name: 'forgot_password',
    component: () => import('@/views/login/forgot-password/index.vue')
  },
  {
    path: '/reset_password/:code/:email',
    name: 'reset_password',
    component: () => import('@/views/login/reset-password/index.vue')
  },
  {
    path: '/:pathMatch(.*)',
    name: '404',
    component: () => import('@/views/404/index.vue')
  }
]
