<template>
  <div class="sidebar-container">
    <div class="sidebar p-8">
      <el-scrollbar wrap-class="scrollbar-wrapper">
        <el-menu :default-active="activeMenu" class="el-menu-vertical">
          <el-menu-item
            v-for="item in menuList"
            :key="item.path"
            :index="item.path"
            @click="handleSelect(item)"
            popper-class="sidebar-popper"
            :disabled="item.disabled"
            :class="item.disabled ? 'is-disabled' : ''"
          >
            <el-icon class="sidebar-icon">
              <component :is="item.icon" />
            </el-icon>
            <template #title>{{ item.title }}</template>
          </el-menu-item>
          <!-- <el-menu-item index="all">全部数据源</el-menu-item>
          <el-menu-item index="document">文件型数据源</el-menu-item>
          <el-menu-item index="database">数据型数据源</el-menu-item>
          <el-menu-item index="graph">知识图谱数据源</el-menu-item> -->
        </el-menu>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Folder, Document, DataLine, Share } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'

const route = useRoute()
// 菜单配置
const menuList = [
  {
    title: '全部数据源',
    path: 'all',
    icon: 'Folder'
  },
  {
    title: '文件型数据源',
    path: 'document',
    icon: 'Document'
  },
  {
    title: '数据型数据源',
    path: 'database',
    icon: 'DataLine'
  },
  {
    title: '知识图谱数据源',
    path: 'graph',
    icon: 'Share',
    disabled: true
  }
]

const activeMenu = computed(() => route.query.type?.toString() || '/all')

const emit = defineEmits(['select'])

const handleSelect = (item: any) => {
  emit('select', { path: item.path })
}
</script>

<style lang="scss" scoped>
.sidebar-container {
  box-sizing: border-box;
  transition: width 0.28s;
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background-color: var(--sidebar-bg-color);
  height: 100%;
  .sidebar {
    .el-menu {
      height: 100%;
      border: none;
    }
  }
  .el-menu-vertical {
    border-right: none;

    .el-menu-item {
      display: flex;
      align-items: center;
      text-align: center;
      vertical-align: middle;
      padding: 13px 12px 13px 16px !important;
      font-weight: 500;
      border-radius: 4px;
      &:hover {
        background: none;
        color: var(--el-menu-active-color);
      }
      &.is-active {
        color: var(--el-menu-active-color);
        background: var(--el-color-primary-light-9);
      }
      // 禁用状态样式
      &.is-disabled {
        background-color: transparent !important;
        color: var(--el-text-color-disabled) !important;
        cursor: not-allowed !important;

        // &:hover {
        //   background-color: transparent !important;
        //   color: var(--el-text-color-disabled) !important;
        // }
      }

      .el-icon {
        margin-right: 5px;
        font-size: 20px;
        margin-top: -2px;
      }
    }
  }
}

:deep(.scrollbar-wrapper) {
  overflow-x: hidden !important;
}
</style>
