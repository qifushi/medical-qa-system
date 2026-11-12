import Layout from '@/layout/main-layout/index.vue'

const modelManage = {
  path: '/modelManage',
  name: 'modelManage',
  meta: { title: '模型管理',icon:'app-menu-modelManage' },
  redirect: '/template',
  // component: Layout,
  children: [
    {
      path: '/template',
      name: 'template',
      meta: {
        icon: 'app-template',
        iconActive: 'app-template-active',
        title: '版本管理',
        activeMenu: '/modelManage',
        parentPath: '/modelManage',
        parentName: 'modelManage',
      },
      component: () => import('@/views/template/index.vue')
    },
    // {
    //   path: '/versionManage',
    //   name: 'versionManage',
    //   meta: {
    //     // isTopmenu: true,
    //     title: '版本管理',
    //     activeMenu: '/modelManage',
    //     parentPath: '/modelManage',
    //     parentName: 'modelManage'
    //   },
    //   component: () => import('@/views/modelManage/versionManage/index.vue')
    // },
    // {
    //   path: '/modelFineTune',
    //   name: 'modelFineTune',
    //   meta: {
    //     // isTopmenu: true,
    //     icon:'Cpu',
    //     title: '数据准备',
    //     activeMenu: '/modelManage',
    //     parentPath: '/modelManage',
    //     parentName: 'modelManage'
    //   },
    //   component: () => import('@/views/modelManage/modelFineTune/index.vue')
    // },
    // {
    //   path: '/modelEvaluation',
    //   name: 'modelEvaluation',
    //   meta: {
    //     // isTopmenu: true,
    //     icon:'Histogram',
    //     title: '模型评测',
    //     activeMenu: '/modelManage',
    //     parentPath: '/modelManage',
    //     parentName: 'modelManage'
    //   },
    //   component: () => import('@/views/modelManage/modelEvaluation/index.vue')
    // }
  ]
}
export default modelManage
