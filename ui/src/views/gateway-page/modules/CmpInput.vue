<template>
  <div class="cmp-input">
    <el-input
      ref="inputRef"
      v-model="textarea"
      :rows="2"
      type="textarea"
      placeholder="请输入您想要查询的内容......"
      resize="none"
      @keydown.enter="sendChatHandle($event)"
    />
    <div class="tools-wrap">
      <img src="~@/assets/gatewayPage/roll1.jpg" alt="" />
      <div class="btn-submit" @click="sendChatHandle">发送</div>
    </div>
  </div>
  <div class="cmp-hot">
    <div class="hot-label">
      <img src="~@/assets/gatewayPage/roll2.png" alt="" />
      大家都在问：
    </div>
    <div class="hot-tag-wrap">
      <div
        class="hot-tag-item"
        @click="handleTagClick(item)"
        v-for="(item, index) in hotList"
        :key="index"
      >
        {{ item }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useStore from '@/stores';
import { ElMessage } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const { application } = useStore()

const textarea = ref('')
const hotList = [
  '各单位年度立项数统计',
  '项目的完成进度相对于计划(里程碑)进度的百分比',
  '亚运会对周边城市社会心理的影响分析'
]
const router = useRouter()
const inputRef = ref()
const { user } = useStore()
const token = user.getToken()
const sendChatHandle = (event: any) => {
  event.preventDefault()
  // 检查是否按下了 Shift 键
  if (event.shiftKey) {
    // 如果按下了 Shift 键，加一个换行符
    textarea.value += '\n'
  } else {
    // 如果没有按下组合键 Shift，则阻止默认事件并处理发送逻辑

    if (textarea.value.trim() === '') return
    // 将输入内容存储到 localStorage 中
    localStorage.setItem('indexMessageContent', textarea.value)
    if (!token) {
      ElMessage.error('还没登录，请先登陆')
      router.push(`/login?redirect=industryTalk`)
    } else {
      router.push({ name: 'industryTalk' })
    }
    // 清空输入框
    textarea.value = ''
  }
}

const handleTagClick = (tag: string) => {
  textarea.value = tag
}
onMounted(() => {
  // 自动聚焦到输入框内
  inputRef.value.focus()
})
</script>

<style lang="scss" scoped>
.cmp-input {
  box-shadow: 0px 2px 4px 0px rgba(31, 35, 41, 0.12);
  border: 1px solid #e4e4e4;
  height: 140px;
  border-radius: 12px;
  position: relative;
  padding: 24px;
  background-color: #fff;
  .tools-wrap {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    img {
      cursor: pointer;
      margin-right: 6px;
    }
  }
  .btn-submit {
    padding: 6px 24px;
    color: #fff;
    background-color: #329dff;
    border-radius: 6px;
    cursor: pointer;
    user-select: none;
    &:hover {
      background-color: #065fb3;
    }
  }
}
.cmp-hot {
  margin-top: 20px;
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
  .hot-label {
    display: flex;
    align-items: center;
    width: 125px;
    color: #7c7c7c;
    height: 32px;
  }
  .hot-tag-wrap {
    width: calc(100% - 125px);
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    .hot-tag-item {
      user-select: none;
      line-height: 32px;
      box-sizing: border-box;
      // background-color: #fff;
      box-shadow: 0px 2px 4px 0px rgba(31, 35, 41, 0.12);
      padding: 0 24px;
      border-radius: 10px;
      cursor: pointer;
      border: 1px solid #e4e4e4;
      background-size: 100%;
      transition: all 1.3s;

      &:hover {
        background: linear-gradient(18deg, #e2f0ff 8%, #f3f8ff 50%, #f0f5ff 82%);
        // background-color: transparent;
      }
    }
  }
}
:deep(.el-textarea__inner ) {
    box-shadow: none;
    height: 110px;
}
@media (max-width: 560px) {
  .cmp-input {
    height: 80px;
    :deep(.el-textarea__inner ) {
        box-shadow: none;
        height: 55px;
    }
  }
  .cmp-hot {
    flex-direction: column;
    .hot-label {
      margin-bottom: 12px;
    }
    .hot-tag-wrap {
      width: 100%;
      .hot-tag-item {
        width: 100%;
      }
    }
  }
}
</style>
