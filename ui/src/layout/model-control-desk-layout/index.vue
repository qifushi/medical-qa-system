<template>
  <div class="app-layout">
    <CmpHeader />
    <div :class="['app-main', activeNav == 'ModelControlIndex' ? 'isHome' : '']">
      <AppMain />
      <CmpStepInstructions />
    </div>
  </div>
</template>
<script setup lang="ts">
import CmpStepInstructions from '@/views/model-control-desk/components/CmpStepInstructions/index.vue'
import CmpHeader from './components/CmpHeader.vue'
import { AppMain } from '../components'
import { computed, ref } from 'vue'

import { useRouter, useRoute } from 'vue-router'
const route = useRoute()

const activeNav = computed(() => {
  return route.name
})
</script>

<style lang="scss" scoped>
.app-layout {
  background-color: var(--app-layout-bg-color);
  min-height: 100vh;
  position: relative;
}

.app-main {
  position: relative;
  min-height: 100%;
  padding: 56px 0 0;
  box-sizing: border-box;
  overflow: auto;
  z-index: 1;
  &.isHome {
    padding-top: 0;
  }
}
</style>
