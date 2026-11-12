import Layout from '@/layout/main-layout/index.vue'
const applicationRouter = {
  path: '/application',
  name: 'application',
  meta: { title: '应用管理', permission: 'APPLICATION:READ', icon: 'app-menu-robot' },
  redirect: '/allApplication',
  component: Layout,
  children: [
    {
      path: '/allApplication',
      name: 'allApplication',
      meta: {
        icon: 'app-all-menu',
        iconActive: 'app-all-menu-active',
        title: '全部应用',
        permission: 'APPLICATION:READ',
        activeMenu: '/application',
        parentPath: '/application',
        parentName: 'application',
      },
      component: () => import('@/views/application/index.vue')
    },
    {
      path: '/talk',
      name: 'talk',
      meta: {
        icon: 'ChatLineSquare',
        // iconActive: 'app-all-menu-active',
        title: '对话类应用',
        permission: 'APPLICATION:READ',
        activeMenu: '/application',
        parentPath: '/application',
        parentName: 'application',
      },
      component: () => import('@/views/application/talkApplication/index.vue')
    },
    {
      path: '/generate',
      name: 'generate',
      meta: {
        icon: 'Edit',
        title: '生成类应用',
        permission: 'APPLICATION:READ',
        activeMenu: '/application',
        parentPath: '/application',
        parentName: 'application',
      },
      component: () => import('@/views/application/generateApplication/index.vue')
    },
    {
      path: '/generate/:id/:type',
      name: 'generateApplicationDetail',
      meta: {
        title: '生成类应用',
        activeMenu: '/application',
        hidden:true
      },
      hidden: true,
      children: [
        {
          path: 'createTask',
          name: 'createTask',
          meta: {
            icon: 'Brush',
            title: '创建任务',
            active: 'createTask',
            parentPath: '/generate/:id/:type',
            parentName: 'generateApplicationDetail'
          },
          component: () => import('@/views/application/generateApplication/component/createGenerateApplication.vue')
        },
        {
          path: 'generateLog',
          name: 'generateLog',
          meta: {
            icon: 'app-document',
            iconActive: 'app-document-active',
            title: '对话日志',
            active: 'generateLog',
            parentPath: '/generate/:id/:type',
            parentName: 'generateApplicationDetail'
          },
          component: () => import('@/views/log/index.vue')
        }
      ]
    },
    {
      path: '/application/create',
      name: 'CreateApplication',
      meta: {
        activeMenu: '/application',
        hidden: true
      },
      component: () => import('@/views/application/CreateAndSetting.vue'),
      hidden: true
    },
    {
      path: '/application/:id/:type',
      name: 'ApplicationDetail',
      meta: {
        title: '应用详情',
        activeMenu: '/application',
        hidden: true
      },
      // component: Layout,
      hidden: true,
      children: [
        {
          path: 'overview',
          name: 'AppOverview',
          meta: {
            icon: 'app-all-menu',
            iconActive: 'app-all-menu-active',
            title: '概览',
            active: 'overview',
            parentPath: '/application/:id/:type',
            parentName: 'ApplicationDetail'
          },
          component: () => import('@/views/application-overview/index.vue')
        },
        {
          path: 'setting',
          name: 'AppSetting',
          meta: {
            icon: 'app-setting',
            iconActive: 'app-setting-active',
            title: '设置',
            active: 'setting',
            parentPath: '/application/:id/:type',
            parentName: 'ApplicationDetail'
          },
          component: () => import('@/views/application/ApplicationSetting.vue')
        },
        {
          path: 'hit-test',
          name: 'AppHitTest',
          meta: {
            icon: 'app-hit-test',
            title: '命中测试',
            active: 'hit-test',
            parentPath: '/application/:id/:type',
            parentName: 'ApplicationDetail'
          },
          component: () => import('@/views/hit-test/index.vue')
        },
        {
          path: 'log',
          name: 'Log',
          meta: {
            icon: 'app-document',
            iconActive: 'app-document-active',
            title: '对话日志',
            active: 'log',
            parentPath: '/application/:id/:type',
            parentName: 'ApplicationDetail'
          },
          component: () => import('@/views/log/index.vue')
        }
      ]
    }
  ]
}

export default applicationRouter
