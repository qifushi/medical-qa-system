<template>
  <div class="role-selection">
    <!-- 背景图容器（单独包裹背景图，保证居中） -->
    <div class="bg-wrapper">
      <img src="/medical/img/juese.png" alt="背景图" class="bg-img">
    </div>
    
    <div class="page-container">
      <!-- 欢迎文本 -->
      <div class="welcome-section">
        <p class="greeting">Hi，很高兴见到你</p>
        <h1 class="question">请问你想？</h1>
      </div>

      <!-- 选项卡片（居中容器） -->
      <div class="options-section">
        <div class="option-card" @click="selectRole('patient')">
          <div class="option-icon patient-icon">
            <img src="/medical/img/img1.png" alt="我是患者" />
          </div>
          <div class="option-text">
            <div class="option-title">我是患者</div>
            <div class="option-subtitle">主动管理，迎接更好的自己。</div>
          </div>
        </div>

        <div class="option-card" @click="selectRole('doctor')">
          <div class="option-icon doctor-icon">
            <img src="/medical/img/img2.png" alt="我是医生" />
          </div>
          <div class="option-text">
            <div class="option-title">我是医生</div>
            <div class="option-subtitle">随时在线，守护每一份信任。</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

// 选择角色
const selectRole = (role: string) => {
  if (role === 'patient') {
    router.push('/chatapp/medicalConsult')
  } else if (role === 'doctor') {
    router.push('/chatapp/doctorMain')
  }
}
</script>

<style scoped lang="scss">
// 外层容器：全屏 + 相对定位
.role-selection {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

// 背景图容器：绝对定位铺满 + 居中显示
.bg-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;

  .bg-img {
    width: 100%;
    height: 100%;
    object-fit: cover;    // 铺满容器不变形
    object-position: center; // 背景图居中显示
  }
}

// 内容容器：居中 + 不超出背景图
.page-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 350px;      // 小于背景图宽度，保证居中且不出格
  height: 100vh;
  margin: 0 auto;        // 水平居中（背景图宽度中间）
  display: flex;
  flex-direction: column;
  padding: 0 20px;       // 左右留白，防止按钮贴边
  padding-top: 25vh;
  box-sizing: border-box; // 内边距计入宽度
}

// 欢迎文本区
.welcome-section {
  margin-bottom: 40px;
  width: 100%;
  text-align: center;    // 文字也居中
}

.greeting {
  font-size: 17px;
  color: #2b3d7b;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.question {
  font-size: 34px;
  font-weight: 600;
  color: #2b3d7b;
  margin: 0;
  letter-spacing: 1px;
  text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9);
}

// 按钮容器：居中 + 宽度限制
.options-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;           // 继承容器宽度（背景图中间）
}

// 按钮样式：固定宽度 + 居中
.option-card {
  width: 100%;           // 不超容器宽度
  max-width: 100%;       // 强制不出格
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 28px;
  padding: 24px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-sizing: border-box;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.985);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

.option-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 16px;
  overflow: hidden;
  background-color: rgba(245, 247, 250, 0.8);

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
}

.option-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a2b4b;
  margin: 0;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.9);
}

.option-subtitle {
  font-size: 13px;
  color: #667788;
  margin: 0;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.8);
}

// 小屏适配（320px以下）
@media (max-width: 320px) {
  .page-container {
    max-width: 300px;
    padding: 0 16px;
    padding-top: 22vh;
  }
  
  .option-card {
    padding: 20px 16px;
    border-radius: 24px;
  }
  
  .option-title {
    font-size: 18px;
  }
  
  .option-icon {
    width: 40px;
    height: 40px;
  }
}
</style>