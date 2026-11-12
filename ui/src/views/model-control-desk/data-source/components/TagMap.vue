<template>
  <div class="tag-map-container">
    <relation-graph
      ref="graphRef"
      :options="options"
      @node-click="handleNodeClick"
      @node-hover="handleNodeHover"
    >
      <template #node="{ node }: { node: RGNode & { text: string } }">
        <div class="my-node">
          <el-tooltip effect="dark" :content="node.text.split('\n')[0]" placement="top">
            <div class="node-title">
              {{ node.text.split('\n')[0] }}
            </div>
          </el-tooltip>
          <div class="node-count">
            {{ node.text.split('\n')[1] }}
          </div>
        </div>
      </template>
    </relation-graph>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { RGJsonData, RGNode, RGLink, RGOptions } from 'relation-graph-vue3'
import RelationGraph from 'relation-graph-vue3'
// 模拟标签数据
const tags = [
  { id: 't1', name: '生产数据生产数据', count: 15, type: 'success' },
  { id: 't2', name: '质检记录', count: 8, type: 'warning' },
  { id: 't3', name: '设备维护', count: 12, type: 'primary' },
  { id: 't4', name: '研发测试', count: 6, type: 'info' },
  { id: 't5', name: '故障诊断', count: 10, type: 'danger' },
  { id: 't6', name: '性能监控', count: 9, type: 'warning' },
  { id: 't7', name: '预测分析', count: 7, type: 'success' },
  { id: 't8', name: '工艺参数', count: 11, type: 'primary' }
]

// 计算节点大小
const calculateNodeSize = (count: number) => {
  const baseSize = 30 // 减小基础大小
  const maxSize = 90 // 设置最大尺寸
  const scale = Math.log(count + 1) * 1.2
  return Math.min(maxSize, Math.max(baseSize, baseSize * scale))
}

// 图谱配置
const options: RGOptions = {
  layouts: [
    {
      layoutName: 'force'
    }
  ],
  defaultNodeColor: '#2f95dc',
  defaultLineColor: '#93cddc',
  allowSwitchLineShape: true,
  allowSwitchJunctionPoint: true,
  defaultJunctionPoint: 'border',
  allowShowMiniToolBar: false
}

// 构建图谱数据
const graphJsonData: RGJsonData = {
  rootId: 'center',
  nodes: [
    {
      id: 'center',
      text: 'Model Studio',
      color: '#1890ff',
      borderColor: '#1890ff',
      width: 60,
      height: 60
    },
    ...tags.map((tag) => ({
      id: tag.id,
      text: `${tag.name}\n(${tag.count})`,
      color: getTagColor(tag.type),
      borderColor: getTagColor(tag.type),
      width: calculateNodeSize(tag.count),
      height: calculateNodeSize(tag.count)
    }))
  ],
  lines: tags.map((tag) => ({
    from: 'center',
    to: tag.id,
    text: '',
    color: getTagColor(tag.type)
  }))
}

// 获取标签颜色
function getTagColor(type: string): string {
  const colorMap: Record<string, string> = {
    success: '#67C23A',
    warning: '#E6A23C',
    danger: '#F56C6C',
    primary: '#409EFF',
    info: '#909399'
  }
  return colorMap[type] || '#909399'
}

// 处理节点点击
const handleNodeClick = (node: RGNode) => {
  console.log('节点点击:', node)
}

// 处理节点悬停
const handleNodeHover = (node: RGNode) => {
  console.log('节点悬停:', node)
}

const graphRef = ref<RelationGraph>()

onMounted(() => {
  // 初始化图谱
  setTimeout(() => {
    graphRef.value?.setJsonData(graphJsonData)
  }, 300)
})
</script>

<style lang="scss" scoped>
.tag-map-container {
  width: 100%;
  // height: 100%;
  height: calc(100vh - var(--app-header-height));
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);

  :deep(.relation-graph) {
    width: 100%;
    height: 100%;
  }
  .my-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 0 2px;
  }

  .node-title {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 600;
    font-size: 15px;
    color: #fff;
    text-align: center;
    cursor: pointer;
  }

  .node-count {
    margin-top: 2px;
    font-size: 13px;
    //   color: #00eaff;
    text-align: center;
    font-family: monospace;
  }
}
</style>
