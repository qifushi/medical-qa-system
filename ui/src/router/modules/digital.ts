
const tool = {
  path: '/digital',
  name: 'digital',
  meta: { title: '数字人',icon: 'UserFilled' },
  redirect: '/digitalChat',
  // component: Layout,
  children: [
    {
      path: '/digitalChat',
      name: 'digitalChat',
      meta: {
        icon:'ChatLineSquare',
        title: '数字人对话',
        activeMenu: '/digital',
        parentPath: '/digital',
        parentName: 'digital',
        // isTopmenu: true,
      },
      component: () => import('@/views/digital/digitalChat/index.vue')
    },
    {
      path: '/digitalSetting',
      name: 'digitalSetting',
      meta: {
        icon:'setting',
        title: '数字人设置',
        activeMenu: '/digital',
        parentPath: '/digital',
        parentName: 'digital',
        // isTopmenu: true,
      },
      component: () => import('@/views/digital/digitalSetting/index.vue')
    },
    {
      path: '/digitalHistory',
      name: 'digitalHistory',
      meta: {
        icon:'app-document',
        title: '历史会话',
        activeMenu: '/digital',
        parentPath: '/digital',
        parentName: 'digital',
        // isTopmenu: true,
      },
      component: () => import('@/views/digital/digitalHistory/index.vue')

    },
  ]
}
export default tool
