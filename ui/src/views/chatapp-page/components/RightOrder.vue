<template>
  <div class="right-order-container" v-loading="loading">
    <div class="primary p-16" style="font-size: 20px">常用指令</div>
    <div class="pb-0 mb-16 add-order">
      <!-- 过渡包裹 -->
      <transition name="slide">
        <!-- 常规模式 -->
        <div v-if="!isSearchMode" class="normal-mode">
          <el-button class="add-button w-full" color="#eeeaea" dark round @click="newOrder">
            <el-icon class="order-icon-color">
              <CirclePlus />
            </el-icon>
            <span class="ml-4 add-text">新建指令</span>
          </el-button>
          <el-button round color="#eeeaea" dark @click="toggleSearchMode">
            <el-icon class="order-icon-color">
              <Search />
            </el-icon>
          </el-button>
        </div>
      </transition>

      <transition name="slide">
        <!-- 搜索模式 -->
        <div v-if="isSearchMode" class="search-mode">
          <el-input
            ref="searchInputRef"
            v-model="searchKeyword"
            placeholder="搜索指令"
            class="search-input"
            @input="filterOrders"
            @blur="handleSearchBlur"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </transition>
    </div>
    <div class="order-tabs">
      <el-button
        plain
        v-for="(item, index) in orderTabs"
        :key="index"
        :type="activeTab === item ? 'primary' : ''"
        @click="handleTabClick(item)"
      >
        {{ item }}
      </el-button>
      <div class="order-list">
        <el-scrollbar>
          <div
            class="order-item mt-16 p-16"
            v-for="(item, index) of orderList"
            @click="clickOrder(item)"
            @mouseenter="mouseenter(item)"
            @mouseleave="mouseId = ''"
          >
            <div style="font-size: 16px; color: #7b7c7e">
              <!-- {{ item.name }} -->
              <div class="flex-between">
                <auto-tooltip :content="item.name">
                  <!-- <el-tag>财务</el-tag> -->
                  {{ item.name }}
                </auto-tooltip>
                <div @click.stop class="flex-center orderBtn" v-if="mouseId === item.id">
                  <el-button style="padding: 0" link @click.stop="deleteOrder(item)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>

            <div class="order-item-content">{{ item.content }}</div>
          </div>
        </el-scrollbar>
      </div>
    </div>
    <NewOrderDialog ref="NewOrderDialogRef" @refresh="refresh"></NewOrderDialog>
  </div>
</template>

<script setup lang="ts">
import customApi from '@/api/custom'
import type { CustomFormType } from '@/api/type/custom'
import { MsgSuccess } from '@/utils/message'
import { nextTick, onMounted, ref } from 'vue'
import NewOrderDialog from './newOrderDialog.vue'

const emit = defineEmits(['clickOrder'])
const loading = ref(false)
const orderTabs = ['全部', '财务', '合同', '项目']

const orderList = ref<any[]>([])
function clickOrder(item: CustomFormType) {
  emit('clickOrder', item)
}
const mouseId = ref('')
function mouseenter(row: any) {
  mouseId.value = row.id
}
function deleteOrder(row: any) {
  customApi.delCustom(row.id, loading).then((res) => {
    console.log(res, 'res11')
    MsgSuccess('新增成功')
    getOrderList()
  })
}
function getOrderList() {
  customApi.getAllCustom(loading).then((res) => {
    console.log(res, 'res11')
    // orderList.value = res.data
    originalOrderList.value = res.data
    filterOrders() // 获取数据后进行过滤
  })
}
const NewOrderDialogRef = ref()
function newOrder() {
  NewOrderDialogRef.value.open()
}
function refresh() {
  getOrderList()
}
// 分类和模糊查询
// 当前选中的分类tab
const activeTab = ref('全部')
// 搜索关键词
const searchKeyword = ref('')
const isSearchMode = ref(false)
// 原始数据列表
const originalOrderList = ref<any[]>([])
const searchInputRef = ref()
const toggleSearchMode = () => {
  isSearchMode.value = !isSearchMode.value
  if (!isSearchMode.value) {
    searchKeyword.value = '' // 退出搜索模式时清空搜索词
    filterOrders() // 重置列表
  } else {
    // 使用nextTick确保DOM更新后再聚焦
    nextTick(() => {
      searchInputRef.value.focus()
    })
  }
}
const handleSearchBlur = () => {
  // 添加短暂延时，确保点击事件能够正确触发
  setTimeout(() => {
    isSearchMode.value = false
    searchKeyword.value = ''
    filterOrders()
  }, 200)
}
const filterOrders = () => {
  let filteredList = [...originalOrderList.value]
  console.log(filteredList, 'filteredList')
  // 只按关键词搜索，不考虑当前选中的tab
  if (searchKeyword.value) {
    filteredList = originalOrderList.value.filter((item) =>
      item.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  // 如果不是搜索模式，才按分类过滤
  if (!isSearchMode.value && activeTab.value !== '全部') {
    filteredList = filteredList.filter((item) => {
      // const type = JSON.parse(item.type)
      switch (activeTab.value) {
        case '财务':
          return item.type === 'finance'
        case '合同':
          return item.type === 'contract'
        case '项目':
          return item.type === 'project'
        default:
          return true
      }
    })
  }

  console.log(filteredList, 'filteredList1')

  orderList.value = filteredList
}
const handleTabClick = (item: string) => {
  activeTab.value = item
  console.log(activeTab.value, 'activeTab.value')
  filterOrders()
}
onMounted(() => {
  getOrderList()
})
</script>

<style scoped lang="scss">
.right-order-container {
  width: 300px;
  height: calc(100% - 20px); // 减去父元素底部padding
  background-color: #fff;
  border-radius: 18px;
  padding: 4px 10px;
  margin-right: 10px;
  box-sizing: border-box;
  .add-order {
    user-select: none;
    display: flex;
    :deep(.el-button + .el-button) {
      margin-left: 6px;
    }
    .add-text {
      color: #5b5c5d;
    }
    .order-icon-color {
      color: #5b5c5d;
    }
  }
  .order-tabs {
    // display: flex;
    .order-list {
      // max-height: 100%;
      height: calc(100vh - 180px);

      .el-scrollbar {
        // 隐藏滚动条
        :deep(.el-scrollbar__bar) {
          display: none !important;
        }
      }

      .order-item {
        box-sizing: border-box;
        border: 1px solid transparent;
        background-color: #f0f7fd;
        border-radius: 10px;
        cursor: pointer;
        user-select: none;
        .orderBtn {
          width: 20px;
          height: 20px;
          background-color: #fff;
          border-radius: 20px;
          border: 1px solid transparent;
          &:hover {
            background-color: #edf3fa;
            border: 1px solid #409eff;
          }
        }
        .order-item-content {
          color: #aeb0b1;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 4;
          -webkit-box-orient: vertical;
          word-break: break-all;
        }
      }
    }
    .order-list .order-item:hover {
      border: 1px solid #409eff;
      background-color: #edf3fa;
    }
  }
  .add-order {
    overflow: hidden;
    .search-input {
      width: 100%;

      :deep(.el-input__wrapper) {
        border-radius: 20px;
        background-color: #eeeaea;
      }
    }

    .normal-mode,
    .search-mode {
      display: flex;
      gap: 6px;
      width: 100%;
    }
    .slide-enter-active,
    .slide-leave-active {
      transition: width 0.3s;
      overflow: hidden;
    }

    .slide-enter-from,
    .slide-leave-to {
      width: 0;
    }

    .slide-enter-to,
    .slide-leave-from {
      width: 100%;
    }
  }
}
</style>
