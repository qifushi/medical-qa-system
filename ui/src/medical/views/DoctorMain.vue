<template>
  <div class="doctor-main">
    <div class="container">
      <!-- 顶部背景图（img31）+ 左上角返回按钮 -->
      <div class="header-bg">
        <img src="/medical/img/img31.png" alt="医生背景" class="bg-img">
        <!-- 返回按钮：放在背景图红框位置 -->
        <button class="btn-back" @click="goBack">←</button>
      </div>

      <!-- 功能菜单容器 -->
      <div class="menu-container">
        <div class="menu-list">
          <button class="menu-item">
            <img src="/medical/img/img32.png" alt="医疗大模型检索" class="menu-icon">
            <div class="menu-content">
              <div class="menu-title">医疗大模型检索</div>
              <div class="menu-desc">以百川大模型为基础，通过融合权威医学知识，为您提供精准的信息服务</div>
            </div>
            <span class="menu-arrow">➤</span>
          </button>

          <button class="menu-item">
            <img src="/medical/img/img33.png" alt="我的本地知识库" class="menu-icon">
            <div class="menu-content">
              <div class="menu-title">我的本地知识库</div>
              <div class="menu-desc">集成构建您的本地知识库，无需联网，绝对机密</div>
            </div>
            <span class="menu-arrow">➤</span>
          </button>

          <button class="menu-item">
            <img src="/medical/img/img34.png" alt="一对一线上问诊" class="menu-icon">
            <div class="menu-content">
              <div class="menu-title">一对一线上问诊</div>
              <div class="menu-desc">通过网络连接您与患者的问诊交流，无需线下到访，灵活运用时间</div>
            </div>
            <span class="menu-arrow">➤</span>
          </button>

          <button class="menu-item">
            <img src="/medical/img/img35.png" alt="面对面AI就诊摘要" class="menu-icon">
            <div class="menu-content">
              <div class="menu-title">面对面AI就诊摘要</div>
              <div class="menu-desc">AI记录您与患者的沟通对话，生成摘要与总结</div>
            </div>
            <span class="menu-arrow">➤</span>
          </button>
        </div>
      </div>

      <!-- 底部导航：无缝紧贴菜单 -->
      <div class="bottom-nav">
        <a href="#" class="nav-item">
          <img src="/medical/img/img19.png" alt="消息" class="nav-icon">
          <span>消息</span>
        </a>
        <a href="#" class="nav-item active home-nav">
          <div class="home-icon-wrapper">
            <img src="/medical/img/img4.png" alt="首页" class="nav-icon home-icon">
          </div>
          <span>首页</span>
        </a>
        <a href="#" class="nav-item">
          <img src="/medical/img/img18.png" alt="我的" class="nav-icon">
          <span>我的</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}

onMounted(() => {
  console.log('医生主界面加载完成')
})
</script>

<style scoped lang="scss">
.doctor-main {
  width: 100%;
  background: #fff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.container {
  max-width: 375px;
  margin: 0 auto;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: auto;
  overflow: visible;
  transform: scale(1);
}

// 顶部背景图 + 返回按钮
.header-bg {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative; // 为返回按钮提供定位上下文

  .bg-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top;
  }

  // ✅ 返回按钮：精准放到第二张图红框位置
  .btn-back {
    position: absolute;
    top: 20px;    // 垂直位置
    left: 16px;   // 水平位置
    background: none;
    border: none;
    font-size: 24px;
    color: #333;
    cursor: pointer;
    padding: 0;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
  }
}

// 菜单容器：移除底部 padding，让导航紧贴
.menu-container {
  background: #fff;
  border-radius: 20px 20px 0 0;
  padding: 16px 16px 0;
  margin-top: -20px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 18px 16px;
  border-radius: 12px;
  color: #333;
  text-decoration: none;
  gap: 16px;
  border: none;
  background: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
  font-family: inherit;

  &:nth-child(1) { background-color: #fff3e0; }
  &:nth-child(2) { background-color: #e3f2fd; }
  &:nth-child(3) { background-color: #ffebee; }
  &:nth-child(4) { background-color: #e0f7fa; }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }
}

.menu-icon {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.menu-content {
  flex: 1;
}

.menu-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

.menu-desc {
  font-size: 15px;
  color: #996644;
  line-height: 1.4;
}

.menu-arrow {
  font-size: 20px;
  color: #999;
  margin-left: auto; // 箭头固定在最右侧
}

// 底部导航：添加顶部阴影分隔
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: #fff;
  padding: 12px 0 20px;
  border-top: 1px solid #eee;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  width: 100%;
  margin: 0;
  flex-shrink: 0;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #666;
  font-size: 14px;
  gap: 6px;
  transition: all 0.3s ease;

  &.active {
    color: #673ab7;
  }
  
  &:hover {
    color: #673ab7;
  }
}

// 首页按钮样式：中间凸起大图标
.home-nav {
  transform: translateY(-16px);

  .home-icon-wrapper {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .home-icon {
    width: 32px;
    height: 32px;
    object-fit: contain;
  }
  
  span {
    font-weight: 600;
    font-size: 14px;
    margin-top: 4px;
  }
}

.nav-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}
</style>