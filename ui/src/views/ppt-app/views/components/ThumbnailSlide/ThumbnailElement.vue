<template>
  <div 
    class="base-element"
    :class="`base-element-${elementInfo.id}`"
    :style="{
      zIndex: elementIndex,
    }"
  >
    <component
      :is="currentElementComponent"
      :elementInfo="elementInfo"
      target="thumbnail"
    ></component>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { ElementTypes, type PPTElement } from '@pptApp/types/slides'

import BaseImageElement from '@pptApp/views/components/element/ImageElement/BaseImageElement.vue'
import BaseTextElement from '@pptApp/views/components/element/TextElement/BaseTextElement.vue'
import BaseShapeElement from '@pptApp/views/components/element/ShapeElement/BaseShapeElement.vue'
import BaseLineElement from '@pptApp/views/components/element/LineElement/BaseLineElement.vue'
import BaseChartElement from '@pptApp/views/components/element/ChartElement/BaseChartElement.vue'
import BaseTableElement from '@pptApp/views/components/element/TableElement/BaseTableElement.vue'
import BaseLatexElement from '@pptApp/views/components/element/LatexElement/BaseLatexElement.vue'
import BaseVideoElement from '@pptApp/views/components/element/VideoElement/BaseVideoElement.vue'
import BaseAudioElement from '@pptApp/views/components/element/AudioElement/BaseAudioElement.vue'

const props = defineProps<{
  elementInfo: PPTElement
  elementIndex: number
}>()

const currentElementComponent = computed<unknown>(() => {
  const elementTypeMap = {
    [ElementTypes.IMAGE]: BaseImageElement,
    [ElementTypes.TEXT]: BaseTextElement,
    [ElementTypes.SHAPE]: BaseShapeElement,
    [ElementTypes.LINE]: BaseLineElement,
    [ElementTypes.CHART]: BaseChartElement,
    [ElementTypes.TABLE]: BaseTableElement,
    [ElementTypes.LATEX]: BaseLatexElement,
    [ElementTypes.VIDEO]: BaseVideoElement,
    [ElementTypes.AUDIO]: BaseAudioElement,
  }
  return elementTypeMap[props.elementInfo.type] || null
})
</script>