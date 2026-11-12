<template>
  <el-card shadow="hover" class="card-box" @mouseenter="cardEnter()" @mouseleave="cardLeave()">
    <div class="card-header">
      <slot name="header">
        <div class="title flex align-center">
          <slot name="icon">
            <AppAvatar v-if="showIcon" class="mr-12" shape="square" :size="32">
              <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
            </AppAvatar>
          </slot>
          <auto-tooltip :content="title" style="width: 65%">
            {{ title }}
          </auto-tooltip>
        </div>
      </slot>
    </div>
    <div class="description break-all mt-12" v-if="$slots.description || description !== undefined">
      <slot name="description">
        <div class="content">
          {{ description }}
        </div>
      </slot>
    </div>
    <!-- 新增显示标签的区域 -->
    <div class="tags-container" v-if="tags && tags.length > 0">
      <template v-for="(tag, index) in visibleTags" :key="index">
        <!-- 仅对折叠标签添加 el-tooltip -->
        <el-tooltip
          v-if="isEllipsis && index === maxVisible - 1"
          placement="top"
          effect="light"
          :content="ellipsisContent"
        >
          <template #content>
            <div style="display: flex; gap: 4px">
              <el-tag
                v-for="(item, index) in ellipsisContent.split(',')"
                :key="index"
                class="tootip-tags"
                size="small"
                type="info"
                >{{ item }}</el-tag
              >
            </div>
          </template>
          <el-tag class="tags" size="small" type="info">+{{ tags.length - maxVisible + 1 }}</el-tag>
        </el-tooltip>
        <el-tag
          v-else
          class="tags custom-tags"
          size="small"
          type="info"
        >
          <span>{{ tag }}</span>
        </el-tag>
      </template>
    </div>

    <slot />
    <slot name="mouseEnter" v-if="$slots.mouseEnter && show" />
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer" />
    </div>
  </el-card>
</template>
<script setup lang="ts">
import { ref, useSlots } from 'vue'
import { useCollapseTagsTooltip } from './useCollapseTagsTooltip' // 引入函数

const slots = useSlots()
defineOptions({ name: 'CardBoxSource' })
const props = withDefaults(
  defineProps<{
    /**
     * 标题
     */
    title?: string
    /**
     * 描述
     */
    description?: string
    /**
     * 是否展示icon
     */
    showIcon?: boolean
    /**
     * 标签数组
     */
    tags?: string[]
  }>(),
  { title: '标题', description: '', showIcon: true, border: true }
)

const show = ref(false)
function cardEnter() {
  show.value = true
}
function cardLeave() {
  show.value = false
}

const maxVisible = 5 // 最多显示几个标签，超出折叠
const { isEllipsis, visibleTags, ellipsisContent } = useCollapseTagsTooltip(
  props.tags as string[],
  maxVisible
)
</script>
<style lang="scss" scoped>
.tootip-tags {
  padding: 2px 4px;
  border: rgba(64, 158, 255, 0.4) 1px solid;
  font-size: 10px;
  color: #565772;
  border-radius: 4px;
  background: #fff;
}
.card-box {
  font-size: 14px;
  position: relative;
  min-height: var(--card-min-height);
  min-width: var(--card-min-width);
  border-radius: 8px;
  .description {
    color: var(--app-text-color-secondary);
    line-height: 22px;
    font-weight: 400;
    .content {
      display: -webkit-box;
      height: var(--app-card-box-description-height, 40px);
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
    }
  }
  /* 新增标签样式 */
  .tags-container {
    display: flex;
    gap: 4px;
    margin-top: 6px;
    max-width: 100%;
    .tags {
      padding: 2px 4px;
      border: rgba(64, 158, 255, 0.4) 1px solid;
      font-size: 10px;
      color: #565772;
      border-radius: 4px;
      background: #fff;
    }
  }

  .card-footer {
    position: absolute;
    bottom: 4px;
    left: 0;
    min-height: 30px;
    color: var(--app-text-color-secondary);
    font-weight: 400;
    padding: 0 16px;
    width: 100%;
    box-sizing: border-box;
  }
}
/* 使用深度选择器 */
:deep(.custom-tags) {
  .el-tag__content {
    width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  }
}
</style>
