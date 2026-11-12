<template>
  <div class="breadcrumb-container">
    <div class="breadcrumb" v-if="items.length > 0">
      <template v-for="(item, index) in items" :key="index">
        <div class="breadcrumb-item" :class="{ active: index === items.length - 1 }">
          <router-link
            v-if="index < items.length - 1 && item.path"
            :to="item.path"
            :class="['breadcrumb-link', item.path ? 'hover' : '']"
          >
            <span class="icon-wrapper" v-if="item.icon">
              <component :is="item.icon" class="breadcrumb-icon" />
            </span>
            <span>{{ item.title }}</span>
          </router-link>
          <span v-else class="breadcrumb-current">
            <span class="icon-wrapper" v-if="item.icon">
              <component :is="item.icon" class="breadcrumb-icon" />
            </span>
            <span>{{ item.title }}</span>
          </span>
        </div>
        <div v-if="index < items.length - 1" class="breadcrumb-separator">
          <component :is="separatorIcon" v-if="separatorIcon" />
          <span v-else>{{ separator }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, withDefaults } from 'vue'
import { ArrowRight, CaretRight } from '@element-plus/icons-vue'

interface BreadcrumbItem {
  title: string
  path: string
  icon?: any
}

interface Props {
  items: BreadcrumbItem[]
  separator?: string
  separatorIcon?: any
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  separator: '/',
  theme: 'light',
  separatorIcon: CaretRight
})
</script>

<style lang="scss" scoped>
.breadcrumb-container {
  padding: 16px 0;
  margin-bottom: 16px;
  border-bottom: 1px solid #eee;
  box-sizing: border-box;
  max-width: 1200px;
  margin: 0 auto;
}

.breadcrumb {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  font-size: 14px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  transition: all 0.3s ease;

  &.active {
    .breadcrumb-current {
      color: #409eff;
      font-weight: 500;

      .icon-wrapper {
        background: rgba(64, 158, 255, 0.1);
      }
    }
  }
}

.breadcrumb-link {
  display: flex;
  align-items: center;
  color: #606266;
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s ease;
  cursor: default;
  &.hover:hover {
    cursor: pointer;
    color: #409eff;
    background: rgba(64, 158, 255, 0.1);

    .icon-wrapper {
      background: rgba(64, 158, 255, 0.2);
    }
  }
}

.breadcrumb-current {
  display: flex;
  align-items: center;
  color: #909399;
  padding: 4px 8px;
  border-radius: 4px;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f5f7fa;
  margin-right: 8px;
  transition: all 0.3s ease;
}

.breadcrumb-icon {
  font-size: 14px;
  color: #606266;
}

.breadcrumb-separator {
  margin: 0 8px;
  color: #c0c4cc;
  display: flex;
  align-items: center;

  svg {
    width: 14px;
    height: 14px;
  }
}

// 主题样式
.breadcrumb-container.light {
  background: #fff;
  border-bottom-color: #ebeef5;
}

.breadcrumb-container.dark {
  background: #1f2d3d;
  border-bottom-color: #2d3a4b;

  .breadcrumb-link {
    color: #c0c4cc;

    &.hover:hover {
      color: #fff;
      background: rgba(64, 158, 255, 0.2);
    }
  }

  .breadcrumb-current {
    color: #fff;
  }

  .icon-wrapper {
    background: rgba(255, 255, 255, 0.1);
  }

  .breadcrumb-icon {
    color: #c0c4cc;
  }

  .breadcrumb-separator {
    color: #5a6c8c;
  }
}
</style>
