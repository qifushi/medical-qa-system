<template>
    <div class="applicationScenarios">
      <CmpHeader />
      <div class="main-page-content">
       <digitalContainer></digitalContainer>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import CmpHeader from '@/views/gateway-page/modules/CmpHeader.vue'
  import digitalContainer from './modules/index.vue'
  // import 'md-editor-v3/lib/style.css'
  </script>
  
  <style lang="scss" scoped>
  .applicationScenarios {
    // height: 100vh;
    box-sizing: border-box;
    overflow-y: auto;
    padding-top: 64px;
  
    .main-page-content {
      // max-width: 1200px;
      box-sizing: border-box;
      margin: 0 auto;
      padding: 0 24px;
      &::-webkit-scrollbar {
        width: 12px;
        height: 0;
      }
    }
  }
  </style>
  