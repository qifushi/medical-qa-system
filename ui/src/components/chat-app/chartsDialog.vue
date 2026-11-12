<template>
  <el-dialog title="图表charts" v-model="chartsDialogVisible" class="chartsTitle" width="60%">
    <div class="export_fle_right mb-8 mt-8">

    </div>
    <div ref="chartRef" style="width: 600px; height: 400px;"></div>
  </el-dialog>
</template>

<script lang="ts" setup>
import Papa from 'papaparse';
import { ref, onMounted, onUnmounted, watchEffect, nextTick } from 'vue';
import * as echarts from 'echarts';
import { marked } from 'marked';

interface HeaderMap {
  [key: string]: any;
}

const chartsDialogVisible = ref(false);
const allData = ref([]);
const chatApplicationId = ref('');
const chatopenId = ref('');
const chatData = ref('');
const chartsType = ref('');
const chartsHeaders = ref([])

// 定义图表容器的引用
const chartRef = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

// 初始化图表
const initChart = async () => {
  if (!chartRef.value) return;

  // 使用 nextTick 确保 DOM 更新完毕后再初始化图表
  await nextTick();

  // 从 chatData 中解析表格数据
  const parsedData = parseMarkdownTable(chatData.value);

  // 检查 parsedData 是否为 undefined 或为空数组
  if (!Array.isArray(parsedData) || parsedData.length === 0) {
    console.error('Parsed data is invalid or empty.');
    return;
  }

  // 基于准备好的DOM，初始化ECharts实例
  chartInstance = echarts.init(chartRef.value);

  // 指定图表的配置项和数据
  const optionPie = {
    title: {
      text: chartsHeaders.value[1],
    },
    tooltip: {
      // trigger: 'item'
    },
    // legend: {
    //   right: '5%',
    //   orient: 'vertical'
    // },
    series: [
      {
        name: chartsHeaders.value[1],
        type: 'pie',
        radius: ['35%', '75%'],
        data: parsedData,
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        // label: {
        //   show: false,
        //   position: 'center'
        // },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          },
          // label: {
          //   show: true,
          //   fontSize: 40,
          //   fontWeight: 'bold'
          // }
        },
        labelLine: {
          show: false
        },
      }
    ]
  };

  const optionBar = {
    title: {
      text: chartsHeaders.value[1]
    },
    tooltip: {},
    legend: {},
    xAxis: {  // 添加 xAxis 配置
        type: 'category',  // 分类轴
        data: parsedData.map(item => item.name).reverse()
    },
    yAxis: {  // 添加 yAxis 配置
        type: 'value'  // 数值轴
    },
    series: [
      {
        name: chartsHeaders.value[1],
        type: 'bar',
        radius: '75%',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(180, 180, 180, 0.2)'
        },
        data: parsedData.map(item => item.value).reverse(),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  // 使用刚指定的配置项和数据显示图表。
  if (chartsType.value == 'bar') {
    chartInstance.setOption(optionBar);
  } else {
    chartInstance.setOption(optionPie);
  }
    
};

// 清理图表实例
const disposeChart = () => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
};

// 使用 watchEffect 来确保图表在每次对话框显示时都能正确初始化
watchEffect(() => {
  if (chartsDialogVisible.value) {
    initChart();
  } else {
    disposeChart();
  }
});

// 解析 Markdown 表格数据
const parseMarkdownTable = (markdownString: string): echarts.SeriesOption['data'] => {
  try {
    const html = marked.parse(markdownString);
    const parser = new DOMParser();
    const doc = parser.parseFromString(html as string, 'text/html');
    const tables = doc.getElementsByTagName('table');

    if (tables.length > 0) {
      const table = tables[0];
      const rows = table.getElementsByTagName('tr');

      const headerRow = rows[0];
      const headers = Array.from(headerRow.children).map((cell) => cell.textContent?.trim());
      chartsHeaders.value = headers as []

      const data = Array.from(rows).slice(1).map((row) => {
        const cells = Array.from(row.children).map((cell) => cell.textContent?.trim());
        const label = cells[0];
        const value = parseFloat(cells[1] || '0');
        return {
          name: label,
          value: value
        };
      });

      return data;
    }
  } catch (error) {
    console.error('Error parsing markdown table:', error);
  }

  return [];
};

// 导出 CSV
const exportCsv = () => {
  console.log('执行了');
  let headerMap: HeaderMap = {};

  // 从映射中提取CSV表头
  let tableHeader = Object.values(headerMap);
  console.log(tableHeader, 'tableHeader');

  // 转换数据为CSV格式，使用映射的表头名称
  var csv = Papa.unparse({
    fields: tableHeader, // 使用映射后的表头
    data: allData.value.map((item) => {
      // 根据映射关系转换每条数据记录
      return Object.keys(headerMap).map((header) => item[header]);
    })
  });

  // 创建Blob对象
  let content = new Blob([csv]);

  // 生成下载链接
  let urlObject = window.URL || window.webkitURL || window;
  let url = urlObject.createObjectURL(content);

  // 创建下载链接DOM元素
  let el = document.createElement('a');
  el.href = url;
  el.download = 'exported_file.csv';

  // 触发点击下载
  el.click();

  // 移除链接释放资源
  urlObject.revokeObjectURL(url);
};

const open = (applicationId: string, chatId: string, data: any, type: string) => {
  chartsDialogVisible.value = true;
  chatApplicationId.value = applicationId;
  chatopenId.value = chatId;
  chatData.value = data?.answer_text ?? '';
  chartsType.value = type
};

defineExpose({ open });

</script>

<style lang="scss" scoped>
.pagination_css {
  margin-top: 10px;
  justify-content: flex-end;
}
.export_fle_right {
  display: flex;
  justify-content: flex-end;
}
.chartsTitle {
  padding: 0 0 var(--el-dialog-padding-primary) 0;
  .el-dialog__header {
    padding: 12px var(--el-dialog-padding-primary);
    background: #2f99ff;
    .el-dialog__title {
      color: #fff;
    }
  }
  .el-dialog__body {
    padding: 0 var(--el-dialog-padding-primary) var(--el-dialog-padding-primary);
  }
  .el-dialog__close {
    color: #fff;
  }
  .el-dialog__headerbtn {
    top: 0;
  }
}
</style>