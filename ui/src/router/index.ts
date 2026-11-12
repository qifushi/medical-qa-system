import { routes } from '@/router/routes'
import useStore from '@/stores'
import { hasPermission } from '@/utils/permission/index'
import { ElMessageBox } from 'element-plus'
import {
  createRouter,
  createWebHistory,
  type NavigationGuardNext,
  type RouteLocationNormalized,
  type RouteRecordName,
  type RouteRecordRaw
} from 'vue-router'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

// 路由前置拦截器
router.beforeEach(
  async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    if (to.name === '404') {
      next()
      return
    }
    const { user } = useStore()
    const notAuthRouteNameList = [
      'register',
      'login',
      'forgot_password',
      'reset_password',
      'Chat',
      'GatewayPage',
      "ModelControlIndex",
      // 医疗模块（知贝）免登录直接访问
      'graphAssistant',
      'medicalConsult',
      'reportAnalysis',
      'medicalService',
      'medicineAnalysis',
      'doctorMain'
    ]

    const token = user.getToken()
    if (!notAuthRouteNameList.includes(to.name ? to.name.toString() : '')) {
      if (!token) {
        const currentPath = window.location.pathname

        // 如果未登录，显示弹窗提示用户操作
        ElMessageBox.confirm('您的登录状态已过期，是否重新登录？', '登录提示', {
          confirmButtonText: '重新登录',
          cancelButtonText: '返回首页',
          type: 'warning',
          distinguishCancelAndClose: true,
        })
          .then((flag) => {
            let redirect = ''
            // 点击确认后跳转到登录页面
            router.push({
              path: '/login', query: {
                redirect: currentPath.indexOf('/model-control-desk') > -1 ? 'ModelControlIndex' : 'home'
              }
            })
          })
          .catch((action) => {
            if (action === 'cancel') {
              currentPath.indexOf('/model-control-desk') > -1 ? router.push({ name: 'ModelControlIndex' }) : router.push({ name: 'home' })
            }
          })
        //old
        // next({
        //   path: '/login'
        // })
        return
      }
    }
    if (!user.userInfo && token) {
      await user.profile()
    }
    // 判断是否有菜单权限
    if (to.meta.permission ? hasPermission(to.meta.permission as any, 'OR') : true) {
      next()
    } else {
      // 如果没有权限则直接取404页面
      next('404')
    }
  }
)

export const getChildRouteListByPathAndName = (path: any, name?: RouteRecordName | any) => {
  return getChildRouteList(routes, path, name)
}

export const getChildRouteList: (
  routeList: Array<RouteRecordRaw>,
  path: string,
  name?: RouteRecordName | null | undefined
) => Array<RouteRecordRaw> = (routeList, path, name) => {
  for (let index = 0; index < routeList.length; index++) {
    const route = routeList[index]
    if (name === route.name && path === route.path) {
      return route.children || []
    }
    if (route.children && route.children.length > 0) {
      const result = getChildRouteList(route.children, path, name)
      if (result && result?.length > 0) {
        return result
      }
    }
  }
  return []
}

export default router
