<template>
  <LayoutContainer class="create-application">
    <template #header>
      <div class="flex-between w-full">
        <h3>数字人对话</h3>
      </div>
    </template>
    <el-row v-loading="loading">
      <el-col :span="24">
        <!-- <div class="p-24 mb-16" style="padding-bottom: 0">
          <h4 class="title-decoration-1 ">数字人预览</h4>
        </div> -->
        <div class="scrollbar-height-left ">
          <!-- <el-scrollbar> -->
            <div class="flex-center " style="padding: 10px;">
              <xlDigital ></xlDigital>

              <!-- <AiChatDigital style="position: absolute;top: 223px;left:25px" :data="applicationForm" :appId="applicationForm?.id"></AiChatDigital> -->

            </div>
            <!-- <div class="flex-end mr-12">
              <el-button text>
                <el-icon><FullScreen /></el-icon>
              </el-button>
            </div> -->
          <!-- </el-scrollbar> -->
        </div>
      </el-col>
    </el-row>
  </LayoutContainer>
</template>

<script setup lang="ts">
// import type { ApplicationFormType } from '@/api/type/application'
import type { ApplicationFormType } from '@/api/type/application'
// import AiChatDigital from '@/components/ai-chatDigital/index.vue'
import { t } from '@/locales'
import useStore from '@/stores'
import { onMounted, ref } from 'vue'
import xlDigital from './xlDigital.vue'
const { application } = useStore()
defineOptions({ name: 'digitalChat' })
// @ts-ignore
const defaultPrompt = t('views.application.prompt.defaultPrompt', {
  data: '{data}',
  question: '{question}'
})
const loading = ref(false)
onMounted(() => {
  getDetail()
})
const applicationForm = ref<ApplicationFormType & { id: string }>({
  id: '',
  name: '',
  desc: '',
  model_id: '',
  multiple_rounds_dialogue: false,
  prologue: t('views.application.prompt.defaultPrologue'),
  dataset_id_list: [],
  dataset_setting: {
    top_n: 3,
    similarity: 0.6,
    max_paragraph_char_number: 5000,
    search_mode: 'embedding',
    no_references_setting: {
      status: 'ai_questioning',
      value: '{question}'
    }
  },
  model_setting: {
    prompt: defaultPrompt
  },
  problem_optimization: false,
  type: 'SIMPLE'
})
const applicationId = ref('01eafd71-5ddb-11ef-871a-dc7196811e7d')
function getDetail() {
  application.asyncGetApplicationDetail(applicationId.value, loading).then((res: any) => {
    applicationForm.value = res.data
    applicationForm.value.model_id = res.data.model
  })
}
</script>

<style lang="scss" scoped>
.create-application {
  .relate-dataset-card {
    color: var(--app-text-color);
  }
  .dialog-bg {
    border-radius: 8px;
    background: var(--dialog-bg-gradient-color);
    overflow: hidden;
    box-sizing: border-box;
  }
  .scrollbar-height-left {
    height: calc(var(--app-main-height) - 64px);
  }
  .scrollbar-height {
    height: calc(var(--app-main-height) - 160px);
  }
}
.flex-end {
  display: flex;
  align-items: center; /* 如果需要，垂直居中对齐 */
  justify-content: end;
}

</style>
