import Layout from '@/layout/main-layout/index.vue'

const tool = {
  path: '/tools',
  name: 'tools',
  meta: { title: '工具管理',icon: 'app-menu-tools' },
  redirect: '/sceneCenter',
  component: Layout,
  children: [
    {
      path: '/sceneCenter',
      name: 'sceneCenter',
      meta: {
        icon:'Grid',
        title: '场景中心',
        activeMenu: '/tools',
        parentPath: '/tools',
        parentName: 'tools',
        // isTopmenu: true,
      },
      component: () => import('@/views/tools/sceneCenter/index.vue')
    },
    {
      path: '/toolsManage',
      name: 'toolsManage',
      meta: {
        icon:'Paperclip',
        title: '工具组件',
        activeMenu: '/tools',
        parentPath: '/tools',
        parentName: 'tools',
        // isTopmenu: true,
      },
      component: () => import('@/views/tools/toolsManage/index.vue')
    },
  ]
}
export default tool
