<template>
  <div class="cmp-contact-info">
    <div class="cmp-contact-content">
      <div class="contact-item" v-for="(item, index) in contactList" :key="index">
        <div class="contact-icon">
          <img :src="item.icon" alt="" />
        </div>
        <div class="contact-des">
          <div class="contact-label">{{ item.label }}</div>
          <div class="contact-value">{{ item.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import icon1 from '@/assets/gatewayPage/roll10.png'
import icon2 from '@/assets/gatewayPage/roll11.png'
import icon3 from '@/assets/gatewayPage/roll12.png'
const contactList = [
  {
    icon: icon1,
    label: 'CALL US',
    value: '010-82781931,010-82784088'
  },
  {
    icon: icon2,
    label: 'ADDRESS',
    value: '北京市海淀区绿地中央广场'
  },
  {
    icon: icon3,
    label: 'EMAIL',
    value: 'zhouyingying@jrsoft.com.cn'
  }
]
</script>

<style lang="scss" scoped>
.cmp-contact-info {
  background-color: #efefef;
  padding: 40px;
  .cmp-contact-content {
    display: flex;
    justify-content: space-around;
    max-width: 1200px;
    margin: 0 auto;
    .contact-item {
      display: flex;
      flex-wrap: wrap;
      flex: 1;
      .contact-icon {
        width: 32px;
        overflow: hidden;
        margin-right: 14px;
        img {
          width: 100%;
        }
      }
      .contact-des {
        width: calc(100% - 32px - 14px);
        color: #333;
        color: 14px;
        .contact-label {
        }
      }
    }
  }
}
@media (max-width: 560px) {
  .cmp-contact-info {
    .cmp-contact-content {
      flex-direction: column;
      .contact-item {
        margin-bottom: 12px;
        &:last-child {
          margin-bottom: 0;
        }
      }
    }
  }
}
</style>
