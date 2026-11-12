<template>
  <div class="menu">
    <div class="menu-logo" @click="goHome">
      <img src="~@/assets/chatapp-page/small_logo.png" alt="" />
    </div>
    <div class="menu-list">
      <div
        class="menu-list-item"
        v-for="(item, index) in menuList"
        :key="index"
        @click="selectMenu(item, index)"
      >
        <div class="menu-list-item-content" :class="{ active: activeIndex === index }">
          <b></b>
          <b></b>
          <div class="menu-list-item-icon">
            <img
              :src="
                activeIndex === index
                  ? `/src/assets/chatapp-page/${item.activeIcon}`
                  : `/src/assets/chatapp-page/${item.icon}`
              "
              alt=""
            />
          </div>
          {{ item.label }}
        </div>
      </div>
    </div>
    <div class="menu-user">
      <img src="~@/assets/chatapp-page/roll20.png" alt="" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeIndex = ref(0)

const selectMenu = (item: any, index: number) => {
  activeIndex.value = index
  console.log(item, index, activeIndex.value, '111')
}
const menuList = [
  {
    icon: 'roll1.png',
    activeIcon: 'roll2.png',
    label: '行业对话'
  },
  {
    icon: 'roll3.png',
    activeIcon: 'roll4.png',
    label: '文本生成'
  },
  {
    icon: 'roll5.png',
    activeIcon: 'roll6.png',
    label: '智能查询'
  },
  {
    icon: 'roll7.png',
    activeIcon: 'roll8.png',
    label: '图谱助手'
  },
  {
    icon: 'roll9.png',
    activeIcon: 'roll10.png',
    label: '合规审查'
  },
  {
    icon: 'roll11.png',
    activeIcon: 'roll12.png',
    label: '语言助手'
  },
  {
    icon: 'roll3.png',
    activeIcon: 'roll4.png',
    label: '文档阅读'
  }
]
const goHome = () => {
  console.log('111')
  router.push({
    name: 'home'
  })
}
</script>
<style scoped lang="scss">
.menu {
  user-select: none;
  background-color: #329cff; // 暂时方便查看
  flex: 0 0 100px;
  width: 100px;
  height: calc(100% - 40px); // 减去父元素底部padding
  position: relative;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  padding-top: 24px;
  overflow: hidden;
  border-radius: 18px;
  .menu-logo {
    cursor: pointer;
    margin-bottom: 30px;
    width: 50px;
    height: 48px;
    flex: 0 1 48px;
    img {
      width: 100%;
      height: 100%;
      object-fit: contain; /* 保持图片比例 */
    }
  }
  .menu-list {
    width: 100%;
    flex: 1 1 0%;
    display: flex;
    flex-direction: column;
    padding: 0px;
    margin: 0px;
    .menu-list-item {
      position: relative;
      font-weight: normal;
      margin-bottom: 20px;
      cursor: pointer;
      color: #fff;

      // transition: all 0.3s ease-in-out; /* 添加过渡效果 */
      .menu-list-item-content {
        user-select: none;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        margin-left: 6px;
        box-sizing: border-box;
        &.active {
          color: #329cff;
          background-color: #f8f8fd;
          border-top-left-radius: 60px;
          border-bottom-left-radius: 60px;
          box-shadow: 0px 4px 10px rgba(50, 156, 255, 0.5); /* 增加阴影效果 */
          b:nth-child(1),
          b:nth-child(2) {
            display: block;
          }
        }
      }
      .menu-list-item-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        user-select: none;

        // position: absolute;
        // top: 0px;
        // left: 0px;
        img {
          width: 100%;
          height: 100%;
          object-fit: contain; /* 保持图片比例 */
        }
      }

      b:nth-child(1) {
        position: absolute;
        top: -15px;
        height: 15px;
        width: 100%;
        background: #fff;
        display: none;
      }
      b:nth-child(1)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-bottom-right-radius: 20px;
        background: #329cff;
      }
      b:nth-child(2) {
        position: absolute;
        bottom: -15px;
        height: 15px;
        width: 100%;
        background: #fff;
        display: none;
      }
      b:nth-child(2)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-top-right-radius: 20px;
        background: #329cff;
      }
    }
  }
  .menu-user {
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
  }
}
</style>
