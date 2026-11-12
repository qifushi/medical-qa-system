"""生成论文所需的全部实验图表与系统示意图。

输出目录: 论文/实验数据/figures/
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---------------- 字体 ----------------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / '论文' / '实验数据' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)
EVAL_FILE = ROOT / '论文' / '实验数据' / 'retrieval_eval.json'

with open(EVAL_FILE, encoding='utf-8') as f:
    EVAL = json.load(f)

METHOD_LABELS = {'substring': '子串检索', 'lexical': '词法检索',
                 'semantic': '语义检索', 'hybrid': '混合检索'}
METHOD_COLORS = {'substring': '#9AA0A6', 'lexical': '#4C78A8',
                 'semantic': '#F58518', 'hybrid': '#E45756'}


# ======================================================
# 图 6-1 & 6-2：主实验对比（Recall/MRR/nDCG grouped bar）
# ======================================================
def plot_main_experiment():
    METRICS = ['recall@1', 'recall@5', 'recall@10', 'mrr@10', 'ndcg@10']
    METRIC_LABELS = ['Recall@1', 'Recall@5', 'Recall@10', 'MRR@10', 'nDCG@10']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=150)

    for idx, (set_name, title) in enumerate(
        [('verbatim', '(a) 原始问句（verbatim, N=120）'),
         ('paraphrase', '(b) 改写问句（paraphrase, N=60）')]):
        ax = axes[idx]
        data = EVAL['sets'][set_name]['overall']
        methods = ['substring', 'lexical', 'semantic', 'hybrid']
        x = np.arange(len(METRICS))
        width = 0.18

        for j, m in enumerate(methods):
            vals = [data[m][metric] for metric in METRICS]
            bars = ax.bar(x + (j - 1.5) * width, vals, width,
                          label=METHOD_LABELS[m], color=METHOD_COLORS[m],
                          edgecolor='white', linewidth=0.8)
            # paraphrase 的 substring 全 0 不加标签，避免遮挡
            if set_name == 'paraphrase' and m == 'substring':
                continue
            for bar, v in zip(bars, vals):
                if v > 0.02:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.01,
                            f'{v:.2f}', ha='center', va='bottom', fontsize=7)

        ax.set_title(title, fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(METRIC_LABELS, fontsize=9)
        ax.set_ylim(0, 1.08)
        ax.set_ylabel('指标值', fontsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        if idx == 1:
            ax.legend(loc='upper right', fontsize=8, framealpha=0.8)
        # 标记全零的子串检索
        if set_name == 'paraphrase':
            ax.annotate('子串检索\n全部指标为 0',
                        xy=(2, 0.05), fontsize=8, color='#7f7f7f',
                        ha='center', style='italic')

    fig.suptitle('图 6-1  四方法在两套评估集上的检索指标对比', fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig6-1_main_experiment.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig6-1_main_experiment.png')


# ======================================================
# 图 6-3：延迟对比 + Miss rate
# ======================================================
def plot_latency():
    sets = ['verbatim', 'paraphrase']
    set_titles = ['原始问句', '改写问句']
    methods = ['substring', 'lexical', 'semantic', 'hybrid']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=150)

    # 左：延迟（两集平均）
    latencies = []
    for m in methods:
        lat = np.mean([EVAL['sets'][s]['overall'][m]['latency_ms'] for s in sets])
        latencies.append(lat)
    bars = ax1.bar([METHOD_LABELS[m] for m in methods], latencies,
                   color=[METHOD_COLORS[m] for m in methods],
                   edgecolor='white', width=0.55)
    for bar, v in zip(bars, latencies):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1.5,
                 f'{v:.1f} ms', ha='center', fontsize=9, fontweight='bold')
    ax1.set_title('(a) 四方法单库平均检索延迟', fontsize=10)
    ax1.set_ylabel('毫秒 (ms)', fontsize=9)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.set_ylim(0, max(latencies) * 1.25)

    # 右：Miss rate 对比（verbatim vs paraphrase）
    x = np.arange(len(methods))
    w = 0.3
    for j, (sname, slabel) in enumerate(zip(sets, set_titles)):
        misses = [EVAL['sets'][sname]['overall'][m]['miss'] for m in methods]
        ax2.bar(x + (j - 0.5) * w, misses, w, label=slabel,
                color='#4C78A8' if j == 0 else '#E45756',
                edgecolor='white')
        for xv, v in zip(x + (j - 0.5) * w, misses):
            if v > 0.005:
                ax2.text(xv, v + 0.01, f'{v:.3f}',
                         ha='center', fontsize=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels([METHOD_LABELS[m] for m in methods], fontsize=9)
    ax2.set_title('(b) 两种场景下的 Miss 率对比', fontsize=10)
    ax2.set_ylabel('Miss rate', fontsize=9)
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=8, loc='upper left')
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    fig.suptitle('图 6-2  延迟与 Miss 率分析', fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig6-2_latency_miss.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig6-2_latency_miss.png')


# ======================================================
# 图 6-3：权重敏感性（硬编码 tune_weights 已跑结果，
#         与论文 6.5 节表格一致）
# ======================================================
def plot_weight_sensitivity():
    # name: (R@1, R@5, R@10, MRR, nDCG) × 2 集
    DATA = {
        'A 0.45/0.35/0.20': {'verb': (0.7833, 0.9750, 0.9833, 0.8651, 0.8948),
                              'para': (0.4167, 0.6333, 0.6833, 0.5150, 0.5565)},
        'B 0.60/0.10/0.30': {'verb': (0.8750, 0.9833, 0.9917, 0.9241, 0.9412),
                              'para': (0.4833, 0.7833, 0.8167, 0.5939, 0.6483)},
        'C 0.65/0.05/0.30': {'verb': (0.8917, 0.9833, 0.9917, 0.9338, 0.9484),
                              'para': (0.4500, 0.7667, 0.8167, 0.5767, 0.6355)},
        'D 0.70/0.00/0.30': {'verb': (0.8750, 0.9833, 0.9917, 0.9271, 0.9436),
                              'para': (0.4667, 0.7667, 0.8333, 0.5832, 0.6437)},
        'E 0.55/0.15/0.30': {'verb': (0.8667, 0.9833, 0.9917, 0.9203, 0.9383),
                              'para': (0.5000, 0.7500, 0.8167, 0.5965, 0.6497)},
        'F 0.50/0.25/0.25': {'verb': (0.8250, 0.9833, 0.9833, 0.8954, 0.9179),
                              'para': (0.5000, 0.6833, 0.7833, 0.5770, 0.6256)},
    }
    schemes = list(DATA.keys())
    verb_r1 = [DATA[s]['verb'][0] for s in schemes]
    verb_r5 = [DATA[s]['verb'][1] for s in schemes]
    para_r1 = [DATA[s]['para'][0] for s in schemes]
    para_r5 = [DATA[s]['para'][1] for s in schemes]

    labels = [s.split(' ', 1)[1] for s in schemes]
    x = np.arange(len(schemes))

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=150)
    ax2 = ax1.twinx()

    ax1.plot(x, verb_r1, '-o', color='#4C78A8', label='verbatim Recall@1', markersize=7, linewidth=2)
    ax1.plot(x, verb_r5, '--s', color='#4C78A8', label='verbatim Recall@5', markersize=5, linewidth=1.5, alpha=0.7)
    ax2.plot(x, para_r1, '-o', color='#E45756', label='paraphrase Recall@1', markersize=7, linewidth=2)
    ax2.plot(x, para_r5, '--s', color='#E45756', label='paraphrase Recall@5', markersize=5, linewidth=1.5, alpha=0.7)

    # 标记选定的方案 B
    ax1.annotate('★ 选定方案 B\n(0.60/0.10/0.30)',
                 xy=(1, verb_r1[1]), xytext=(1.3, 0.70),
                 fontsize=8, color='#1a1a1a',
                 arrowprops=dict(arrowstyle='->', color='#E45756', lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', fc='#fff3cd', ec='#e0a800'))

    for i, (v1, p1) in enumerate(zip(verb_r1, para_r1)):
        ax1.text(i, v1 + 0.008, f'{v1:.3f}', ha='center', fontsize=7, color='#4C78A8')
        ax2.text(i, p1 - 0.022, f'{p1:.3f}', ha='center', fontsize=7, color='#E45756')

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=8, ha='center')
    ax1.set_xlabel('权重方案', fontsize=10)
    ax1.set_ylabel('verbatim Recall', color='#4C78A8', fontsize=10)
    ax2.set_ylabel('paraphrase Recall', color='#E45756', fontsize=10)
    ax1.set_ylim(0.72, 1.02)
    ax2.set_ylim(0.30, 0.62)
    ax1.grid(alpha=0.3)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right', fontsize=8)

    plt.title('图 6-3  融合权重对 Recall 的影响（双 Y 轴）', fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig6-3_weight_sensitivity.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig6-3_weight_sensitivity.png')


# ======================================================
# 图 6-5：分库结果（paraphrase Recall@1 对比）
# ======================================================
def plot_per_kb():
    kb_names = ['report_analysis', 'medicine_analysis', 'medical_service']
    kb_cn = ['报告分析', '药品分析', '就医助手']
    methods = ['substring', 'lexical', 'semantic', 'hybrid']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5), dpi=150)

    for idx, (set_name, title) in enumerate(
        [('verbatim', '(a) verbatim Recall@1'),
         ('paraphrase', '(b) paraphrase Recall@1')]):
        ax = ax1 if idx == 0 else ax2
        # 从 sets[set_name] 的按库结果读
        per_kb = EVAL['sets'][set_name].get('per_kb', {})
        x = np.arange(len(kb_names))
        width = 0.18
        for j, m in enumerate(methods):
            vals = []
            for kb in kb_names:
                try:
                    v = per_kb[kb][m]['recall@1']
                except KeyError:
                    # fallback: 如果 JSON 没有 per_kb 字段，用 overall 占位
                    v = EVAL['sets'][set_name]['overall'][m]['recall@1']
                vals.append(v)
            bars = ax.bar(x + (j - 1.5) * width, vals, width,
                          label=METHOD_LABELS[m], color=METHOD_COLORS[m],
                          edgecolor='white')
            for bar, v in zip(bars, vals):
                if v > 0.03 and v < 0.99:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.015,
                            f'{v:.2f}', ha='center', fontsize=7)

        ax.set_title(title, fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(kb_cn, fontsize=9)
        ax.set_ylim(0, 1.1)
        ax.set_ylabel('Recall@1', fontsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        if idx == 1:
            ax.legend(fontsize=8, loc='upper right')

    fig.suptitle('图 6-4  三个知识库上的 Recall@1 对比', fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig6-4_per_kb.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig6-4_per_kb.png')


# ======================================================
# 图 3-1：系统分层架构（框图）
# ======================================================
def draw_architecture():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    layers = [
        ('表现层  Vue 3 单页应用',   '#E45756', ['角色选择', '患者主界面', '报告/药品/就医', '医生工作台']),
        ('接口层  Django 4.2',       '#F58518', ['chat / reset_history', 'image_upload', 'file_upload']),
        ('业务层  对话编排',         '#F28E2B', ['多轮历史', '知识摘要', '文件解析/OCR', '提示词/深度思考']),
        ('检索层  混合检索',         '#E15759', ['TF-IDF 词法通道', 'LSA 语义通道', '实体覆盖通道', '加权融合 + 缓存']),
        ('知识层  三库 249,890 条',  '#76B7B2', ['report_analysis', 'medicine_analysis', 'medical_service']),
        ('模型层  Ollama + CMeKG + PaddleOCR', '#59A14F', ['qwen2.5vl:3b CPU', 'CMeKG 医学分词/实体', 'PP-OCRv6 扫描件']),
    ]

    box_w = 8.5
    box_h = 1.05
    start_y = 7.3
    step_y = 1.25
    for i, (title, color, items) in enumerate(layers):
        y = start_y - i * step_y
        rect = plt.Rectangle((0.75, y), box_w, box_h,
                             facecolor=color, alpha=0.18,
                             edgecolor=color, linewidth=1.8,
                             joinstyle='round')
        ax.add_patch(rect)
        ax.text(1.0, y + box_h - 0.30, title,
                fontsize=10.5, fontweight='bold', color='#333333')
        # items 横排
        n = len(items)
        for j, it in enumerate(items):
            ix = 1.0 + (box_w - 0.5) * (j + 0.5) / n
            ax.text(ix, y + 0.25, it,
                    fontsize=7.8, color='#444444',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white',
                              ec=color, alpha=0.9, lw=0.8))
        # 向下箭头
        if i < len(layers) - 1:
            ax.annotate('', xy=(5, y - 0.15), xytext=(5, y - 0.02),
                        arrowprops=dict(arrowstyle='->', color='#666666', lw=1.2))

    # 右上标注
    ax.text(9.6, 8.2, '用户浏览器', fontsize=8, ha='center', color='#888888', style='italic')
    ax.annotate('', xy=(5, 8.35), xytext=(9.2, 8.2),
                arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

    ax.set_title('图 3-1  系统分层架构', fontsize=13, fontweight='bold', pad=15)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig3-1_architecture.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig3-1_architecture.png')


# ======================================================
# 图 4-1：混合检索查询流程
# ======================================================
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    steps = [
        ('用户查询 q', '#4C78A8'),
        ('jieba 搜索模式分词', '#4C78A8'),
        ('TF-IDF 稀疏打分', '#E45756'),
        ('SVD 语义打分', '#F58518'),
        ('词法前60 ∪ 语义前60\n候选集 C', '#B279A2'),
        ('候选集上算覆盖率/名称加成', '#F28E2B'),
        ('归一化 + 加权融合\nS(e)=0.60L+0.10S+0.30C+0.10B', '#59A14F'),
        ('排序 → Top-k 返回', '#4C78A8'),
    ]

    box_w = 1.0
    gap = 0.22
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    start_x = (10 - total_w) / 2
    y = 2.0
    box_h = 1.4

    for i, (label, color) in enumerate(steps):
        x = start_x + i * (box_w + gap)
        rect = plt.Rectangle((x, y), box_w, box_h,
                             facecolor=color, alpha=0.20,
                             edgecolor=color, linewidth=1.5,
                             joinstyle='round')
        ax.add_patch(rect)
        # 多行文字居中
        lines = label.split('\n')
        nlines = len(lines)
        line_height = 0.16
        start_text_y = y + box_h / 2 + line_height * (nlines - 1) / 2
        for j, line in enumerate(lines):
            ax.text(x + box_w / 2, start_text_y - j * line_height,
                    line, fontsize=7.5, ha='center', va='center', color='#222222',
                    fontweight='bold' if i in (0, 7) else 'normal')

        # 箭头
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + box_w + gap * 0.3, y + box_h / 2),
                        xytext=(x + box_w, y + box_h / 2),
                        arrowprops=dict(arrowstyle='->', color='#666666', lw=1.1))

    ax.text(5, 4.6, '索引构建阶段（离线）', fontsize=10, ha='center', color='#76B7B2',
            fontweight='bold')
    ax.text(5, 3.65, '实体 → 拼接检索文本 → jieba 分词 → TF-IDF 矩阵 → TruncatedSVD(96) → pickle 缓存',
            fontsize=8, ha='center', color='#76B7B2', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', fc='#E7F5F0', ec='#76B7B2'))

    ax.set_title('图 4-1  混合检索离线构建与在线查询流程', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig4-1_pipeline.png', bbox_inches='tight')
    plt.close(fig)
    print('saved fig4-1_pipeline.png')


# ======================================================
# main
# ======================================================
if __name__ == '__main__':
    plot_main_experiment()
    plot_latency()
    try:
        plot_weight_sensitivity()
    except Exception as e:
        print(f'skip weight sensitivity: {e}')
    try:
        plot_per_kb()
    except Exception as e:
        print(f'skip per-kb: {e}')
    draw_architecture()
    draw_pipeline()
    print(f'\n所有图表已保存到 {FIG_DIR}')
