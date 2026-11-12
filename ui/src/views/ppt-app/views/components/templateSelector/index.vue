<template>
    <div class="template-selector">
        <div class="templates">
            <div class="template" :class="{ selected: selectedTemplate === template.id }" v-for="template in templates"
                :key="template.id" @click="handleTemplateSelect(template.id)">
                <img :src="getImageUrl(template.cover)" :alt="template.name" />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue'

// 定义模板类型
interface Template {
    id: string
    name: string
    cover: string
}

// 定义 props
const props = defineProps<{
    templates: Template[]
    selectedTemplate: string
}>()

// 定义 emits
const emit = defineEmits<{
    'update:selectedTemplate': [value: string]
}>()

// 预加载图片模块
interface ImageModule {
    default: string
}

const images: Record<string, ImageModule> = import.meta.glob(
    '/src/views/ppt-app/mocks/imgs/*.jpg',
    {
        eager: true
    }
) as Record<string, ImageModule>

const getImageUrl = (name: string): string => {
    const path = `/src/views/ppt-app/mocks/imgs/${name}`
    return images[path].default
}

// 处理模板选择
const handleTemplateSelect = (templateId: string) => {
    emit('update:selectedTemplate', templateId)
}
</script>

<style lang="scss" scoped>
.template-selector {
    max-height: 100%;
    overflow: hidden;
    
    .templates {
        display: flex;
        justify-content: left;
        gap: 12px;
        overflow-y: auto;
        overflow-x: hidden;
        // margin-bottom: 16px;
        height: 100%;
        max-height: 100%;
        padding-right: 8px; // 为滚动条预留空间
        @include flex-grid-layout();
        padding-bottom: 4px;
        // 关键：防止滚动事件穿透到父级容器
        overscroll-behavior: contain;
        -webkit-overflow-scrolling: touch; // 提升移动端滚动体验
        .template {
            border: 2px solid $borderColor;
            border-radius: $borderRadius;
            width: 324px;
            height: 184px;
            cursor: pointer;
            transition: all 0.2s ease;
            flex-shrink: 0; // 防止模板被压缩

            &:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

            &.selected {
                border-color: $themeColor;
                box-shadow: 0 0 0 2px rgba(77, 107, 254, 0.2);
            }

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: calc($borderRadius - 2px);
                -webkit-user-drag: none;
            }
        }
    }
}

@media screen and (width <=800px) {
    .template-selector {
        .templates {
            max-height: 450px;
            display: block;
            overflow: auto;

            .template {
                width: 100%;
                height: unset;
                margin-bottom: 12px;

                &:last-child {
                    margin-bottom: 0;
                }
            }
        }
    }
}
</style>