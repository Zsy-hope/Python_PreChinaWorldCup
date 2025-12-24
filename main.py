import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def calculate_worldcup_probability():
    """
    基于多因素的综合分析预测国足2030年进军世界杯概率（含图表）
    """
    print("=" * 60)
    print("2030年国足世界杯出线概率分析报告")
    print("=" * 60)

    # ========== 1. 基础参数设置 ==========
    asia_slots = 8.5  # 亚洲区8.5个名额
    china_ranking = 14  # 国足当前亚洲排名
    asia_teams = 46  # 亚足联成员国数量

    # ========== 2. 四维度评估体系 ==========
    dimensions = {
        '青训发展': {'score': 5.2, 'weight': 0.4, 'color': '#FF6B6B'},
        '国家队现状': {'score': 5.8, 'weight': 0.20, 'color': '#4ECDC4'},
        '联赛水平': {'score': 6.1, 'weight': 0.30, 'color': '#45B7D1'},
        '外部环境': {'score': 4.9, 'weight': 0.20, 'color': '#96CEB4'}
    }

    # ========== 3. 计算与文本输出 ==========
    print("\n一、四维度评估分析")
    print("-" * 40)

    composite_score = 0
    for dim_name, dim_data in dimensions.items():
        dim_value = dim_data['score'] * dim_data['weight']
        composite_score += dim_value
        stars = "★" * int(dim_data['score'])
        print(f"{dim_name:8} : {dim_data['score']:.1f}分 {stars:10}")

    print(f"\n综合竞争力得分: {composite_score:.2f}/10分")

    # ========== 4. 概率计算 ==========
    # 三种计算模型
    ranking_gap = china_ranking - asia_slots
    base_prob = max(0, 50 - (ranking_gap * 8))
    score_prob = composite_score * 7
    strong_teams = 6
    remaining_slots = asia_slots - strong_teams
    competition_prob = (remaining_slots / (asia_teams - strong_teams)) * 100

    # 加权合成
    final_prob = base_prob * 0.4 + score_prob * 0.4 + competition_prob * 0.2
    final_prob = max(2, min(35, final_prob))

    print("\n二、概率计算结果")
    print("-" * 40)
    print(f"1. 排名基础概率: {base_prob:.1f}%")
    print(f"2. 综合评分概率: {score_prob:.1f}%")
    print(f"3. 竞争环境概率: {competition_prob:.1f}%")
    print(f"4. 最终预测概率: {final_prob:.1f}%")

    # ========== 5. 生成图表分析 ==========
    print("\n三、可视化分析图表生成中...")
    create_visualization_charts(dimensions, final_prob, china_ranking)

    return final_prob


def create_visualization_charts(dimensions, final_prob, china_ranking):
    """生成分析图表"""

    # 创建2行3列的图表布局
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('2030年国足世界杯出线概率分析图表', fontsize=14, fontweight='bold')

    # ===== 图表1: 四维度评分雷达图 =====
    ax1 = plt.subplot(2, 3, 1, projection='polar')

    dim_names = list(dimensions.keys())
    dim_scores = [dimensions[name]['score'] for name in dim_names]
    dim_colors = [dimensions[name]['color'] for name in dim_names]

    N = len(dim_names)
    angles = [n / N * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # 闭合
    scores = dim_scores + [dim_scores[0]]

    ax1.plot(angles, scores, 'o-', linewidth=2)
    ax1.fill(angles, scores, alpha=0.25)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(dim_names)
    ax1.set_ylim(0, 10)
    ax1.set_title('四维度综合评估', pad=20)

    # ===== 图表2: 因素权重分布 =====
    ax2 = plt.subplot(2, 3, 2)

    factors = list(dimensions.keys())
    weights = [dimensions[f]['weight'] for f in factors]
    colors = [dimensions[f]['color'] for f in factors]

    bars = ax2.bar(factors, weights, color=colors, edgecolor='black')
    ax2.set_ylabel('权重')
    ax2.set_title('各因素权重分布')
    ax2.set_ylim(0, 0.40)

    for bar, weight in zip(bars, weights):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.01,
                 f'{weight:.2f}', ha='center', va='bottom')

    # ===== 图表3: 竞争对手分析 =====
    ax3 = plt.subplot(2, 3, 3)

    teams = ['日本', '韩国', '伊朗', '澳大利亚', '沙特',
             '卡塔尔', '阿联酋', '伊拉克', '阿曼', '乌兹别克', '中国']
    rankings = [1, 3, 2, 4, 5, 6, 8, 7, 9, 11, china_ranking]
    team_colors = ['gray' if team != '中国' else 'red' for team in teams]

    bars3 = ax3.barh(teams, rankings, color=team_colors)
    ax3.set_xlabel('亚洲排名')
    ax3.set_title('主要竞争对手排名')
    ax3.invert_yaxis()

    for bar, rank in zip(bars3, rankings):
        ax3.text(rank + 0.2, bar.get_y() + bar.get_height() / 2,
                 f'第{rank}名', va='center')

    # ===== 图表4: 概率组成分析 =====
    ax4 = plt.subplot(2, 3, 4)

    prob_components = ['基础排名', '综合评分', '竞争环境']
    prob_values = [35, 40, 25]  # 三个模型的权重
    prob_colors = ['#FF9999', '#66B3FF', '#99FF99']

    wedges, texts, autotexts = ax4.pie(prob_values, labels=prob_components,
                                       colors=prob_colors, autopct='%1.1f%%',
                                       startangle=90)
    ax4.set_title('概率计算模型权重')

    # ===== 图表5: 概率可视化 =====
    ax5 = plt.subplot(2, 3, 5)

    # 进度条式显示
    ax5.barh(['出线概率'], [100], color='lightgray', alpha=0.3, height=0.3)
    prob_bar = ax5.barh(['出线概率'], [final_prob], color='green',
                        alpha=0.7, height=0.3)
    ax5.set_xlim(0, 100)
    ax5.set_xlabel('概率 (%)')
    ax5.set_title(f'最终出线概率: {final_prob:.1f}%')

    # 添加概率标签
    ax5.text(final_prob / 2, 0, f'{final_prob:.1f}%', ha='center', va='center',
             color='white', fontsize=12, fontweight='bold')

    # ===== 图表6: 敏感性分析 =====
    ax6 = plt.subplot(2, 3, 6)

    factors_sensitivity = ['青训提升', '排名提升', '联赛改善', '归化球员', '管理优化']
    base = final_prob
    impacts = [base * 1.25, base * 1.20, base * 1.15, base * 1.30, base * 1.10]

    x_pos = range(len(factors_sensitivity))
    bars6 = ax6.bar(x_pos, impacts, color=['#FF6B6B', '#4ECDC4', '#45B7D1',
                                           '#96CEB4', '#FFD166'])
    ax6.axhline(y=base, color='gray', linestyle='--', label='当前概率')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(factors_sensitivity, rotation=15)
    ax6.set_ylabel('概率 (%)')
    ax6.set_title('各因素改善的影响')
    ax6.legend()

    # 添加改善值标签
    for i, impact in enumerate(impacts):
        improvement = impact - base
        ax6.text(i, impact + 0.5, f'+{improvement:.1f}%',
                 ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

    # ===== 额外：简洁总结图 =====
    fig2, (ax7, ax8) = plt.subplots(1, 2, figsize=(12, 5))

    # 左侧：概率对比
    scenarios = ['当前水平', '青训改善', '归化助力', '最佳情况']
    probs = [final_prob, final_prob * 1.25, final_prob * 1.30, final_prob * 1.5]
    probs = [min(p, 40) for p in probs]  # 限制上限

    bars7 = ax7.bar(scenarios, probs, color=['lightgray', '#4CAF50', '#2196F3', '#FF9800'])
    ax7.set_ylabel('出线概率 (%)')
    ax7.set_title('不同发展情景对比')
    ax7.set_ylim(0, 45)

    for bar, prob in zip(bars7, probs):
        ax7.text(bar.get_x() + bar.get_width() / 2., prob + 1,
                 f'{prob:.1f}%', ha='center', va='bottom')

    # 右侧：关键建议
    ax8.axis('off')
    suggestions = [
        '1. 加强青训体系建设',
        '2. 争取亚洲排名进入前12',
        '3. 合理使用归化球员',
        '4. 改善联赛竞争环境',
        '5. 优化预选赛备战'
    ]

    ax8.text(0.1, 0.9, '关键建议措施', fontsize=12, fontweight='bold',
             transform=ax8.transAxes)
    for i, suggestion in enumerate(suggestions):
        ax8.text(0.1, 0.7 - i * 0.15, suggestion, fontsize=10,
                 transform=ax8.transAxes,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax8.text(0.5, 0.1, f'当前预测概率: {final_prob:.1f}%',
             fontsize=11, fontweight='bold', ha='center',
             transform=ax8.transAxes,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    plt.tight_layout()
    plt.show()

    print("\n图表生成完成！")
    print("=" * 60)


# 主程序
if __name__ == "__main__":
    print("开始进行2030年国足世界杯出线概率分析...\n")

    try:
        probability = calculate_worldcup_probability()

        print("\n四、关键结论与建议")
        print("-" * 40)
        print(f"1. 当前条件下，2030年出线概率约为 {probability:.1f}%")
        print("2. 主要优势：联赛水平相对较好，基础设施完善")
        print("3. 主要劣势：青训产出不足，亚洲排名偏低")
        print("4. 关键竞争对手：阿曼、乌兹别克、阿联酋、约旦")

        print("\n五、概率提升策略")
        print("-" * 40)
        print("短期策略（1-2年）：")
        print("  • 合理使用归化球员，补充关键位置")
        print("  • 优化预选赛备战，确保对阵中下游球队全取积分")
        print("  • 争取有利的预选赛分组抽签")

        print("\n长期策略（3-5年）：")
        print("  • 青训体系改革，提升至6.5分以上")
        print("  • 联赛可持续发展，增强本土球员竞争力")
        print("  • 亚洲排名稳步提升至前12名")

        print("\n" + "=" * 60)
        print("分析完成！图表已全部生成。")
        print("注：此为基于公开数据的预测分析，实际概率受多种变数影响。")
        print("=" * 60)

    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        print("请确保已安装必要的库: pip install numpy matplotlib")