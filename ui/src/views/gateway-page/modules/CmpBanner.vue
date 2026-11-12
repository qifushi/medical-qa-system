<template>
  <div class="cmp-banner">
    <div class="cmp-banner-content">
      <img class="banner-text" src="../../../assets/gatewayPage/banner-text.png" alt="" />
      <img class="banner-icon" src="../../../assets/gatewayPage/banner-icon.png" alt="" />
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.cmp-banner {
  background-size: 100% 100%;
  background-image: url('@/assets/gatewayPage/banner-bg.jpg');
  .cmp-banner-content {
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    padding: 120px 0;
    .banner-text {
      width: 41%;
    }
    .banner-icon {
      position: absolute;
      right: 0;
      width: 91%;
      bottom: 20px;
      margin-right: -22%;
    }
  }
}
@media (max-width: 560px) {
  .cmp-banner {
    .cmp-banner-content {
      padding: 40px;
      .banner-text {
        width: 80%;
      }
    }
  }
}
</style>
