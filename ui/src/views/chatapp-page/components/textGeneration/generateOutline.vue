<template>
  <div class="chat-content">
    <el-collapse v-model="activeNames">
      <el-collapse-item
        v-for="(one_item, one_index) of outlineData.outline"
        :key="one_index"
        :name="one_index"
      >
        <template #title>
          <div class="el-collapse-item-title flex-between" @click.stop="showCollapse(one_index)">
            <div class="text">
              {{ `${one_index + 1} ${one_item.outline_one}` }}
              <div class="el-collapse-item-title-text">
                {{ one_item.outline_one_content }}
              </div>
            </div>
            <div class="right-button" >
              <div class="right-button-flex">
                <el-tooltip effect="dark" content="新增" placement="bottom">
                  <el-button
                    text
                    size="small"
                    icon="Plus"
                    @click.stop.prevent="addHandle(one_index)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip effect="dark" content="编辑" placement="bottom">
                  <el-button
                    text
                    size="small"
                    icon="Edit"
                    @click.stop.prevent="editHandle(one_index)"
                  ></el-button>
                </el-tooltip>
                <el-popconfirm
                  placement="bottom"
                  title="确定要删除该内容吗？删除后不可恢复!"
                  @confirm="deleteHandle(one_index)"
                >
                  <template #reference>
                    <el-button text size="small" icon="Delete"></el-button>
                  </template>
                </el-popconfirm>
              </div>
            </div>
          </div>
        </template>
        <div
          class="flex-between paragraph-content mb-12"
          v-for="(two_item, two_index) of one_item.outline_two"
        >
          <div>
            <h3>
              {{ `${one_index + 1}.${two_index + 1} ${two_item.outline_two_title}` }}
            </h3>
            <div style="font-size: 14px;">
              {{ two_item.outline_two_content }}
            </div>
          </div>
          <div class="right-button" >
            <div class="right-button-flex">
              <el-tooltip effect="dark" content="新增11" placement="bottom">
                <el-button
                  text
                  size="small"
                  icon="Plus"
                  @click.stop.prevent="addHandle(one_index, two_index)"
                ></el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="编辑" placement="bottom">
                <el-button
                  text
                  size="small"
                  icon="Edit"
                  @click.stop.prevent="editHandle(one_index, two_index)"
                ></el-button>
              </el-tooltip>
              <el-popconfirm
                placement="bottom"
                title="确定要删除该内容吗？删除后不可恢复!"
                @confirm="deleteHandle(one_index, two_index)"
              >
                <template #reference>
                  <el-button text size="small" icon="Delete"></el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>

  <!-- 编辑弹窗 -->
  <el-dialog title="编辑章节" v-model="editDialogVisible">
    <el-form
      ref="EditOutlineRef"
      :model="editOutlineForm"
      label-position="top"
      require-asterisk-position="right"
      @submit.prevent
      :rules="outlineRules"
    >
      <el-form-item label="标题" prop="title">
        <el-input v-model="editOutlineForm.title" placeholder="请输入章节标题" show-word-limit>
        </el-input>
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input
          type="textarea"
          v-model="editOutlineForm.content"
          placeholder="请输入章节内容"
          show-word-limit
          :rows="8"
        >
        </el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="editDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="editSubmit(EditOutlineRef)" :loading="loading">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 新增弹窗 -->
  <el-dialog title="新增章节" v-model="addDialogVisible">
    <el-form
      ref="AddOutlineRef"
      :model="addOutlineForm"
      label-position="top"
      require-asterisk-position="right"
      @submit.prevent
      :rules="addOutlineRules"
    >
      <el-form-item label="插入位置" prop="node">
        <el-radio-group v-model="addOutlineForm.node">
          <el-radio-button label="本节之前" value="before" />
          <el-radio-button label="本节之后" value="after" />
        </el-radio-group>
      </el-form-item>
      <template v-if="isOneOutline">
        <el-form-item label="一级章节标题" prop="oneTitle">
          <el-input v-model="addOutlineForm.oneTitle" placeholder="请输入章节标题" show-word-limit>
          </el-input>
        </el-form-item>
        <el-form-item label="一级章节内容" prop="oneContent">
          <el-input
            type="textarea"
            v-model="addOutlineForm.oneContent"
            placeholder="请输入章节内容"
            show-word-limit
            :rows="4"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="二级章节标题" prop="twoTitle">
          <el-input v-model="addOutlineForm.twoTitle" placeholder="请输入章节标题" show-word-limit>
          </el-input>
        </el-form-item>
        <el-form-item label="二级章节内容" prop="twoContent">
          <el-input
            type="textarea"
            v-model="addOutlineForm.twoContent"
            placeholder="请输入章节内容"
            show-word-limit
            :rows="4"
          >
          </el-input>
        </el-form-item>
      </template>
      <template v-else>
        <el-form-item label="章节标题" prop="twoTitle">
          <el-input v-model="addOutlineForm.twoTitle" placeholder="请输入章节标题" show-word-limit>
          </el-input>
        </el-form-item>
        <el-form-item label="章节内容" prop="twoContent">
          <el-input
            type="textarea"
            v-model="addOutlineForm.twoContent"
            placeholder="请输入章节内容"
            show-word-limit
            :rows="4"
          >
          </el-input>
        </el-form-item>
      </template>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="addDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="addSubmit(AddOutlineRef)" :loading="loading">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import type { FormInstance } from 'element-plus';
import { onMounted, reactive, ref, watch } from 'vue';

const props = defineProps({
  outlineData: {
    type: Object,
    default: () => {}
  }
})
const emit = defineEmits(['deleteOutline', 'addOutline', 'editOutline'])
// 新增弹窗-- start
const AddOutlineRef = ref()
const addDialogVisible = ref(false)
const addOutlineForm = ref({
  oneTitle: '',
  oneContent: '',
  twoTitle: '',
  twoContent: '',
  node: 'after'
})
const addOutlineRules = reactive({
  oneTitle: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  oneContent: [{ required: true, message: '请输入文章内容', trigger: 'blur' }],
  twoTitle: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  twoContent: [{ required: true, message: '请输入文章内容', trigger: 'blur' }]
})
const addOneOutlineIndex = ref() // 新增一级标题的索引
const addTwoOutlineIndex = ref() // 新增二级标题的索引
const isOneOutline = ref(false) // 是否是一级标题（新增）
// 新增操作
const addHandle = (one_index: number, two_index?: number) => {
  addDialogVisible.value = true
  // 清空表单数据
  AddOutlineRef.value && AddOutlineRef.value.resetFields()
  addOneOutlineIndex.value = one_index
  addTwoOutlineIndex.value = two_index
  console.log(one_index, two_index, 'two_indexs')

  if (two_index !== undefined && two_index !== null) {
    // 点击二级标题
    isOneOutline.value = false
  } else {
    // 点击一级标题
    isOneOutline.value = true
  }
}
const addSubmit = (formEl: FormInstance | undefined) => {
  // 验证表单
  if (!formEl) return
  AddOutlineRef.value.validate((valid: any) => {
    if (valid) {
      emit(
        'addOutline',
        addOutlineForm.value,
        isOneOutline.value,
        addOneOutlineIndex.value,
        addTwoOutlineIndex.value
      )

      addDialogVisible.value = false
    }
  })
}

// 新增弹窗-- end

// 编辑弹窗-- start
const outlineRules = reactive({
  title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入文章内容', trigger: 'blur' }]
})
const editDialogVisible = ref(false)
const editOutlineForm = ref({
  title: '',
  content: ''
})
const EditOutlineRef = ref()
const loading = ref(false)
const outlineEditIndex_one = ref<number>() // 需要修改的一级标题的索引
const outlineEditIndex_two = ref<number>() // 需要修改的二级标题的索引

// 编辑操作
const editHandle = (outline_one_index: number, outline_two_index?: number) => {
  console.log(outline_one_index, outline_two_index, 'editIndex')
  editDialogVisible.value = true
  // 保存索引，在点击提交的时候赋值
  outlineEditIndex_one.value = outline_one_index
  outlineEditIndex_two.value = outline_two_index
  let outlineArr = props.outlineData.outline
  // 数据回显
  if (outline_two_index !== undefined && outline_two_index !== null) {
    // 二级标题
    editOutlineForm.value = {
      title: outlineArr[outline_one_index].outline_two[outline_two_index].outline_two_title,
      content: outlineArr[outline_one_index].outline_two[outline_two_index].outline_two_content
    }
  } else {
    // 一级标题
    editOutlineForm.value = {
      title: outlineArr[outline_one_index].outline_one,
      content: outlineArr[outline_one_index].outline_one_content
    }
  }
}

const editSubmit = (formEl: FormInstance | undefined) => {
  console.log(formEl, 'el')
  // 验证表单
  if (!formEl) return
  let outlineArr = props.outlineData.outline
  // 验证表单
  EditOutlineRef.value.validate((valid: any) => {
    if (valid) {
      emit(
        'editOutline',
        editOutlineForm.value,
        outlineEditIndex_one.value,
        outlineEditIndex_two.value
      )
      editDialogVisible.value = false
    }
  })
}

// 编辑弹窗-- end

// 删除操作

const deleteHandle = (outline_one_index: number, outline_two_index?: number) => {
  emit('deleteOutline', outline_one_index, outline_two_index)
}

const activeNames = ref<any>([])

function showCollapse(index: number) {
  console.log(index, 'aaa')
}
onMounted(() => {
  // 返回大纲时，默认展开
  props.outlineData.outline && props.outlineData.outline.forEach((item: any, index: number) => {
      activeNames.value.push(index)
    })
}),
watch(
  () => props.outlineData,
  (newValue: any, oldValue: any) => {
    newValue.outline.forEach((item: any, index: number) => {
      console.log(item, 'index,', index)
      activeNames.value.push(index)
    })
    console.log(newValue, oldValue, 'newValue')
  },
  { deep: true }
)
</script>
<style lang="scss" scoped>
.dialog-bg {
  border-radius: 8px;
  // background: var(--dialog-bg-gradient-color);
  background: #fff;
  overflow: hidden;
  box-sizing: border-box;
}

.chat-content {
  padding: 0 24px 24px 24px;
}

.el-collapse-item-title {
  width: 96%;
  text-align: left;

  .el-collapse-item-title-text {
    font-weight: 500;
    font-size: 14px;
    margin-top: 8px;
  }

  .text {
    flex: 1;
    font-weight: bold;
    font-size: 18px;
  }

  &:hover {
    background-color: #f0f0f0;
  }
}

.right-button {
  width: 160px;
  margin-right: 10px;

  .right-button-flex {
    display: flex;
    justify-content: end;
    align-items: center;
  }
}

:deep(.el-collapse-item__arrow) {
  flex: 1 0 auto;
  order: -1;
}

:deep(.el-collapse-item__header) {
  height: auto;
  line-height: 1.5;
  margin: 10px 0;
}

.paragraph-content {
  margin-left: 4%;

  &:hover {
    background-color: #f0f0f0;
  }
}
:deep(.el-collapse) {
  border: none;
}
</style>
