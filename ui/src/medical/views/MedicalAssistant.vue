<template>
  <div class="medical-assistant">
    <div class="container">
      <h2>知贝医疗助手</h2>
      <p class="description">专业的医疗AI助手，为您提供健康咨询和医疗建议</p>
      <div class="chat-container">
        <MedicalChat />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MedicalChat from '../components/MedicalChat.vue'
</script>

<style scoped lang="scss">
.medical-assistant {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 0;

  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;

    h2 {
      text-align: center;
      color: #303133;
      margin-bottom: 8px;
      font-size: 28px;
      font-weight: 600;
    }

    .description {
      text-align: center;
      color: #606266;
      margin-bottom: 40px;
      font-size: 16px;
    }

    .chat-container {
      height: 600px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    }
  }
}

@media (max-width: 768px) {
  .medical-assistant {
    padding: 20px 0;

    .container {
      .chat-container {
        height: 500px;
      }
    }
  }
}
</style>