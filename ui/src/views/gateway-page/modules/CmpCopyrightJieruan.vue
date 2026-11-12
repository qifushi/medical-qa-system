<template>
  <div class="copyright">
    <div class="copyright-content">
      <div v-if="logoAndCopyright.isShowLogoAndCopyright">
        Copyright © 2003-2025 JRSoft Technology Co.Ltd.
        <span class="tips1">All rights reserved.</span>
      </div>
      <div class="tips2" v-if="logoAndCopyright.isShowLogoAndCopyright">All rights reserved.</div>
      <div v-if="logoAndCopyright.isShowLogoAndCopyright">杰软科技（集团）有限公司 京ICP备18031564号-1</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useStore from '@/stores'
const { logoAndCopyright } = useStore()
</script>

<style lang="scss" scoped>
.copyright {
  background-color: #292929;
  padding: 12px;
  text-align: center;
  .copyright-content {
    max-width: 1200px;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 78px;
    margin: 0 auto;
    font-size: 14px;
    color: #999;
    flex-direction: column;
    & > div {
      margin-bottom: 6px;
      &:last-child {
        margin-bottom: 0;
      }
    }
    .tips1 {
      display: inline-block;
    }
    .tips2 {
      display: none;
    }
  }
}
@media (max-width: 560px) {
  .copyright {
    .copyright-content {
      .tips1 {
        display: none;
      }
      .tips2 {
        display: block;
      }
    }
  }
}
</style>
