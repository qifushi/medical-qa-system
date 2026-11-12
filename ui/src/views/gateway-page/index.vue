<template>
  <div class="main-page">
    <CmpHeader />

    <CmpBanner />
    <div class="page-content">
      <div class="page-content-inner">
        <CmpInput />
        <CmpServices />
      </div>
    </div>
    <CmpContactInfo />
    <CmpCopyright />
    <div class="logoImg" @click="goAudioCall">
      <img :src="logoImg" alt="" />
    </div>
  </div>
</template>

<script setup lang="ts">
import logoImg from '@/assets/kefu.gif'
import useStore from '@/stores'
import { useRouter } from 'vue-router'
import CmpBanner from './modules/CmpBanner.vue'
import CmpContactInfo from './modules/CmpContactInfo.vue'
import CmpCopyright from './modules/CmpCopyright.vue'
import CmpHeader from './modules/CmpHeader.vue'
import CmpInput from './modules/CmpInput.vue'
import CmpServices from './modules/CmpServices.vue'

const { logoAndCopyright } = useStore()
const router = useRouter()

function goAudioCall() {
  router.push({ name: 'audioCall' })
}
</script>

<style lang="scss" scoped>
.main-page {
  height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
  padding-top: 64px;
  &::-webkit-scrollbar {
    width: 0;
    height: 0;
  }
  .page-content {
    // max-width: 1200px;
    // margin: 0 auto;
    position: relative;
    &::after {
      content: '';
      position: absolute;
      left: 0;
      width: 100vw;
      height: 100%;
      top: 0;
      background-image: url('@/assets/gatewayPage/body_bg.jpg');
      background-size: 100% 100%;
      background-position: center;
      z-index: -1;
    }
    .page-content-inner {
      max-width: 1200px;
      margin: 0 auto;
    }
  }
  .logoImg {
    position: fixed;
    right: 40px;
    bottom: 15%;
    cursor: pointer;
    width: 70px;
    height: 70px;
    background-color: #fff;
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    img {
      object-fit: cover;

      width: 100%;
      height: 100%;
      // 禁止选中、拖动
      -webkit-user-drag: none;
      user-select: none;
    }
  }
}
@media (max-width: 560px) {
  .main-page {
    .logoImg {
      width: 52px;
      height: 52px;
      right: 20px;
      bottom: 10%;

      img {
      }
    }
  }

  :deep(.cmp-services) {
    margin-top: 24px;
  }
}
:deep(.cmp-services) {
  margin-top: 80px;
}

:deep(.cmp-input) {
  margin-top: -28px;
}
@media (max-width: 560px) {
  .main-page {
    .page-content {
      .page-content-inner {
        padding: 0 24px;
      }
    }
  }
  :deep(.cmp-services) {
    margin-top: 24px;
  }
}
</style>
