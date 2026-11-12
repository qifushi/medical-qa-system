<template>
  <div class="export-dialog">
    <Tabs 
      :tabs="tabs" 
      :value="dialogForExport" 
      card
      @update:value="key => setDialogForExport(key as DialogForExportTypes)" 
    />
    <div class="content">
      <component :is="currentDialogComponent" @close="setDialogForExport('')"></component>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useMainStore } from '@pptApp/store'
import type { DialogForExportTypes } from '@pptApp/types/export'

import ExportImage from './ExportImage.vue'
import ExportJSON from './ExportJSON.vue'
import ExportPDF from './ExportPDF.vue'
import ExportPPTX from './ExportPPTX.vue'
import ExportSpecificFile from './ExportSpecificFile.vue'
import Tabs from '@pptApp/components/Tabs.vue'
import { Role } from '@/utils/permission/type'
import { hasPermission } from '@/utils/permission'

interface TabItem {
  key: DialogForExportTypes
  label: string
}

const mainStore = useMainStore()
const { dialogForExport } = storeToRefs(mainStore)

const setDialogForExport = mainStore.setDialogForExport
const isAdmin = computed(() => hasPermission(new Role('ADMIN'), 'OR'))
const tabs = computed<TabItem[]>(() => {
  const defaultTabs: TabItem[] = [
    { key: 'pptx', label: '导出 PPTX' },
    { key: 'image', label: '导出图片' },
    { key: 'pdf', label: '打印 / 导出 PDF' },
  ]
  
  if (isAdmin.value) {
    return [
      ...defaultTabs,
      { key: 'json', label: '导出 JSON' },
      { key: 'pptist', label: '导出 PPTIST 文件' },
    ]
  }
  
  return defaultTabs
})

const currentDialogComponent = computed<unknown>(() => {
  const dialogMap = {
    'image': ExportImage,
    'json': ExportJSON,
    'pdf': ExportPDF,
    'pptx': ExportPPTX,
    'pptist': ExportSpecificFile,
  }
  if (dialogForExport.value) return dialogMap[dialogForExport.value] || null
  return null
})
</script>

<style lang="scss" scoped>
.export-dialog {
  margin: -20px;
}
.content {
  height: 460px;
  padding: 12px;
  font-size: 13px;

  @include overflow-overlay();
}
</style>