import Layout from '@/layout/main-layout/index.vue'
import type { RouteRecordRaw } from 'vue-router'

const chatappRouter: RouteRecordRaw[] = [
  {
    path: '/chatapp',
    name: 'chatapp',
    meta: { type: 'chatapp-page', title: '八大应用' },
    redirect: 'industryTalk',
    component: Layout,
    children: [
      {
        path: 'industryTalk',
        name: 'industryTalk',
        meta: {
          icon: 'roll1.png',
          activeIcon: 'roll2.png',
          active: '/chatapp/industryTalk', // 激活的侧边菜单项
          title: '行业对话',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () => import('@/views/chatapp-page/index.vue')
      },
      {
        path: 'textGeneration/:id',
        name: 'textGeneration',
        meta: {
          icon: 'roll3.png',
          activeIcon: 'roll4.png',
          active: '/chatapp/textGeneration', // 激活的侧边菜单项
          title: '文本生成',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () =>
          import('@/views/chatapp-page/components/textGeneration/createGenerateApplication.vue')
      },
      {
        path: 'smartQuery',
        name: 'smartQuery',
        meta: {
          icon: 'roll5.png',
          activeIcon: 'roll6.png',
          active: '/chatapp/smartQuery', // 激活的侧边菜单项
          title: '智能查询',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () => import('@/views/chatapp-page/index.vue')
      },
      {
        path: 'createAippt',
        name: 'createAippt',
        meta: {
          icon: 'roll23.png',
          activeIcon: 'roll24.png',
          active: '/chatapp/pptApp', // 激活的侧边菜单项
          title: '智能PPT',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () => import('@/views/ppt-app/createAippt.vue')
      },
      {
        path: 'pptAppEdit',
        name: 'pptAppEdit',
        meta: {
          icon: 'roll13.png',
          activeIcon: 'roll14.png',
          active: '/chatapp/pptApp', // 激活的侧边菜单项
          title: 'ppt生成',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true // 已经有 hidden 字段
        },
        component: () => import('@/views/ppt-app/index.vue')
      },
      {
        path: 'documentRead',
        name: 'documentRead',
        meta: {
          icon: 'roll13.png',
          activeIcon: 'roll14.png',
          active: '/chatapp/documentRead', // 激活的侧边菜单项
          title: '文档阅读',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () => import('@/views/chatapp-page/index.vue')
      },
      {
        path: 'graphAssistant',
        name: 'graphAssistant',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/graphAssistant', // 激活的侧边菜单项
          title: '知贝',
          parentPath: '/chatapp',
          parentName: 'chatapp'
        },
        component: () => import('@/medical/views/RoleSelection.vue')
      },
      {
        path: 'medicalConsult',
        name: 'medicalConsult',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/medicalConsult',
          title: '知贝问诊',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true
        },
        component: () => import('@/medical/views/MedicalConsult.vue')
      },
      {
        path: 'reportAnalysis',
        name: 'reportAnalysis',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/reportAnalysis',
          title: '报告分析',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true
        },
        component: () => import('@/medical/views/ReportAnalysis.vue')
      },
      {
        path: 'medicalService',
        name: 'medicalService',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/medicalService',
          title: '就医服务',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true
        },
        component: () => import('@/medical/views/MedicalService.vue')
      },
      {
        path: 'medicineAnalysis',
        name: 'medicineAnalysis',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/medicineAnalysis',
          title: '药品分析',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true
        },
        component: () => import('@/medical/views/MedicineAnalysis.vue')
      },
      {
        path: 'doctorMain',
        name: 'doctorMain',
        meta: {
          icon: 'roll7.png',
          activeIcon: 'roll8.png',
          active: '/chatapp/doctorMain',
          title: '医生主界面',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          hidden: true
        },
        component: () => import('@/medical/views/DoctorMain.vue')
      },
      {
        path: 'complianceReview',
        name: 'complianceReview',
        meta: {
          icon: 'roll9.png',
          activeIcon: 'roll10.png',
          active: '/chatapp/complianceReview', // 激活的侧边菜单项
          title: '合规审查',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          disabled: true
        },
        component: () => import('@/views/chatapp-page/index.vue')
      },
      {
        path: 'languageAssistant',
        name: 'languageAssistant',
        meta: {
          icon: 'roll11.png',
          activeIcon: 'roll12.png',
          active: '/chatapp/languageAssistant', // 激活的侧边菜单项
          title: '语言助手',
          parentPath: '/chatapp',
          parentName: 'chatapp',
          disabled: true
        },
        component: () => import('@/views/chatapp-page/index.vue')
      }

    ]
  }
]

export default chatappRouter
