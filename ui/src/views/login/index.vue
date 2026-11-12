<template>
  <login-layout v-loading="loading">
    <LoginContainer subTitle="欢迎使用 Smart Brain 智能知识库" style="user-select: none">
      <h2 class="mb-24" style="user-select: none">普通登录</h2>
      <el-form
        class="login-form"
        :rules="rules"
        :model="loginForm"
        ref="loginFormRef"
        @keyup.enter="login"
      >
        <div class="mb-24">
          <el-form-item prop="username">
            <el-input
              size="large"
              class="input-item"
              v-model="loginForm.username"
              placeholder="请输入用户名"
            >
            </el-input>
          </el-form-item>
        </div>
        <div class="mb-24">
          <el-form-item prop="password">
            <el-input
              type="password"
              size="large"
              class="input-item"
              v-model="loginForm.password"
              placeholder="请输入密码"
              show-password
            >
            </el-input>
          </el-form-item>
        </div>
      </el-form>
      <el-button size="large" type="primary" class="w-full" @click="login">登录</el-button>
      <div class="operate-container flex-between mt-12">
        <!-- <el-button class="register" @click="handlePoW" link type="primary"> 工作量证明 </el-button> -->
        <el-button
          class="forgot-password"
          @click="router.push('/forgot_password')"
          link
          type="primary"
        >
          忘记密码?
        </el-button>
      </div>
    </LoginContainer>
  </login-layout>
</template>
<script setup lang="ts">
import type { LoginRequest } from '@/api/type/user'
import useStore from '@/stores'
import type { FormInstance, FormRules } from 'element-plus'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import UserApi from '@/api/user'

const loading = ref<boolean>(false)
const { user } = useStore()
const router = useRouter()
const loginForm = ref<LoginRequest>({
  username: '',
  password: ''
})

const rules = ref<FormRules<LoginRequest>>({
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: 'blur'
    }
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    }
  ]
})
const loginFormRef = ref<FormInstance>()
const { application } = useStore()

const login = () => {
  loginFormRef.value?.validate().then(() => {
    loading.value = true
    user
      .login(loginForm.value.username, loginForm.value.password)
      .then(() => {
        const redirect = router.currentRoute.value.query.redirect
        if (redirect) {
          // 首页点击应用，跳转到对外的应用页面
          if (redirect.includes('graphAssistant')) {
            // 暂定跳转到公平感知识库中
            router.push(`/dataset/d351a342-27b9-11ef-a3a5-0242ac110005/document`)
          } else if (redirect.includes('textGeneration')) {
            router.push({
              name: 'textGeneration',
              params: { id: 'c24a374e-329f-11ef-8f88-0242ac110005' }
            })
          } else {
            router.push({ name: redirect as string })
          }
        } else {
          router.push({ name: 'home' })
        }
      })
      .finally(() => (loading.value = false))
  })
}

const progress = ref(0)
// 获取挑战码
const getChallenge = async () => {
  const response = await UserApi.getChallengeCode()
  return response.data
}

// PoW计算函数
const calculatePoW = async (challenge: string, difficulty: number) => {
  progress.value = 0

  let nonce = 0
  const prefix = '0'.repeat(difficulty)

  // 通过循环来实现工作量证明的计算过程
  // eslint-disable-next-line no-constant-condition
  while (true) {
    // 定期更新进度（每10万次）
    if (nonce % 100000 === 0) {
      progress.value = Math.min(99, Math.floor(nonce / 1000000))
    }

    const testStr = challenge + nonce
    const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(testStr))
    const hexHash = Array.from(new Uint8Array(hash))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('')

    if (hexHash.startsWith(prefix)) {
      return nonce
    }
    nonce++
  }
}

// 工作量证明处理
const handlePoW = async () => {
  try {
    // 1. 获取挑战码
    const { challenge, difficulty } = await getChallenge()

    // 2. 进行PoW计算，获得满足条件的随机数
    const nonce = await calculatePoW(challenge, difficulty)

    // 3. 提交证明请求
    const response = await UserApi.postChallengeProof({
      challenge,
      nonce
    })
  } catch (error: any) {}
}
</script>
<style lang="scss" scope></style>
