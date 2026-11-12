import Layout from '@/layout/model-control-desk-layout/index.vue'
const modelControlDeskRouters = {
  path: '/model-control-desk',
  name: 'ModelControlDesk',
  meta: { title: '训练控制台', },
  redirect: '/model-control-desk/index',
  component: Layout,
  children: [

    {
      path: 'index', // 首页
      name: 'ModelControlIndex',
      meta: {
        cache: true
      },
      component: () => import('@/views/model-control-desk/index-page/index.vue'),
    },
    {
      path: 'model-release', // 模型发布
      name: 'ModelRelease',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-release/index.vue'),
    },
    {
      path: 'model-evaluation', // 模型评测
      name: 'ModelEvaluation',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-evaluation/index.vue'),
    },
    {
      path: 'evaluation-detail', // 评测页面
      name: 'EvaluationDetail',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-evaluation/modules/evaluationDeatil/index.vue'),
    },
    {
      path: 'model-evaluation/lateralComparison',// 横向对比
      name: 'ModelEvaluationLateralComparison',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-evaluation/components/lateralComparison.vue'),
    },
    {
      path: 'model-training', // 模型训练
      name: 'ModelTraining',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-training/index.vue'),
    },
    {
      path: 'model-training/simpleness', // 快速模型训练
      name: 'ModelTrainingSimpleness',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-training/simpleness-view.vue'),
    },
    {
      path: 'model-training/major', // 高级模型训练
      name: 'ModelTrainingMajor',
      meta: {
      },
      component: () => import('@/views/model-control-desk/model-training/major-view.vue'),
    },
    {
      path: 'data-treating', // 数据准备
      name: 'DataTreating',
      meta: {
      },
      component: () => import('@/views/model-control-desk/data-treating/index.vue'),
    },
    {
      path: 'data-source', // 数据源管理
      name: 'DataSource',
      meta: {
      },
      component: () => import('@/views/model-control-desk/data-source/index.vue'),
    },
    {
      path: '/data-source/:id',
      name: 'DataSourceDetail',
      meta: {
      },
      component: () => import('@/views/model-control-desk/data-source/components/DetailSoure.vue'),
    }

  ]
}

export default modelControlDeskRouters
