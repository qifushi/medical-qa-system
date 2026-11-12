<template style="position: relative">
  <CreatePage
    v-if="isEmptyOfData"
    v-model="isEmptyOfData"
    @update:modelValue="handleCreatePageClose"
  ></CreatePage>

  <div v-else class="source-main-container">
    <!-- <sidebar @select="handleMenuSelect" /> -->
    <LeftTagsList v-model="selectedTags"></LeftTagsList>
    <div class="main-container">
      <SourceList ref="sourceListRef" v-model="selectedTags" />
    </div>
    <!-- ECharts 容器 -->
    <!-- <div class="treemap-container" style="display: none;">
      <div id="treemap" style="width: 100%; height: 100%"></div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CreatePage from './components/CreatePage.vue'
import SourceList from './components/SourceList.vue'
import LeftTagsList from './components/LeftTagsList.vue'
// import * as echarts from 'echarts'
import trainSourceApi from '@/api/train-source'




const isEmptyOfData = ref(false)
const sourceListRef = ref()


// 检查是否有数据源
const checkHasData = async () => {
  try {
    trainSourceApi.postTrainSourceList({ current_page: 1, page_size: 10 }, {}).then((res) => {
      console.log(res, 'res111')
      isEmptyOfData.value =  !(res.data && res.data.records.length > 0)
    })

  } catch (error) {
    console.error('获取数据源列表失败:', error)
  }
}

// 处理创建页面关闭
const handleCreatePageClose = (value: boolean) => {
  isEmptyOfData.value = value
  if (!value) {
    // 刷新数据列表
    refreshDataList()
  }
}
const refreshDataList = () => {
  // 先检查是否有数据
  checkHasData()
  // 如果有数据，刷新列表
  if (!isEmptyOfData.value) {
    sourceListRef.value?.getList()
  }
}
const selectedTags = ref({
  type: '', // 数据源类型
  tags: [] // 其他标签
})


// function getLevelOption() {
//   return [
//     {
//       itemStyle: {
//         borderWidth: 0,
//         gapWidth: 2
//       }
//     },
//     {
//       itemStyle: {
//         gapWidth: 1
//       }
//     },
//     {
//       colorSaturation: [0.35, 0.5],
//       itemStyle: {
//         gapWidth: 1,
//         borderColorSaturation: 0.6
//       }
//     }
//   ]
// }

// const formatUtil = echarts.format
// 初始化 ECharts 图表
// const initTreemap = () => {
//   const chartDom = document.getElementById('treemap')
//   if (chartDom) {
//     // 检查 chartDom 是否为有效的元素
//     const myChart = echarts.init(chartDom)
//     const option = {
//       title: {
//         show: false // 设置标题不可见
//       },
//       series: [
//         {
//           breadcrumb: { show: false },
//           type: 'treemap',
//           data: convertToTreemapData(),
//           levels: getLevelOption(),
//           top: '0px',
//           left: '0px',
//           right: '0px',
//           bottom: '0px',
//           width: '100%',
//           height: '100%',
//           roam: 'move' // 设置可平移，不可缩放
//         }
//       ],

//       tooltip: {
//         formatter: function (info: any) {
//           var value = info.value
//           var treePathInfo = info.treePathInfo
//           var treePath = []
//           for (var i = 1; i < treePathInfo.length; i++) {
//             treePath.push(treePathInfo[i].name)
//           }
//           return [
//             '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
//             '出现次数: ' + formatUtil.addCommas(value) + ' 次'
//           ].join('')
//         }
//       }
//     }
//     myChart.setOption(option)
//     // 监听容器大小变化
//     const resizeObserver = new ResizeObserver(() => {
//       myChart.resize()
//     })
//     resizeObserver.observe(chartDom)
//   }
// }


// ==后期数据需要按照真实的改变==
// const sourceList = ref([])
// const getTagFrequency = () => {
//   const freqMap: Record<string, number> = {}
//   sourceList.value.forEach((item) => {
//     ;(item.tags || []).forEach((tag) => {
//       freqMap[tag] = (freqMap[tag] || 0) + 1
//     })
//   })
//   return freqMap
// }
// const convertToTreemapData = () => {
//   const freqMap = getTagFrequency()
//   return Object.keys(freqMap).map((tag) => ({
//     name: tag,
//     value: freqMap[tag]
//   }))
// }

// const getList = () => {
//   trainSourceApi.getTrainSourceList({ current_page: 1, page_size: 10 }, {}).then((res) => {
//     console.log(res,'res');
    
//     // sourceList.value = res.data.data
//   })
// }

// 组件挂载时检查数据
onMounted(() => {
  // getList()
  checkHasData()
  // initTreemap() // echarts
})
</script>

<style lang="scss" scoped>
.source-main-container {
  width: 100%;
  height: calc(100vh - 56px);
  display: flex;
  .main-container {
    flex: 1;
    // padding: 20px;
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .title {
        font-size: 18px;
        font-weight: 600;
      }
    }
  }
}
.treemap-container {
  position: fixed;
  right: 10px;
  bottom: 10px;
  width: 100px;
  height: 100px;
  overflow: hidden;
  transform-origin: bottom right;
  transition:
    width 0.5s ease,
    height 0.5s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  &:hover {
    width: 40%;
    height: 60%;
  }
}
</style>