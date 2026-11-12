<template>
  <LayoutContainer header="项目管理">
    <div class="template-manage flex main-calc-height">
      <iframe src="http://localhost:1717/" style="width: 100%" frameborder="0"></iframe>
    </div>
  </LayoutContainer>
</template>

<script lang="ts" setup></script>

<style lang="scss" scoped>
.template-manage {
  &__left {
    box-sizing: border-box;
    width: var(--setting-left-width);
    min-width: var(--setting-left-width);
  }

  .model-list-height {
    height: calc(var(--create-dataset-height) - 70px);
  }
}
</style>
