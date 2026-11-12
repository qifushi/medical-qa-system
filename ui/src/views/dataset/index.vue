<template>
  <div class="dataset-list-container p-24" style="padding-top: 16px">
    <div class="flex-between mb-16">
      <h4>{{ datasetTitle }}</h4>
      <el-input
        v-model="getListParams.searchValue"
        @change="searchHandle"
        placeholder="按名称搜索"
        prefix-icon="Search"
        class="w-240"
        clearable
      />
    </div>
    <div v-loading.fullscreen.lock="paginationConfig.current_page === 1 && loading">
      <InfiniteScroll
        :size="datasetList.length"
        :total="paginationConfig.total"
        :page_size="paginationConfig.page_size"
        v-model:current_page="paginationConfig.current_page"
        @load="getList"
        :loading="loading"
      >
        <el-row :gutter="15">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-16">
            <CardAdd title="创建知识库" @click="router.push({ path: '/dataset/create' })" />
          </el-col>
          <template v-for="(item, index) in datasetList" :key="index">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-16">
              <CardBox
                :title="item.name"
                :description="item.desc"
                class="cursor"
                @click="router.push({ path: `/dataset/${item.id}/document` })"
              >
                <template #icon>
                  <AppAvatar
                    v-if="item.type === '1'"
                    class="mr-8 avatar-purple"
                    shape="square"
                    :size="32"
                  >
                    <img src="@/assets/icon_web.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                  <AppAvatar v-else class="mr-8" shape="square" :size="32">
                    <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                </template>
                <div class="delete-button">
                  <el-tag v-if="item.type === '0'">通用型</el-tag>
                  <el-tag class="purple-tag" v-else-if="item.type === '1'" type="warning"
                    >Web 站点</el-tag
                  >
                </div>

                <template #footer>
                  <div class="footer-content flex-between">
                    <div>
                      <span class="bold">{{ item?.document_count || 0 }}</span>
                      文档<el-divider direction="vertical" />
                      <span class="bold">{{ numberFormat(item?.char_length) || 0 }}</span>
                      字符<el-divider direction="vertical" />
                      <span class="bold">{{ item?.application_mapping_count || 0 }}</span>
                      关联应用
                    </div>
                    <div @click.stop>
                      <el-dropdown trigger="click">
                        <el-button text @click.stop>
                          <el-icon><MoreFilled /></el-icon>
                        </el-button>
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item
                              icon="Refresh"
                              @click.stop="syncDataset(item)"
                              v-if="item.type === '1'"
                              >同步</el-dropdown-item
                            >
                            <el-dropdown-item @click="reEmbeddingDataset(item)">
                              <AppIcon
                                iconName="app-document-refresh"
                                style="font-size: 16px"
                              ></AppIcon>
                              重新向量化</el-dropdown-item
                            >
                            <el-dropdown-item
                              icon="Setting"
                              @click.stop="router.push({ path: `/dataset/${item.id}/setting` })"
                            >
                              设置</el-dropdown-item
                            >
                            <el-dropdown-item @click.stop="export_dataset(item)">
                              <AppIcon iconName="app-export"></AppIcon>导出</el-dropdown-item
                            >
                            <el-dropdown-item icon="Delete" @click.stop="deleteDataset(item)"
                              >删除</el-dropdown-item
                            >
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </div>
                  </div>
                </template>
              </CardBox>
            </el-col>
          </template>
        </el-row>
      </InfiniteScroll>
    </div>
    <SyncWebDialog ref="SyncWebDialogRef" @refresh="refresh" />
        <!-- 页脚 -->
        <div v-if="logoAndCopyright.isShowLogoAndCopyright" class="footer">
      <p>Copyright © 2023-2025 杰软科技（集团）有限公司</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import datasetApi from '@/api/dataset'
import useStore from '@/stores'
import { MsgConfirm, MsgSuccess } from '@/utils/message'
import { numberFormat } from '@/utils/utils'
import SyncWebDialog from '@/views/dataset/component/SyncWebDialog.vue'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const { logoAndCopyright } = useStore()

const SyncWebDialogRef = ref()
const loading = ref(false)
const datasetList = ref<any[]>([])
const paginationConfig = reactive({
  current_page: 1,
  page_size: 20,
  total: 0
})
const getListParams= ref({
  searchValue: '',
  category: ''
})

// const searchValue = ref('')
const categoryMap = {
  '': '全部知识',
  '1': '科研知识',
  '2': '财务知识',
  '3': '人事知识'
} as { [key: string]: string };
const datasetTitle = computed(() => {
      return categoryMap[getListParams.value.category] || '知识库'
})
function refresh() {
  MsgSuccess('同步任务发送成功')
}

function reEmbeddingDataset(row: any) {
  datasetApi.putReEmbeddingDataset(row.id).then(() => {
    MsgSuccess('提交成功')
  })
}

function syncDataset(row: any) {
  SyncWebDialogRef.value.open(row.id)
}

function searchHandle() {
  paginationConfig.current_page = 1
  datasetList.value = []
  getList()
}
const export_dataset = (item: any) => {
  datasetApi.exportDataset(item.name, item.id, loading).then((ok) => {
    MsgSuccess('导出成功')
  })
}

function deleteDataset(row: any) {
  MsgConfirm(
    `是否删除知识库：${row.name} ?`,
    `此知识库关联 ${row.application_mapping_count} 个应用，删除后无法恢复，请谨慎操作。`,
    {
      confirmButtonText: '删除',
      confirmButtonClass: 'danger'
    }
  )
    .then(() => {
      datasetApi.delDataset(row.id, loading).then(() => {
        const index = datasetList.value.findIndex((v) => v.id === row.id)
        datasetList.value.splice(index, 1)
        MsgSuccess('删除成功')
      })
    })
    .catch(() => {})
}

function getList() {
  datasetApi
    .getDataset(paginationConfig, { name: getListParams.value.searchValue, category:getListParams.value.category}, loading)
    .then((res) => {
      paginationConfig.total = res.data.total
      datasetList.value = [...datasetList.value, ...res.data.records]
    })
  // datasetApi
  //   .getDataset(paginationConfig, searchValue.value && { name: searchValue.value }, loading)
  //   .then((res) => {
  //     paginationConfig.total = res.data.total
  //     datasetList.value = [...datasetList.value, ...res.data.records]
  //   })
}

onMounted(() => {
  const routeCategoryMap:{ [key: string]: string } = {
    'allDataset':'',
    'scientific': '1',
    'finance': '2',
    'personnel': '3'
  }
  const currentRoute = router.currentRoute.value.name as string
  if (currentRoute && routeCategoryMap[currentRoute]) {
  getListParams.value.category = routeCategoryMap[currentRoute];
  } else {
    getListParams.value.category = ''; // 当路由名称不在映射中时显示全部
}
  
  getList()

})
</script>
<style lang="scss" scoped>
.dataset-list-container {
  .delete-button {
    position: absolute;
    right: 12px;
    top: 18px;
    height: auto;
  }
  .footer-content {
    .bold {
      color: var(--app-text-color);
    }
  }
  :deep(.el-divider__text) {
    background: var(--app-layout-bg-color);
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
</style>
