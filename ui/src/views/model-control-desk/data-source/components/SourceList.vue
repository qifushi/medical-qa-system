<template>
  <div class="application-list-container p-24" style="padding-top: 16px">
    <div class="container-title mb-16">
      <h4>数据源管理</h4>
      <el-input
        v-model="searchValue"
        @change="searchHandle"
        placeholder="按名称、标签搜索"
        prefix-icon="Search"
        class="w-240"
        clearable
      />
    </div>
    <div class="container-search-result mb-16" v-if="modelValue.type || modelValue.tags.length">
      <div style="min-width: 80px">
        共 <span class="primary-color">{{ paginationConfig.total }}</span> 个结果
      </div>
      <div class="tags-container">
        <!-- 显示数据源类型标签 -->
        <el-tag
          v-if="modelValue.type"
          disable-transitions
          closable
          @close="clearType"
          type="primary"
        >
          {{ getTypeLabel(modelValue.type) }}
        </el-tag>

        <!-- 显示其他标签 -->
        <el-tag
          v-for="(tag, index) in modelValue.tags"
          :key="index"
          disable-transitions
          closable
          @close="removeTag(index)"
          type="primary"
        >
          {{ tag.value }}
        </el-tag>
      </div>
      <el-button type="info" link @click="clearSelectedTags">清空</el-button>
    </div>
    <div v-loading.fullscreen.lock="paginationConfig.current_page === 1 && loading">
      <InfiniteScroll
        :size="tableData.length"
        :total="paginationConfig.total"
        :page_size="paginationConfig.page_size"
        v-model:current_page="paginationConfig.current_page"
        @load="getList"
        :loading="loading"
      >
        <el-row :gutter="15">
          <el-col :xs="24" :sm="12" :md="12" :lg="8" :xl="8" class="mb-16">
            <CardAdd title="创建数据源" @click="openCreateDialog" />
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="8"
            :xl="8"
            v-for="(item, index) in tableData"
            :key="index"
            class="mb-16"
          >
            <CardBoxSource
              :title="item.name"
              :tags="item.allTags"
              :description="item.describe"
              class="application-card cursor boxShadow"
              @click="handleJumpSourceData(item)"
            >
              <template #icon>
                <el-tooltip placement="top" :content="getSourceTypeName(item.type)">
                  <el-icon
                    style="padding: 4px; border-radius: 4px; margin-right: 8px"
                    :size="14"
                    :style="{
                      border: `1px solid ${getIconBorderColorAndIconcolor(item.type)}`,
                      color: getIconBorderColorAndIconcolor(item.type)
                    }"
                  >
                    <component :is="getDefaultIcon(item)" />
                  </el-icon>
                </el-tooltip>
              </template>

              <template #footer>
                <div class="footer-content">
                  <el-tooltip effect="dark" content="编辑" placement="top">
                    <el-button text @click.stop="handleEdit(item)">
                      <AppIcon iconName="Setting"></AppIcon>
                    </el-button>
                  </el-tooltip>
                  <el-divider direction="vertical" />
                  <el-tooltip effect="dark" content="删除" placement="top">
                    <el-button text @click.stop="handleDelete(item)">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </el-tooltip>
                </div>
              </template>
            </CardBoxSource>
          </el-col>
        </el-row>
      </InfiniteScroll>
    </div>
    <!-- <CreateApplicationDialog ref="CreateApplicationDialogRef" /> -->
    <!-- 页脚 -->
    <!-- <div v-if="logoAndCopyright.isShowLogoAndCopyright" class="footer">
      <p>Copyright © 2023-2025 杰软科技（集团）有限公司</p>
    </div> -->
    <AddSourceDialog ref="AddSourceDialogRef" @refresh="getList" />
  </div>
</template>

<script setup lang="ts">
import trainSourceApi from '@/api/train-source'
import { ref, reactive, watch, onMounted } from 'vue'
// import { isAppIcon, isWorkFlow } from '@/utils/application'
import AddSourceDialog from './AddSourceDialog.vue'
// import { Folder, Document, DataLine, Share } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { tagsList } from '../type/tag'
import _ from 'lodash'
import { MsgSuccess,MsgConfirm } from '@/utils/message'


const router = useRouter()
// 定义数据源类型枚举
enum SourceType {
  FILE = '0',
  DATABASE = '1',
  GRAPH = '2'
}

// 定义数据源类型映射
const SourceTypeMap: Record<SourceType, string> = {
  [SourceType.FILE]: '文件型数据源',
  [SourceType.DATABASE]: '数据库数据源',
  [SourceType.GRAPH]: '知识图谱数据源'
}

// 定义表格数据接口
interface DataSourceItem {
  id: string
  name: string
  describe: string
  type: SourceType
  icon?: string
  tags?: string[]
  custom_tags: ''
  allTags?: string[] // 用于存储合并后的标签
}
const props = defineProps<{
  sourceType?: string
  modelValue: {
    type: string
    tags: any[]
  }
}>()
const emit = defineEmits(['update:modelValue'])
const loading = ref(false)
const tableData = ref<DataSourceItem[]>([])

// 获取数据源类型名称（用于列表项）
const getSourceTypeName = (type: SourceType): string => {
  console.log('%c [ type ]-243', 'font-size:13px; background:pink; color:#bf2c9f;', type)

  return SourceTypeMap[type] || '未知类型'
}
// 获取图标边框颜色\图标颜色
const getIconBorderColorAndIconcolor = (type: SourceType): string => {
  const colorMap: Record<SourceType, string> = {
    [SourceType.FILE]: 'var(--el-color-success)',
    [SourceType.DATABASE]: 'var(--el-color-warning)',
    [SourceType.GRAPH]: 'var(--el-color-primary)'
  }
  return colorMap[type] || '#eee'
}
// 根据数据源类型获取默认图标
const getDefaultIcon = (item: DataSourceItem): string => {
  // 如果有自定义图标，优先使用自定义图标
  if (item.icon) return item.icon

  // 根据类型设置默认图标
  switch (item.type) {
    case SourceType.FILE:
      return 'Document'
    case SourceType.DATABASE:
      return 'DataLine'
    case SourceType.GRAPH:
      return 'Guide'
    default:
      return 'Document' // 默认使用Document图标
  }
}
// 编辑数据源
const handleEdit = (item: DataSourceItem) => {
  router.push({ path: `/data-source/${item.id}` })
}

// 删除数据源
const handleDelete = (row: DataSourceItem) => {
  MsgConfirm(
    // @ts-ignore
    `是否删除数据源：${row.name} ?`,
    '删除后无法恢复，请谨慎操作。',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      confirmButtonClass: 'danger'
    }
  ).then(() => {
    trainSourceApi.delTrainSource(row.id).then((res) => {
    console.log(res, 'res')
    if (res.code === 200) {
      const index = tableData.value.findIndex((v) => v.id === row.id)
      tableData.value.splice(index, 1)
      MsgSuccess('删除成功')
      // getList()
    }
  })
  })
  .catch(() => {})
}

const searchValue = ref('')
const paginationConfig = reactive({
  current_page: 1,
  page_size: 20,
  total: 0
})
const AddSourceDialogRef = ref()

function openCreateDialog() {
  AddSourceDialogRef.value?.open({
    type: '0', // 默认全部数据源
    pullType: '1' // 默认手动拉取
  })
}

// 处理数据源跳转
function handleJumpSourceData(item: DataSourceItem) {
  router.push({ path: `/data-source/${item.id}` })

  console.log('跳转到数据源:', item)
}

// 获取数据列表
const getList = () => {
  loading.value = true
  // 准备搜索参数
  const params = {
    name: searchValue.value || '',
    type: props.modelValue.type || '', // 优先使用选中的类型
    tags: _.map(props.modelValue.tags, 'key') 
  }
  
  // 清空当前数据，避免显示旧数据
  // tableData.value = []
  
  trainSourceApi
    .postTrainSourceList(paginationConfig, params, loading)
    .then((res) => {
      console.log('API返回数据:', res)
      
      if (res.code === 200 && res.data && res.data.records) {
        // 改进的标签提取函数
        const extractTagValues = (tagArray: any[] = []) => {
          if (!Array.isArray(tagArray)) return []
          
          return tagArray.map(tag => {
            // 处理对象形式的标签 {key: 'xxx', value: 'yyy'}
            if (tag && typeof tag === 'object') {
              return tag.value || tag.label || tag.name || tag
            }
            // 处理字符串形式的标签
            return tag
          }).filter(Boolean) // 过滤掉空值
        }
        
        // 处理返回的数据，合并tags和custom_tags
        const processedRecords = res.data.records.map((record: any) => {
          // 提取并合并标签
          const tagValues = extractTagValues(record.tags || [])
          const customTagValues = extractTagValues(record.custom_tags || [])
          
          // console.log(`处理记录 ${record.id}:`, {
          //   原始tags: record.tags,
          //   提取后tags: tagValues,
          //   原始custom_tags: record.custom_tags,
          //   提取后custom_tags: customTagValues
          // })
          
          return {
            ...record,
            allTags: [...tagValues, ...customTagValues]
          }
        })
        
        // 使用新数组替换tableData，确保视图更新
        if (paginationConfig.current_page === 1) {
          // 第一页或筛选时，替换数据
          tableData.value = processedRecords
        paginationConfig.total = res.data.total 
        } else {
          // 加载更多时，拼接数据
          tableData.value = [...tableData.value, ...processedRecords]
        }
        paginationConfig.total = res.data.total 
      } else {
        console.error('API返回数据格式不正确:', res)
        tableData.value = []
      }
      
      loading.value = false
    })
    .catch((error) => {
      console.error('获取数据列表失败:', error)
      tableData.value = []
      loading.value = false
    })
}
watch(
  () => props.modelValue,
  (newValue) => {
    console.log(
      '%c [ newValue ]-339',
      'font-size:13px; background:pink; color:#bf2c9f;',
      newValue
    )
 // 筛选时重置分页
    paginationConfig.current_page = 1
    getList()
  },
  // { immediate: true }
  { deep: true }
)
// 清空已选标签
const clearSelectedTags = () => {
   // 清空时重置分页
    paginationConfig.current_page = 1
  emit('update:modelValue', { type: '', tags: [] })
  getList()
}
// 移除单个标签
const removeTag = (index: number) => {
   // 移除时重置分页
    paginationConfig.current_page = 1
  const newTags = { ...props.modelValue }
  newTags.tags.splice(index, 1)
  emit('update:modelValue', newTags)
  getList()
}
function searchHandle() {
  paginationConfig.current_page = 1

  getList()
}
// 暴露方法供父组件调用
defineExpose({
  getList
})

// 获取类型标签的显示文本
const getTypeLabel = (type: string) => {
  // 查找对应的数据源类型标签
  const typeTag = tagsList.find((g) => g.parentKey === '100')?.childs.find((t) => t.key === type)

  return typeTag ? typeTag.value : type
}

// 清除类型标签
const clearType = () => {
   // 清除时重置分页
    paginationConfig.current_page = 1
  const newTags = { ...props.modelValue, type: '' }
  emit('update:modelValue', newTags)
  getList()
}
onMounted(() => {
  getList()
})
</script>

<style lang="scss" scoped>
.application-list-container {
  .container-title {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .container-search-result {
    display: flex;
    align-items: center;
    gap: 8px;
    .primary-color {
      color: var(--el-color-primary);
    }
    .tags-container {
      display: flex; // 添加 flex 布局
      flex-wrap: wrap; // 允许标签换行
      gap: 8px; // 设置标签之间的间距
    }
  }
}
.application-card {
  .status-tag {
    position: absolute;
    right: 16px;
    top: 20px;
  }
}
.dropdown-custom-switch {
  padding: 5px 11px;
  font-size: 14px;
  font-weight: 400;
  span {
    margin-right: 26px;
  }
}
.footer {
  text-align: center;
  padding: 10px 0;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  color: #909399;
  background-color: var(--app-layout-bg-color);
}
.boxShadow:hover {
  background: linear-gradient(
      179deg,
      rgba(64, 158, 255, 0.22) -8.26%,
      hsla(0deg, 0%, 100%, 0) 44.84%
    ),
    #fff;
  box-shadow: 0px 12px 30px rgba(122, 161, 225, 0.2);
}
</style>
