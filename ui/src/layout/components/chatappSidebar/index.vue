<template>
  <div class="menu">
    <div class="menu-logo" @click="goHome">
      <img src="~@/assets/chatapp-page/small_logo.png" alt="" />
    </div>
    <div class="menu-list">
      <div
        class="menu-list-item"
        v-for="(menu, index) in subMenuList"
        :key="index"
        @click="menu.meta?.disabled ? null : selectMenu(menu, index)"
        :class="{ 'menu-list-item--disabled': menu.meta?.disabled }"
      >
        <div
          class="menu-list-item-content"
          :class="{ active: activeMenu === (menu.meta?.active || menu.path) }"
        >
          <b></b>
          <b></b>
          <div class="menu-list-item-icon">
            <img
              :src="
                getImageUrl(
                  (activeMenu === (menu.meta?.active || menu.path)
                    ? menu.meta?.activeIcon
                    : menu.meta?.icon) as string
                )
              "
              alt=""
            />
            <!-- <img
              :src="
                activeMenu === (menu.meta?.active || menu.path)
                  ? `/src/assets/chatapp-page/${menu.meta?.activeIcon}`
                  : `/src/assets/chatapp-page/${menu.meta?.icon}`
              "
              alt=""
            /> -->
          </div>
          {{ menu.meta?.title }}
        </div>
      </div>
    </div>
    <div class="menu-user">
      <img src="~@/assets/chatapp-page/roll20.png" alt=""/>
    </div>
  </div>
</template>
<script setup lang="ts">
import { getChildRouteListByPathAndName } from '@/router/index'

import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
const subMenuList = computed(() => {
  const { meta } = route
  let childrenRoute =  getChildRouteListByPathAndName(meta.parentPath, meta.parentName)
  
   return  childrenRoute.filter(route => !route.meta?.hidden)
})

const activeMenu = computed(() => {
  const { path, meta } = route

  return meta.active || path
})
const selectMenu = (menu: any, index: number) => {
  console.log(menu, 'menu')

  if (menu.name === 'textGeneration') {
    // 连接大纲应用id
    router.push({ path: '/textGeneration/c24a374e-329f-11ef-8f88-0242ac110005' })
  } else {
    router.push({ name: menu.name })
  }
}

const goHome = () => {
  router.push({
    name: 'home'
  })
}

// 预加载 chatapp-page 目录下所有 png 图片
// 定义图片模块的接口类型
interface ImageModule {
  default: string
}
// 使用类型断言指定images对象的类型
const images: Record<string, ImageModule> = import.meta.glob('/src/assets/chatapp-page/*.png', {
  eager: true
}) as Record<string, ImageModule>

const getImageUrl = (name: string): string => {
  // 构建完整的图片路径
  const path = `/src/assets/chatapp-page/${name}`
  // 返回图片的实际URL
  return images[path].default
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
      &--disabled {
        opacity: 0.5;
        cursor: not-allowed;

        &:hover {
          cursor: not-allowed;
        }
      }
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
