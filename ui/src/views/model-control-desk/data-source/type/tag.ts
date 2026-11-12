interface Tag {
    key: string
    value: string 
    disabled?: boolean // 这里添加 disabled 属性的类型定义
    custom?: boolean; // 标记是否为自定义标签
  }
  const selectTagsList = [
    {
        parentKey: '200',
        parentValue: '大模型',
      childs: [
        { key: '201', value: '预训练' },
        { key: '202', value: '微调' },
        { key: '203', value: '多模态' },
        { key: '204', value: '提示词工程' },
        { key: '205', value: '强化学习' }
      ]
    },
    {
        parentKey: '300',
        parentValue: '模型能力评估',
      childs: [
        { key: '301', value: '语言理解' },
        { key: '302', value: '检索增强' },
        { key: '303', value: '逻辑推理' },
        { key: '304', value: '智能体' }
      ]
    },
    {
        parentKey: '400',
        parentValue: '自然语言处理',
      childs: [
        { key: '401', value: '舆情分析' },
        { key: '402', value: '智能问答' },
        { key: '403', value: '文本审核' },
        { key: '404', value: '观点抽取' },
        { key: '405', value: '情感分析' },
        { key: '406', value: '文本生成' }
      ]
    }
]
  const tagsList = [
    {
      parentKey: '100',
      parentValue:'数据源类型',
      childs: [
        // { key: '全部数据源', value: '全部数据源' },
        { key: '0', value: '文件型数据源' },
        { key: '1', value: '数据库数据源' },
        { key: '2', value: '知识图谱数据源', disabled: true }
      ]
    },
    ...selectTagsList
  ]
  
  export { type Tag, tagsList, selectTagsList}
  