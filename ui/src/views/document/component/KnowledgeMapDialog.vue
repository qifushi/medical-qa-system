<template>
  <el-dialog
    title="知识图谱"
    v-model="dialogVisible"
    width="90%"
    class="select-dataset-dialog"
    style="position: relative"
    :before-close="close"
    v-if="dialogVisible"
    destroy-on-close
  >
    <div v-loading="loading" ref="myPage" class="my-graph" style="height: calc(100vh)">
      <RelationGraph
        ref="graphRef"
        :options="graphOptions"
        @node-click="onNodeClick"
        @line-click="onLineClick"
        @canvas-click="onCanvasClick"
      >
        <template #node="{ node }: { node: RGNode & { text: string } }">
          <div
            class="my-node ellipsis-3"
            @mouseover="highlightConnectedNodes(node)"
            @mouseleave="resetNodesVisibility()"
          >
            {{ node.text }}
          </div>
        </template>
      </RelationGraph>
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
import type {
  RelationGraphComponent,
  RGJsonData,
  RGLine,
  RGLink,
  RGNode,
  RGOptions,
  RGUserEvent
} from 'relation-graph-vue3'
import RelationGraph from 'relation-graph-vue3'
import { onMounted, ref } from 'vue'
const props = defineProps({
  row: {
    type: Object,
    default: {}
  }
})
const graphRef = ref<RelationGraphComponent>()

const graphOptions: RGOptions = {
  downloadImageFileName: '知识图谱',
  moveToCenterWhenRefresh: false,
  zoomToFitWhenRefresh: false,
  useAnimationWhenRefresh: true,
  hideNodeContentByZoom: true,
  defaultLineColor: 'rgba(171, 165, 165, 1)',
  layouts: [
    {
      label: '中心',
      layoutName: 'force',
      centerOffset_x: 0,
      centerOffset_y: 0,
      distance_coefficient: 1,
      maxLayoutTimes: 300,
      force_node_repulsion: 1,
      force_line_elastic: 1,
      from: 'top',
      levelDistance: '',
      min_per_width: 100,
      max_per_width: 600,
      min_per_height: 300,
      max_per_height: 600
    }
  ]
}
const loading = ref(false)
const onCanvasClick = ($event: RGUserEvent) => {
  const graphInstance = graphRef.value?.getInstance()
  console.log('onCanvasClick:', $event)
  if (graphInstance) {
    graphInstance.clearChecked()
  }
}
const onNodeClick = (nodeObject: RGNode, $event: RGUserEvent) => {
  // Handle node click event
}
const onLineClick = (lineObject: RGLine, linkObject: RGLink, $event: RGUserEvent) => {
  // Handle line click event
}
const showGraph = async (nodes: any, lines: any) => {
  const __graph_json_data: RGJsonData = {
    rootId: 'root',
    nodes: nodes,
    lines: lines
  }
  const graphInstance = graphRef.value?.getInstance()
  if (!graphInstance) return

  await graphInstance.setJsonData(__graph_json_data)
  // await graphInstance.moveToCenter()
  // await graphInstance.zoomToFit()
  await graphInstance.refresh()
}
// 控制弹窗的可见性
const dialogVisible = ref(false)
// 处理接口返回的数据，将其转换为 ECharts 格式
const transformData = (res: any) => ({
  nodes: res.data.nodes.map((node: any) => ({
    text: node.properties.name, // 节点名称
    category: node.labels[0], // 节点类别
    id: node.element_id // 节点的唯一标识
  })),
  links: res.data.relationships.map((rel: any) => ({
    from: rel.start_node_element_id, // 关系的起始节点
    to: rel.end_node_element_id, // 关系的目标节点
    text: rel.type // 关系标签
  }))
})
// 获取数据并渲染图表
const getData = async (row: any) => {
  let res = await documentApi.postknowledgeMap(
    row.dataset_id,
    row.id,
    { filename: row.name },
    loading
  )
  console.log(res, 'res')

  const { nodes, links } = transformData(res)
  console.log(nodes, links, 'links')

  showGraph(nodes, links) //demo 数据
}
// 打开弹窗并加载图表数据
const open = async (row: any) => {
  dialogVisible.value = true

  getData(row)
}

// 鼠标悬浮时高亮相连的节点和连线
const highlightConnectedNodes = (node: RGNode) => {
  const graphInstance = graphRef.value?.getInstance()
  if (!graphInstance) return

  // 获取所有节点和连线
  const allNodes = graphInstance.getNodes()
  const allLines = graphInstance.getLines()

  // 找出相连的节点
  const connectedNodeIds = new Set([node.id])
  allLines.forEach((line) => {
    if (line.from === node.id) {
      connectedNodeIds.add(line.to)
    }
    if (line.to === node.id) {
      connectedNodeIds.add(line.from)
    }
  })

  // 更新所有节点的透明度
  allNodes.forEach((n) => {
    n.opacity = connectedNodeIds.has(n.id) ? 1 : 0.2
  })

  // 更新所有连线的透明度
  allLines.forEach((line) => {
    line.opacity = connectedNodeIds.has(line.from) && connectedNodeIds.has(line.to) ? 1 : 0.2
  })

  // graphInstance.refresh()
}

const resetNodesVisibility = () => {
  const graphInstance = graphRef.value?.getInstance()
  if (!graphInstance) return

  // 重置所有节点和连线为完全不透明
  graphInstance.getNodes().forEach((node) => {
    node.opacity = 1
  })
  graphInstance.getLines().forEach((line) => {
    line.opacity = 1
  })

  // graphInstance.refresh()
}
const close = () => {
  dialogVisible.value = false
}
// 向外暴露 open 方法供父组件调用
defineExpose({ open })

// 组件挂载时初始化图表
onMounted(() => {
  console.log('挂载')
})
</script>

<style lang="scss" scoped>
.knowledge-graph {
  width: 100%;
  height: 500px;
  background-color: darkslategray;
}
.my-graph {
  display: flex;
  place-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  .my-node {
    // padding: 10px;
    cursor: pointer;
    transition: opacity 0.3s ease;
  }
}
:deep(.rel-node) {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}
.ellipsis-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  overflow: hidden;
}
</style>
