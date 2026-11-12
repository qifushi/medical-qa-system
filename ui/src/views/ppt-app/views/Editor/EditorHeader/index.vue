<template>
  <div class="editor-header" v-bind="$attrs">
    <div class="left">
      <Popover trigger="click" placement="bottom-start" v-model:value="mainMenuVisible">
        <template #content>
          <div class="main-menu">
            <!-- <div class="ai-menu" @click="openAIPPTDialog(); mainMenuVisible = false">
              <div class="icon"><IconClick theme="two-tone" :fill="['#ffc158', '#fff']" /></div>
              <div class="aippt-content">
                <div class="aippt"><span>AIPPT</span></div>
                <div class="aippt-subtitle">输入一句话，智能生成演示文稿</div>
              </div>
            </div> -->
          </div>
          <!-- <Divider :margin="10" /> -->
          <div class="import-section">
            <div class="import-label">导入文件</div>
            <div class="import-grid">
              <FileInput class="import-block"
                accept="application/vnd.openxmlformats-officedocument.presentationml.presentation" @change="
                  (files) => {
                    importPPTXFile(files);
                    mainMenuVisible = false
                  }
                ">
                <span class="icon">
                  <IconFilePdf theme="multi-color" :fill="['#333', '#d14424', '#fff']" />
                </span>
                <span class="label">PPTX</span>
                <!-- <span class="sub-label">（仅供测试）</span> -->
              </FileInput>
              <FileInput v-hasPermission="new Role('ADMIN')" class="import-block" accept=".json" @change="files => {
                importJSON(files)
                mainMenuVisible = false
              }">
                <span class="icon">
                  <IconFileJpg theme="multi-color" :fill="['#333', '#d14424', '#fff']" />
                </span>
                <span class="label">JSON</span>
                <!-- <span class="sub-label">（仅供测试）</span> -->
              </FileInput>
              <FileInput v-hasPermission="new Role('ADMIN')" class="import-block" accept=".pptist" @change="files => {
                importSpecificFile(files)
                mainMenuVisible = false
              }">
                <span class="icon">
                  <IconNotes theme="multi-color" :fill="['#333', '#d14424', '#fff']" />
                </span>
                <span class="label">PPTIST</span>
                <span class="sub-label">（WEB格式）</span>
              </FileInput>
            </div>
          </div>
          <Divider :margin="10" />
          <PopoverMenuItem class="popover-menu-item" @click="setDialogForExport('pptx')">
            <IconDownload class="icon" /> 导出文件
          </PopoverMenuItem>
          <Divider :margin="10" />
          <PopoverMenuItem class="popover-menu-item" @click="
              resetSlides();
              mainMenuVisible = false
            ">
            <IconRefresh class="icon" /> 重置幻灯片
          </PopoverMenuItem>
          <PopoverMenuItem v-hasPermission="new Role('ADMIN')" class="popover-menu-item" @click="
              openMarkupPanel();
              mainMenuVisible = false
            ">
            <IconMark class="icon" /> 幻灯片类型标注
          </PopoverMenuItem>
          <PopoverMenuItem class="popover-menu-item" @click="
              mainMenuVisible = false;
              hotkeyDrawerVisible = true
            ">
            <IconCommand class="icon" /> 快捷操作
          </PopoverMenuItem>
          <!-- <PopoverMenuItem class="popover-menu-item" @click="goLink('https://github.com/pipipi-pikachu/PPTist/issues')"><IconComment class="icon" /> 意见反馈</PopoverMenuItem>
          <PopoverMenuItem class="popover-menu-item" @click="goLink('https://github.com/pipipi-pikachu/PPTist/blob/master/doc/Q&A.md')"><IconHelpcenter class="icon" /> 常见问题</PopoverMenuItem> -->
          <PopoverMenuItem class="popover-menu-item" v-tooltip="'Copyright 2020-PRESENT pipipi-pikachu'">
            <IconHelpcenter class="icon" /> 关于
          </PopoverMenuItem>
          <PopoverMenuItem class="popover-menu-item" @click="handleRest">
            <IconLogout class="icon" /> 重新AI生成PPT
          </PopoverMenuItem>
          <!-- <a class="github-link" v-tooltip="'Copyright 2020-PRESENT pipipi-pikachu'" href="https://github.com/pipipi-pikachu/PPTist" target="_blank">
        <div class="menu-item"><IconGithub class="icon" /></div>
      </a> -->
        </template>
        <div class="menu-item">
          <IconHamburgerButton class="icon" />
        </div>
      </Popover>
      <div class="title-logo" @click="goPptIndex">
        智能PPT
      </div>
      <div class="title">
        <Input class="title-input" ref="titleInputRef" v-model:value="titleValue" @blur="handleUpdateTitle()"
          v-if="editingTitle"></Input>
        <div class="title-text" @click="startEditTitle()" :title="title" v-else>{{ title }}</div>
      </div>
    </div>

    <div class="right">

      <div class="group-menu-item">

        <div class="menu-item" v-tooltip="'幻灯片放映（F5）'" @click="enterScreening()">
          <IconPpt class="icon" />
        </div>
        <Popover trigger="click" center>
          <template #content>
            <PopoverMenuItem class="popover-menu-item" @click="enterScreeningFromStart()">
              <IconSlideTwo class="icon" /> 从头开始
            </PopoverMenuItem>
            <PopoverMenuItem class="popover-menu-item" @click="enterScreening()">
              <IconPpt class="icon" /> 从当前页开始
            </PopoverMenuItem>
          </template>
          <div class="arrow-btn">
            <IconDown class="arrow" />
          </div>
        </Popover>
      </div>
      <!-- <div class="menu-item" v-tooltip="'AI生成PPT'" @click="openAIPPTDialog(); mainMenuVisible = false">
        <span class="text ai">AI</span>
      </div> -->
      <div class="menu-item template-switch-container" v-tooltip="'更换模板'" @click="showAIPPTDialog = true">
        <img src="@pptApp/assets/imgs/switchTem.svg" alt="" width="18px">
        <div v-if="showTemplateTooltip" class="animated-tooltip" :class="{ 'fade-out': !showTemplateTooltip }">
          模版不满意？点击更换模板再修改PPT内容
          <div class="tooltip-arrow"></div>
        </div>
      </div>
      <div class="menu-item" v-tooltip="'回到大纲'" @click="goOutline()">
        <img src="@pptApp/assets/imgs/backdoc.svg" alt="" width="18px">
      </div>
      <div class="menu-item" v-tooltip="'导出'" @click="setDialogForExport('pptx')">
        <IconDownload class="icon" />
      </div>
      <div class="menu-item" v-tooltip="'重新AI生成PPT'" @click="
        handleRest
        ">
        <IconLogout class="icon" />
      </div>
      <!-- <a class="github-link" v-tooltip="'Copyright 2020-PRESENT pipipi-pikachu'" href="https://github.com/pipipi-pikachu/PPTist" target="_blank">
        <div class="menu-item"><IconGithub class="icon" /></div>
      </a> -->
    </div>

    <Drawer :width="320" v-model:visible="hotkeyDrawerVisible" placement="right">
      <HotkeyDoc />
      <template v-slot:title>快捷操作</template>
    </Drawer>

    <FullscreenSpin :loading="exporting" tip="正在导入..." />
  </div>
  <Modal :visible="showAIPPTDialog" :width="720" :closeOnClickMask="false" :closeOnEsc="false" closeButton
    @closed="closeAIPPTDialog()">
    <div class="aiPPT-modal">
      <div class="header">
        <span class="title">智能PPT</span>
        <span class="subtite">从下方挑选合适的模板，进行替换</span>
      </div>
      <TemplateSelector :templates="templates" v-model:selectedTemplate="selectedTemplate" style="height: 500px;"/>
      <div class="btns">
        <Button class="btn" type="primary" @click="switchTemplate()">替换</Button>
        <Button class="btn" @click="closeAIPPTDialog()">取消</Button>
      </div>
    </div>
  </Modal>
</template>

<script lang="ts" setup>
import { ElMessageBox } from 'element-plus'
import mssage from '@/views/ppt-app/components/Message.vue'
import useImport from '@pptApp/hooks/useImport'
import useScreening from '@pptApp/hooks/useScreening'
import useSlideHandler from '@pptApp/hooks/useSlideHandler'
import type { DialogForExportTypes } from '@pptApp/types/export'
import { storeToRefs } from 'pinia'
import { nextTick, ref, useTemplateRef } from 'vue'
import { useMainStore, useSlidesStore, usePPTLogStore, useOutLineStore } from '@pptApp/store'
import { Role } from '@/utils/permission/type'
import Divider from '@pptApp/components/Divider.vue'
import Drawer from '@pptApp/components/Drawer.vue'
import FileInput from '@pptApp/components/FileInput.vue'
import FullscreenSpin from '@pptApp/components/FullscreenSpin.vue'
import Input from '@pptApp/components/Input.vue'
import Popover from '@pptApp/components/Popover.vue'
import PopoverMenuItem from '@pptApp/components/PopoverMenuItem.vue'
import HotkeyDoc from './HotkeyDoc.vue'
import api from '@pptApp/services'
import useAIPPT from '@pptApp/hooks/useAIPPT'
import type { Slide, SlideTheme } from '@pptApp/types/slides'
import { useRouter } from 'vue-router'
import Modal from '@pptApp/components/Modal.vue'
import TemplateSelector from '@pptApp/views/components/templateSelector/index.vue'
import Button from '@pptApp/components/Button.vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const { AIPPT } = useAIPPT()

const showAIPPTDialog = ref(false)
const mainStore = useMainStore()
const slidesStore = useSlidesStore()
const { title, contentSlides, slideIndex, templates } = storeToRefs(slidesStore)
const { showTemplateTooltip } = storeToRefs(mainStore)
const { enterScreening, enterScreeningFromStart } = useScreening()
const { importSpecificFile, importPPTXFile, importJSON, exporting } = useImport()
const { resetSlides } = useSlideHandler()

const pptStore = usePPTLogStore()
const mainMenuVisible = ref(false)
const hotkeyDrawerVisible = ref(false)
const editingTitle = ref(false)
const titleValue = ref('')
const titleInputRef = useTemplateRef<InstanceType<typeof Input>>('titleInputRef')
const selectedTemplate = ref('template_1')
const outLineStore = useOutLineStore()

const closeAIPPTDialog = () => {
  showAIPPTDialog.value = false
}
const startEditTitle = () => {
  titleValue.value = title.value
  editingTitle.value = true
  nextTick(() => titleInputRef.value?.focus())
}

const handleUpdateTitle = () => {
  slidesStore.setTitle(titleValue.value)
  editingTitle.value = false
}

const goLink = (url: string) => {
  window.open(url)
  mainMenuVisible.value = false
}

const setDialogForExport = (type: DialogForExportTypes) => {
  mainStore.setDialogForExport(type)
  mainMenuVisible.value = false
}

const openMarkupPanel = () => {
  mainStore.setMarkupPanelState(true)
}

const openAIPPTDialog = () => {
  mainStore.setAIPPTDialogState(true)
}
const goPptIndex = () => {
  router.push({ name: 'createAippt' })
}
const handleRest = () => {
  pptStore.restLog()
  router.push('/createAippt')
}

const goOutline = () => {
  ElMessageBox.confirm('离开当前页面将丢失未保存的编辑内容，是否确认返回大纲？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    if(!outLineStore.outline){
      ElMessage.warning('未找到大纲信息，请重新创建PPT大纲')

      router.push({
        name: 'createAippt',
      })
    }else {
      // 清理当前编辑状态
      mainStore.setActiveElementIdList([])

      // 跳转到创建PPT页面的大纲步骤
      router.push({
        name: 'createAippt',
        query: { step: 'outline' }
      })
    }
  
  }).catch(() => {
    console.log('取消返回大纲');
  })
}
const switchTemplate = async() => {
  ElMessageBox.confirm('更换模板会丢失编辑的内容，是否确认更换？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async() => {
    if (!outLineStore.outline) {
      ElMessage.warning('未找到PPT内容，请重新生成')

      router.push({
        name: 'createAippt',
      })
    } else {
      const templateData = await api.getMockData(selectedTemplate.value)
      const templateSlides: Slide[] = templateData.slides
      const templateTheme: SlideTheme = templateData.theme
      const currentSlideindex = slideIndex.value // 保存换模板前选中的幻灯片索引
      resetSlides()
      AIPPT(templateSlides, contentSlides.value)
      slidesStore.setTheme(templateTheme)
      await nextTick()
      mainStore.setActiveElementIdList([]) // 清除选中状态
      slidesStore.updateSlideIndex(currentSlideindex) // 更新到换模板前幻灯片所在页
    }
  }).catch(() => {
    console.log('取消更换');
  }).finally(() => {
    closeAIPPTDialog()
  })
}
</script>

<style lang="scss" scoped>
.editor-header {
  background-color: #fff;
  user-select: none;
  border-bottom: 1px solid $borderColor;
  display: flex;
  justify-content: space-between;
  padding: 0 8px;
  
}
.left,
.right {
  display: flex;
  justify-content: center;
  align-items: center;
}
.menu-item {
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  padding: 0 10px;
  border-radius: $borderRadius;
  cursor: pointer;

  .icon {
    font-size: 18px;
    color: #666;
  }
  .text {
    width: 18px;
    text-align: center;
    font-size: 17px;
  }
  .ai {
    background: linear-gradient(270deg, #d897fd, #33bcfc);
    background-clip: text;
    color: transparent;
    font-weight: 700;
  }

  &:hover {
    background-color: #f1f1f1;
  }
}
.popover-menu-item {
  display: flex;
  padding: 8px 10px;

  .icon {
    font-size: 18px;
    margin-right: 12px;
  }
}
.main-menu {
  width: 300px;
}
.ai-menu {
  background: linear-gradient(270deg, #f8edff, #d4f1ff);
  color: $themeColor;
  border-radius: $borderRadius;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  cursor: pointer;

  .icon {
    font-size: 22px;
    margin-right: 16px;
  }
  .aippt-content {
    display: flex;
    flex-direction: column;
  }
  .aippt {
    font-weight: 700;
    font-size: 16px;

    span {
      background: linear-gradient(270deg, #d897fd, #33bcfc);
      background-clip: text;
      color: transparent;
    }
  }
  .aippt-subtitle {
    font-size: 12px;
    color: #777;
    margin-top: 5px;
  }
}

.import-section {
  padding: 5px 0;

  .import-label {
    font-size: 12px;
    color: #999;
    margin-bottom: 6px;
  }
  .import-grid {
    display: flex;
    gap: 8px;
    justify-content: space-between;
  }
  .import-block {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px 8px;
    border-radius: $borderRadius;
    border: 1px solid $borderColor;
    transition: background-color 0.2s;
    cursor: pointer;

    &:hover {
      background-color: #f1f1f1;
    }
    .icon {
      font-size: 24px;
      margin-bottom: 2px;
    }
    .label {
      font-size: 12px;
      text-align: center;
    }
    .sub-label {
      font-size: 10px;
      color: #999;
    }
  }
}

.group-menu-item {
  height: 30px;
  display: flex;
  margin: 0 8px;
  padding: 0 2px;
  border-radius: $borderRadius;

  &:hover {
    background-color: #f1f1f1;
  }

  .menu-item {
    padding: 0 3px;
  }
  .arrow-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
}
.title-logo {
  font-weight: 700;
  font-size: 20px;
  margin-right: 8px;
  background: linear-gradient(270deg, #d897fd, #33bcfc);
  background-clip: text;
  color: transparent;
  cursor: pointer;
}
.title {
  height: 30px;
  margin-left: 2px;
  font-size: 13px;

  .title-input {
    width: 200px;
    height: 100%;
    padding-left: 0;
    padding-right: 0;

    ::v-deep(input) {
      height: 28px;
      line-height: 28px;
    }
  }
  .title-text {
    min-width: 20px;
    max-width: 400px;
    line-height: 30px;
    padding: 0 6px;
    border-radius: $borderRadius;
    cursor: pointer;

    @include ellipsis-oneline();

    &:hover {
      background-color: #f1f1f1;
    }
  }
}
.github-link {
  display: inline-block;
  height: 30px;
}
.template-switch-container {
  position: relative;
}

.animated-tooltip {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(270deg, #d897fd, #33bcfc);
  color: white;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: heartBeat 1.5s ease-in-out forwards;

  &.fade-out {
    animation: fadeOut 0.6s ease-out forwards;
  }

  .tooltip-arrow {
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid #d897fd;
  }
}

@keyframes heartBeat {
  0% {
    transform: translateX(-50%) scale(1);
  }
  14% {
    transform: translateX(-50%) scale(1.2);
  }
  28% {
    transform: translateX(-50%) scale(1);
  }
  42% {
    transform: translateX(-50%) scale(1.2);
  }
  70% {
    transform: translateX(-50%) scale(1);
  }
}


@keyframes fadeOut {
  0% {
    opacity: 1;
    transform: translateX(-50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) scale(0.7);
  }
}
.fade-out {
  opacity: 0;
}
.aiPPT-modal{
.header {
  margin-bottom: 20px;

  .title {
    font-weight: 700;
    font-size: 20px;
    margin-right: 8px;
    background: linear-gradient(270deg, #d897fd, #33bcfc);
    background-clip: text;
    color: transparent;
    vertical-align: text-bottom;
    line-height: 1.1;
  }

  .subtite {
    color: #888;
    font-size: 13px;
  }
  
}
.btns {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;

  .btn {
    width: 120px;
    margin: 0 5px;
  }
}
}
</style>
<style>
.modal{
  /* 解决el-message的层级问题 */
  z-index: 2000 !important;  
}
</style>