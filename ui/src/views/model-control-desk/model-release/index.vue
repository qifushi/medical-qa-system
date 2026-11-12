<template>
  <div style="height: calc(100vh - 56px)">
    <div class="application-list-container p-24" style="padding-top: 16px">
      <div class="container-title mb-16">
        <h4>模型发布</h4>
        <el-input
          v-model="searchValue"
          @change="searchHandle"
          placeholder="按名称搜索"
          prefix-icon="Search"
          class="w-240"
          clearable
        />
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
            <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-16">
              <CardAdd title="新增模型发布" @click="openCreateDialog" style="min-height: 195.5px" />
            </el-col>
            <el-col
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
              :xl="4"
              v-for="(item, index) in tableData"
              :key="index"
              class="mb-16"
            >
              <CardBox
                :title="item.model_name"
                :description="item.model_desc"
                class="application-card cursor boxShadow"
              >
                <template #icon>
                  <AppIcon iconName="app-smartModel-icon" class="card-icon"></AppIcon>
                </template>
                <div class="status-tag">
                  <el-tag
                    :type="getStatusTagType(item)"
                    effect="plain"
                    style="border-radius: 4px"
                    >{{ getStatusText(item) }}</el-tag
                  >
                </div>
                <div v-if="!item.model_desc" class="no-description mt-12">暂无描述</div>
                <div class="card-content">
                  <div class="api-info-item">
                    <span class="label">发布地址：</span>
                    <span class="value">{{ item.publish_ip }}:{{ item.publish_port }}/v1</span>
                    <el-tooltip effect="dark" content="复制" placement="top">
                      <el-button
                        type="info"
                        link
                        size="small"
                        @click.stop="copyClick(`${item.publish_ip}:${item.publish_port}/v1`)"
                        icon="CopyDocument"
                      >
                      </el-button>
                    </el-tooltip>
                  </div>
                  <div class="api-info-item">
                    <span class="label">API KEY：</span>
                    <span class="value">{{ formatApiKey(item.api_key) }}</span>
                    <el-tooltip effect="dark" content="复制" placement="top">
                      <el-button
                        type="info"
                        link
                        size="small"
                        @click.stop="copyClick(item.api_key)"
                        icon="CopyDocument"
                      >
                      </el-button>
                    </el-tooltip>
                  </div>
                  <div class="api-info-item">
                    <span class="label">模型名称：</span>
                    <span class="value">{{ item.model_code }}</span>
                    <el-tooltip effect="dark" content="复制" placement="top">
                      <el-button
                        type="info"
                        link
                        size="small"
                        @click.stop="copyClick(item.model_code)"
                        icon="CopyDocument"
                      >
                      </el-button>
                    </el-tooltip>
                  </div>
                </div>
                <template #footer>
                  <div class="footer-content">
                    <el-tooltip effect="dark" content="编辑" placement="top">
                      <el-button
                        :disabled="item.publish_status === PublishStatus.Published"
                        text
                        @click.stop="openCreateDialog(item)"
                      >
                        <AppIcon iconName="Setting"></AppIcon>
                      </el-button>
                    </el-tooltip>
                    <el-divider direction="vertical" />
                    <el-tooltip
                      effect="dark"
                      :content="
                        item.publish_status === PublishStatus.Published ? '取消发布' : '发布'
                      "
                      placement="top"
                    >
                      <el-button text @click.stop="handleRelease(item)">
                        <AppIcon
                          :style="{
                            color:
                              item.publish_status === PublishStatus.Published
                                ? 'var(--el-color-danger)'
                                : ''
                          }"
                          :iconName="
                            item.publish_status === PublishStatus.Published
                              ? 'app-smartModel-cancelRelease'
                              : 'app-smartModel-release'
                          "
                        ></AppIcon>
                      </el-button>
                    </el-tooltip>
                    <el-divider direction="vertical" />

                    <el-tooltip effect="dark" content="监控" placement="top">
                      <el-button text disabled>
                        <AppIcon iconName="Monitor"></AppIcon>
                      </el-button>
                    </el-tooltip>
                    <el-divider direction="vertical" />
                    <el-tooltip effect="dark" content="发布至应用平台" placement="top">
                      <el-button
                        text
                        :disabled="!isPublishToAppEnabled(item)"
                        :loading="getPublishToAppLoading(item.id as string)"
                        @click.stop="publishToApplicationPlatform(item)"
                      >
                        <AppIcon
                          iconName="Connection"
                          :style="{
                            color: isPublishToAppEnabled(item) ? 'var(--el-color-primary)' : ''
                          }"
                        ></AppIcon>
                      </el-button>
                    </el-tooltip>
                    <el-divider direction="vertical" />
                    <el-tooltip effect="dark" content="删除" placement="top">
                      <el-button
                        :disabled="item.publish_status === PublishStatus.Published"
                        text
                        @click.stop="handleDelete(item)"
                      >
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </el-tooltip>
                  </div>
                </template>
              </CardBox>
            </el-col>
          </el-row>
        </InfiniteScroll>
      </div>
      <AddReleaseDialog ref="AddReleaseDialogRef" @refresh="refreshList"></AddReleaseDialog>
      <!-- <CreateApplicationDialog ref="CreateApplicationDialogRef" /> -->
      <!-- 页脚 -->
      <!-- <div v-if="logoAndCopyright.isShowLogoAndCopyright" class="footer">
      <p>Copyright © 2023-2025 杰软科技（集团）有限公司</p>
    </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AddReleaseDialog from './components/addReleaseDialog.vue'
import modelReleaseApi from '@/api/train-release'
import ModelApi from '@/api/model'
import { type ModelReleaseType } from '@/api/type/model-release'
import { MsgSuccess, MsgConfirm } from '@/utils/message'
import { copyClick } from '@/utils/clipboard'

enum PublishStatus {
  Unpublished = 0,
  Published = 1
}
const loading = ref(false)
const tableData = ref<ModelReleaseType[]>([])

const searchValue = ref('')
const paginationConfig = reactive({
  current_page: 1,
  page_size: 20,
  total: 0
})
// 发布时间跟踪Map
const modelPublishTimeMap = ref<Map<string, number>>(new Map())
// 3分钟的毫秒数
const DEPLOY_MONITOR_DURATION = 3 * 60 * 1000

// 获取数据列表
const getList = async () => {
  loading.value = true
  const params = {
    kw: searchValue.value || ''
  }
  try {
    const res = await modelReleaseApi.postModelReleaseList(paginationConfig, params)
    paginationConfig.total = res.data.total
    if (paginationConfig.current_page === 1) {
      // 第一页时替换数据
      tableData.value = res.data.records
    } else {
      tableData.value = [...tableData.value, ...res.data.records]
    }
  } catch (error) {
    console.error('获取模型发布列表失败:', error)
  } finally {
    loading.value = false
  }
}

function searchHandle() {
  paginationConfig.total = 0
  paginationConfig.current_page = 1
  tableData.value = []
  getList()
}
const formatApiKey = (apiKey: string) => {
  if (!apiKey || apiKey.length < 12) {
    return '**********'
  }
  const preStr = apiKey.substring(0, 8)
  const endStr = apiKey.substring(apiKey.length - 4)
  const middleStars = '*'.repeat(10)

  return preStr + middleStars + endStr
}

const refreshList = () => {
  paginationConfig.current_page = 1
  tableData.value = []
  getList()
}
// ==== 按钮操作 ====
const handleDelete = async (item: any) => {
  try {
    await MsgConfirm(`是否删除模型：${item.model_name} ?`, '删除后无法恢复，请谨慎操作。', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      confirmButtonClass: 'danger'
    })

    const res = await modelReleaseApi.delModelRelease(item.id)
    console.log(res, 'res')

    if (res.code === 200) {
      const index = tableData.value.findIndex((v) => v.id === item.id)
      tableData.value.splice(index, 1)
      MsgSuccess('删除成功')
      getList()
    }
  } catch (error) {
    // 用户取消删除或删除失败
    console.log('删除操作取消或失败:', error)
  }
}
// 发布操作
const handleRelease = (item: any) => {
  const isPublished = item.publish_status === PublishStatus.Published
  const actionText = isPublished ? '取消' : '发布'
  const suffixText = isPublished ? ' 模型发布吗？' : ' 模型吗？'

  const message = h('p', null, [
    h('span', null, `确认${actionText} `),
    h(
      'span',
      {
        style: {
          color: 'var(--el-color-warning)'
        }
      },
      item.model_name
    ),
    h('span', null, suffixText)
  ])

  ElMessageBox.confirm(message, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      loading.value = true
      const params = {
        publish_id: item.id,
        status: item.publish_status === 1 ? 'down' : 'up', // 需要发布传'up',需要取消发布传‘down’
        infer_framework: item.infer_framework
      }
      // 调用 发布/取消发布 接口
      modelReleaseApi
        .putModelReleaseStatus(params)
        .then(() => {
          getList()

          const isPublishAction = item.publish_status === PublishStatus.Unpublished
          // 如果是发布操作，记录发布时间
          if (isPublishAction) {
            modelPublishTimeMap.value.set(item.id, Date.now())
          } else {
            // 如果是取消发布，清理发布时间记录
            modelPublishTimeMap.value.delete(item.id)
          }
            console.log('%c [ item ]-317', 'font-size:13px; background:pink; color:#bf2c9f;', item)
          
          ElMessage.success(isPublishAction ? '发布成功' : '取消发布成功')
        })
        .catch((error) => {
          console.error('操作失败:', error)
          ElMessage.error(
            item.publish_status === PublishStatus.Published
              ? '取消发布失败，请稍后重试'
              : '发布失败，请稍后重试'
          )
        })
        .finally(() => {
          loading.value = false
        })
    })
    .catch(() => {
      // ElMessage.info('操作已取消')
    })
}
// 判断模型是否在部署监控期内
const isInDeployMonitorPeriod = (modelId: string) => {
  const publishTime = modelPublishTimeMap.value.get(modelId)
  if (!publishTime) return false

  const currentTime = Date.now()
  return currentTime - publishTime < DEPLOY_MONITOR_DURATION
}
// 发布至应用平台的方法
const publishToApplicationPlatform = async (item: any) => {
  console.log('%c [ item ]-343', 'font-size:13px; background:pink; color:#bf2c9f;', item)
  setPublishToAppLoading(item.id, true)
  try {
    // 这里调用发布至应用平台的API接口
    const params = {
      name: item.model_name, // 模型名称
      model_name: item.model_code, // 模型编码
      model_type: 'LLM',
      provider: 'model_vllm_provider',
      credential: {
        api_base: `${item.publish_ip}:${item.publish_port}`,
        api_key: item.api_key
      }
    }
    const res = await ModelApi.createModel(params)
    if (res.code === 200) {
      ElMessage.success('发布至应用平台成功')
    }
  } catch (error) {
    console.error('发布至应用平台失败:', error)
  } finally {
    setPublishToAppLoading(item.id, false)
  }
}

const AddReleaseDialogRef = ref()
const openCreateDialog = (data: any) => {
  AddReleaseDialogRef.value?.open(data)
}

// 获取状态标签类型
const getStatusTagType = (item: any) => {
  if (item.publish_status === PublishStatus.Published) {
  // 如果在部署监控期内且健康检查失败，显示警告色
    if (isInDeployMonitorPeriod(item.id) && item.health_status === 'interrupted') {
      return 'warning'
    }
    return item.health_status === 'interrupted' ? 'danger' : 'success'
  }
  return 'info'
}

// 获取状态文本
const getStatusText = (item: any) => {
  if (item.publish_status === PublishStatus.Published) {
    // 如果在部署监控期内且健康检查失败，显示"状态异常"
    if (isInDeployMonitorPeriod(item.id) && item.health_status === 'interrupted') {
      return '服务受限'
    }
    return item.health_status === 'interrupted' ? '已中断' : '已发布'
  }
  return '未发布'
}
let healthCheckTimer: NodeJS.Timeout | null = null
// 检查模型健康状态
const checkModelHealth = async (model: any) => {
  try {
    const res = await modelReleaseApi.getModelHealth(model.publish_ip, model.publish_port)

    // 根据健康检查结果更新模型状态
    const modelIndex = tableData.value.findIndex((item) => item.id === model.id)
    if (modelIndex !== -1) {
      // 假设接口返回的健康状态字段为 healthy 或 status
      const isHealthy = res?.data?.status === 200 && res.code === 200
        const newHealthStatus = isHealthy ? 'healthy' : 'interrupted'

      tableData.value[modelIndex] = {
        ...tableData.value[modelIndex],
        health_status: newHealthStatus
      }
        // 如果在监控期内健康检查成功（可以提前结束监控）
      if (isHealthy && isInDeployMonitorPeriod(model.id)) {
        console.log(`模型 ${model.model_name} 部署成功，健康检查通过`)
      }
    }
  } catch (error) {
    console.error('健康检查失败:', error)
    // 如果接口调用失败，标记为中断状态
    const modelIndex = tableData.value.findIndex((item) => item.id === model.id)
    if (modelIndex !== -1) {
      tableData.value[modelIndex] = {
        ...tableData.value[modelIndex],
        health_status: 'interrupted'
      }
    }
  }
}
// 批量检查所有已发布模型的健康状态
const checkAllPublishedModelsHealth = () => {
  const publishedModels = tableData.value.filter((model) => model.publish_status === 1)
  publishedModels.forEach((model) => {
    checkModelHealth(model)
  })
}
// 启动定时健康检查
const startHealthCheck = () => {
  // 立即执行一次检查
  setTimeout(() => {
    checkAllPublishedModelsHealth()
  }, 1000)

  // 设置每半分钟检查一次
  healthCheckTimer = setInterval(() => {
    checkAllPublishedModelsHealth()
  }, 30000)
}
const isPublishToAppEnabled = (item: any) => {
  const isHealthy =
    item.publish_status === PublishStatus.Published && item.health_status === 'healthy'
  const isNotLoading = !getPublishToAppLoading(item.id)

  return isHealthy && isNotLoading
}
onMounted(() => {
  getList()
  startHealthCheck()
})
onBeforeUnmount(() => {
  // 清理定时器
  if (healthCheckTimer) {
    clearInterval(healthCheckTimer)
    healthCheckTimer = null
  }
})
// 添加发布至应用平台的loading状态管理
const publishToAppLoadingMap = ref<Map<string, boolean>>(new Map())

// 获取特定模型的loading状态
const getPublishToAppLoading = (itemId: string) => {
  return publishToAppLoadingMap.value.get(itemId) || false
}

// 设置特定模型的loading状态
const setPublishToAppLoading = (itemId: string, loading: boolean) => {
  publishToAppLoadingMap.value.set(itemId, loading)
}
// 暴露方法供父组件调用
defineExpose({
  getList
})
</script>

<style lang="scss" scoped>
.container-title {
  display: flex;
  align-items: center;
  gap: 16px;
}
.application-card {
  .card-content {
    margin-top: 8px;
    margin-bottom: 30px;
  }

  .api-info-item {
    display: flex;
    align-items: center;
    gap: 4px;
    // margin-bottom: 6px;
    font-size: 12px;
    color: var(--app-text-color-secondary);

    .label {
      flex-shrink: 0;
      font-weight: 500;
    }

    .value {
      // flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      min-width: 0;
    }

    .el-button {
      flex-shrink: 0;
      font-size: 12px;
      padding: 0 4px;
    }
  }
  .card-icon {
    font-size: 14px;
    color: #5e6772;
    border: 1px solid #dfe2e5;
    border-radius: 4px;
    padding: 4px;
    margin-right: 8px;
  }
  .status-tag {
    position: absolute;
    right: 16px;
    // top: 20px;
    top: 16px;
  }
  .api-key-container {
    display: flex;
    align-items: center;
    gap: 8px; /* 调整文本和按钮之间的间距 */
    color: var(--app-text-color-secondary);
    font-size: 14px;
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
.no-description {
  height: var(--app-card-box-description-height, 40px);
  color: var(--app-text-color-secondary);
  line-height: 22px;
  font-weight: 400;
}
</style>
