<template>
  <div>
    <el-text type="info">
      <span class="ml-4">{{ datetimeFormat(data.create_time) }}</span>
    </el-text>
  </div>
  <div>
    <el-tooltip effect="dark" content="生成柱状图" placement="top" v-if="shouldShowElement1()">
        <el-button text @click="buildBar">
          <p style="color:blue;">生成柱状图</p>
        </el-button>
    </el-tooltip>
    <el-divider direction="vertical" v-if="shouldShowElement1()" />
    <el-tooltip effect="dark" content="生成饼图" placement="top" v-if="shouldShowElement1()">
        <el-button text @click="buildPie">
          <p style="color:blue;">生成饼图</p>
        </el-button>
    </el-tooltip>
    <el-divider direction="vertical" v-if="shouldShowElement1()" />

    <el-tooltip effect="dark" content="换个答案" placement="top">
      <el-button :disabled="chat_loading" text @click="regeneration">
        <AppIcon iconName="Refresh"></AppIcon>
      </el-button>
    </el-tooltip>
    <el-divider direction="vertical" />
    <el-tooltip effect="dark" content="复制" placement="top">
      <el-button text @click="copyClick(data?.answer_text)">
        <AppIcon iconName="app-copy"></AppIcon>
      </el-button>
    </el-tooltip>
    <el-divider direction="vertical" />
    <el-tooltip
      effect="dark"
      content="赞同"
      placement="top"
      v-if="buttonData?.vote_status === '-1'"
    >
      <el-button text @click="voteHandle('0')" :disabled="loading">
        <AppIcon iconName="app-like"></AppIcon>
      </el-button>
    </el-tooltip>
    <el-tooltip
      effect="dark"
      content="取消赞同"
      placement="top"
      v-if="buttonData?.vote_status === '0'"
    >
      <el-button text @click="voteHandle('-1')" :disabled="loading">
        <AppIcon iconName="app-like-color"></AppIcon>
      </el-button>
    </el-tooltip>
    <el-divider direction="vertical" v-if="buttonData?.vote_status === '-1'" />
    <el-tooltip
      effect="dark"
      content="反对"
      placement="top"
      v-if="buttonData?.vote_status === '-1'"
    >
      <el-button text @click="voteHandle('1')" :disabled="loading">
        <AppIcon iconName="app-oppose"></AppIcon>
      </el-button>
    </el-tooltip>
    <el-tooltip
      effect="dark"
      content="取消反对"
      placement="top"
      v-if="buttonData?.vote_status === '1'"
    >
      <el-button text @click="voteHandle('-1')" :disabled="loading">
        <AppIcon iconName="app-oppose-color"></AppIcon>
      </el-button>
    </el-tooltip>
  </div>
  <chartsDialog 
  ref="chartsDialogRef"
  />
</template>
<script setup lang="ts">
import applicationApi from '@/api/application';
import { copyClick } from '@/utils/clipboard';
import { datetimeFormat } from '@/utils/time';
import { ref } from 'vue';
import chartsDialog from './chartsDialog.vue';
const props = defineProps({
  data: {
    type: Object,
    default: () => {}
  },
  applicationId: {
    type: String,
    default: ''
  },
  chatId: {
    type: String,
    default: ''
  },
  chat_loading: {
    type: Boolean
  },
  log: Boolean
})

const emit = defineEmits(['update:data', 'regeneration', 'readAnswer'])

const buttonData = ref(props.data)
const loading = ref(false)
const chartsDialogRef = ref()

function readAnswer() {
  emit('readAnswer')
}

function regeneration() {
  emit('regeneration')
}

function voteHandle(val: string) {
  applicationApi
    .putChatVote(props.applicationId, props.chatId, props.data.record_id, val, loading)
    .then(() => {
      buttonData.value['vote_status'] = val
      emit('update:data', buttonData.value)
    })
}

function buildPie() {
  chartsDialogRef.value.open(props.applicationId, props.chatId, props.data, 'pie')
  console.log(props.applicationId,props.data.answer_text, 'applicationId')
}
function buildBar() {
  chartsDialogRef.value.open(props.applicationId, props.chatId, props.data, 'bar')
  console.log(props.applicationId,props.data.answer_text, 'applicationId')
}

function shouldShowElement1() {
  return props.applicationId === '8cc5ef86-5550-11ef-a540-e8611f4f18cd';
}

</script>
<style lang="scss" scoped></style>
