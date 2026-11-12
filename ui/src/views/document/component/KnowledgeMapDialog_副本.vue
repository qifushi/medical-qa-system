<template>
  <el-dialog
    title="知识图谱"
    v-model="dialogVisible"
    width="80%"
    class="select-dataset-dialog"
    style="position: relative"
  >
    <div ref="chartRef" class="knowledge-graph" style="width: 100%; height: 500px"></div>
    <div class="add_sub_button">
      <el-button @click="zoomMap(1.2)">+</el-button>
      <el-button @click="zoomMap(0.8)">-</el-button>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import documentApi from '@/api/document'
import * as echarts from 'echarts'
import { onMounted, ref } from 'vue'

// 控制弹窗的可见性
const dialogVisible = ref(false)

// 引用图表容器的 DOM 元素
const chartRef = ref<HTMLElement | null>(null)
// ECharts 实例，用于管理图表
let chartInstance: echarts.ECharts | null = null

// 放大/缩小图表
const zoomMap = (scale: number) => {
  if (!chartInstance) return
  // 确保 series 存在且为数组
  const series = chartInstance.getOption().series
  if (!series || !Array.isArray(series) || series.length === 0) {
    return
  }
  // 获取当前缩放级别
  const currentZoom = series?.[0]?.zoom || 1

  // 计算新的缩放比例
  const newZoom = currentZoom * scale

  // 设置缩放范围
  chartInstance.setOption({
    series: [
      {
        zoom: newZoom
      }
    ]
  })
}
// 处理接口返回的数据，将其转换为 ECharts 格式
const transformData = (res: any) => ({
  nodes: res.data.nodes.map((node: any) => ({
    name: node.properties.name, // 节点名称
    category: node.labels[0], // 节点类别
    draggable: true, // 节点是否可拖拽
    id: node.element_id, // 节点的唯一标识
    x: Math.floor(Math.random() * 101), // 生成0到100之间的随机整数
    y: Math.floor(Math.random() * 101) // 生成0到100之间的随机整数
  })),
  links: res.data.relationships.map((rel: any) => ({
    source: rel.start_node_element_id, // 关系的起始节点
    target: rel.end_node_element_id, // 关系的目标节点
    label: { show: true, formatter: rel.type } // 关系标签显示及格式
  }))
})

// 渲染图表的函数
const renderChart = (nodes: any[], links: any[]) => {
  if (!chartRef.value) return

  // ECharts 配置项
  const option: echarts.EChartsOption = {
    tooltip: {}, // 提示框组件，显示节点/边的详细信息
    animationDuration: 1000, // 图表动画的持续时间
    animationEasingUpdate: 'quinticInOut', // 图表动画的缓动效果
    // 普通关系图配置，需单独设置每个节点位置
    series: [
      {
        type: 'graph',
        layout: 'none', // 保持无布局，手动控制节点位置
        data: nodes,
        links: links,
        roam: true,
        symbolSize: 60,
        edgeSymbol: ['', 'arrow'],
        edgeSymbolSize: [2, 10],
        color: [
          '#ea9b70',
          '#c092bd',
          '#d6c9b1',
          '#9bca98',
          '#e06f6b',
          '#e3b7c8',
          '#5c8cd4',
          '#a6abb5'
        ], // 节点颜色
        categories: [
          { name: 'Document', itemStyle: { color: '#c092bd' } }, // Document 节点的颜色配置
          { name: 'Chunk', itemStyle: { color: '#ea9b70' } }, // Chunk 节点的颜色配置
          { name: 'Certificate', itemStyle: { color: '#FFC300' } } // Certificate 节点的颜色配置
        ],
        // force: {
        //   repulsion: 400, // 节点间的排斥力
        //   edgeLength: 300, // 关系连接线的长度
        //   layoutAnimation: true, // 是否启用力引导布局的动态动画
        //   friction: 0.6 // 摩擦力系数，控制节点移动的阻力
        // },
        edgeLabel: {
          show: true,
          position: 'middle', // 确保标签显示在连线上
          align: 'center'
          // width: 120, // 标签宽度
          // padding: 4, // 标签内边距
          // overflow: 'truncate' // 标签超出部分显示省略号
        },
        lineStyle: {
          color: 'source',
          opacity: 0.9,
          width: 1
        },
        label: {
          show: true,
          color: '#fff', // 节点标签文字颜色
          formatter: '{b}',
          fontSize: 12,
          padding: 4,
          width: 50,
          overflow: 'truncate'
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: { width: 5 }
        }
      }
    ]
    // 力导图配置：
    // series: [
    //   {
    //     type: 'graph', // 指定图表类型为关系图
    //     layout: 'force', // 通过力引导布局对节点进行排列
    //     data: nodes, // 节点数据
    //     links: links, // 边数据（节点关系）
    //     roam: true, // 启用缩放和平移功能
    //     symbolSize: 60, // 节点大小
    //     edgeSymbol: ['', 'arrow'], // 边的符号样式（箭头指向目标节点）
    //     edgeSymbolSize: [2, 10],
    //     color: [
    //       '#ea9b70',
    //       '#c092bd',
    //       '#d6c9b1',
    //       '#9bca98',
    //       '#e06f6b',
    //       '#e3b7c8',
    //       '#5c8cd4',
    //       '#a6abb5'
    //     ], // 节点颜色
    //     // force: {
    //     //   repulsion: 400, // 节点间的排斥力
    //     //   edgeLength: 300, // 关系连接线的长度
    //     //   layoutAnimation: true, // 是否启用力引导布局的动态动画
    //     //   friction: 0.6 // 摩擦力系数，控制节点移动的阻力
    //     // },
    //     categories: [
    //       { name: 'Document', itemStyle: { color: '#c092bd' } }, // Document 节点的颜色配置
    //       { name: 'Chunk', itemStyle: { color: '#ea9b70' } }, // Chunk 节点的颜色配置
    //       { name: 'Certificate', itemStyle: { color: '#FFC300' } } // Certificate 节点的颜色配置
    //     ],
    //     label: {
    //       show: true, // 显示节点标签
    //       color: '#fff', // 节点标签文字颜色
    //       formatter: '{b}', // 节点标签显示节点名称
    //       fontSize: 12, // 节点标签字体大小
    //       padding: 4, // 节点标签的内边距
    //       width: 50,
    //       overflow: 'truncate' // 节点标签超出部分显示省略号
    //     },
    //     lineStyle: {
    //       color: 'source', // 关系线的颜色来源节点
    //       opacity: 0.9, // 关系线的不透明度
    //       width: 1, // 关系线的宽度
    //       type: 'solid' // 关系线的样式类型
    //     },
    //     emphasis: {
    //       focus: 'adjacency', // 高亮相邻节点和关系
    //       lineStyle: { width: 5 } // 鼠标悬停时关系线的宽度
    //     },
    //     edgeLabel: {
    //       show: true, // 显示关系标签
    //       position: 'middle', // 关系标签位置
    //       // width: 120, // 标签宽度
    //       // padding: 4, // 标签内边距
    //       // overflow: 'truncate', // 标签超出部分显示省略号
    //       formatter: (params: any) => params.data.label?.formatter || params.data.label,
    //       align: 'center' // 标签对齐方式
    //     },
    //     labelLayout: {
    //       hideOverlap: false // 隐藏重叠元素
    //     }
    //   }
    // ]
  }

  // 初始化或更新 ECharts 实例的配置
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }
  chartInstance.setOption(option)
}

// 获取数据并渲染图表
const getData = async (row: any) => {
  const res = await documentApi.postknowledgeMap(row.dataset_id, row.id, { filename: row.name })
  console.log(res, 'res')

  const { nodes, links } = transformData(res)
  renderChart(nodes, links)
}

// 打开弹窗并加载图表数据
const open = async (row: any) => {
  dialogVisible.value = true
  await getData(row)
}

// 向外暴露 open 方法供父组件调用
defineExpose({ open })

// 组件挂载时初始化图表
onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
  }
})
</script>

<style lang="scss" scoped>
.knowledge-graph {
  width: 100%;
  height: 500px;
}
.add_sub_button {
  position: absolute;
  bottom: 140px;
  right: 100px;
  display: flex;
  flex-direction: column;
  .el-button {
    padding: 14px !important;
  }
  .el-button + .el-button {
    margin-left: 0px !important;
    margin-top: 2px;
  }
}
</style>
