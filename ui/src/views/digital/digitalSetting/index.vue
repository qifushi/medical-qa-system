<template>
  <LayoutContainer class="create-application mr-8 ml-8" >
    <template #header v-if="false">
      <!-- 头部 头像 -->
      <div class="flex-center w-full" >
        <AppIcon class="sticky-item" iconName="app-circle-plus"></AppIcon>
        <div class="w-full">
          <el-scrollbar>
            <div class="scrollbar-flex-content">
              <el-avatar :icon="UserFilled"  v-for="item in 50" :key="item" class="scrollbar-demo-item"  />
            </div>
          </el-scrollbar>
        </div>
      </div>
    </template>
  </LayoutContainer>
</template>
<script setup lang="ts">
import { UserFilled } from '@element-plus/icons-vue';
</script>
<style lang="scss" scoped>
.sticky-item {
  font-size: 50px;
  color: #2f99ff;
  flex-shrink: 0;
}
.scrollbar-item {
  margin-left: 10px;
}

.scrollbar-flex-content {
  display: flex;
}
.scrollbar-demo-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px;
  text-align: center;
}
</style>
