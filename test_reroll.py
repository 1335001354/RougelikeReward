import numpy as np
import matplotlib.pyplot as plt

# --- 配置 Matplotlib 以正确显示中文和负号 ---
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号
except:
    print("未能设置中文字体，标签可能无法正常显示。")


# --- 1. 定义改造后的函数 ---
def modified_function(x, a, t, k_avg, k_diff, alpha):
    """
    实现改造后的函数，确保 f(0) = a。
    
    参数:
    x: 自变量，可以是一个 NumPy 数组
    a: 当 x=0 时的函数值
    t: 斜率变化的过渡点
    k_avg: 平均斜率
    k_diff: 斜率差的一半
    alpha: 过渡锐度
    """
    # 计算公式中的两个核心部分
    cosh_term_x = np.log(np.cosh(alpha * (x - t)))
    cosh_term_t = np.log(np.cosh(alpha * t)) # 这是一个常数
    
    # 返回最终计算结果
    return a + k_avg * x + (k_diff / alpha) * (cosh_term_x - cosh_term_t)


# --- 2. 设定我们示例中使用的参数 ---
a_val = 50      # 当 x=0 时的函数值
t_val = 20      # 斜率过渡点
k_avg_val = 6
k_diff_val = 4
alpha_val = 0.5


# --- 3. 生成用于绘图的数据点 ---
# x 的范围应包含 0 和 t，并向两边扩展以观察曲线形态
x_values = np.linspace(0, 40, 500)
y_values = modified_function(x_values, a_val, t_val, k_avg_val, k_diff_val, alpha_val)


# --- 4. 开始绘图 ---
plt.figure(figsize=(12, 8))

# 绘制函数曲线
plt.plot(x_values, y_values, color='purple', linewidth=2.5, label='改造后的函数曲线')

# 标记和注释关键点
# a) 标记起始点 (0, a)
plt.plot(0, a_val, 'ro', markersize=9, label=f'起始点 (0, {a_val})')
plt.text(0.5, a_val + 10, f'f(0) = {a_val}', fontsize=12)

# b) 标记斜率过渡点 t
plt.axvline(x=t_val, color='gray', linestyle='--', linewidth=1.5, label=f'斜率过渡点 t = {t_val}')
plt.text(t_val + 0.5, (y_values.min() + y_values.max())/2, f't = {t_val}\n(斜率在此处\n开始显著增大)', fontsize=12, color='gray')


# --- 5. 美化图表 ---
plt.title(f'函数图像: f(0)={a_val}, 斜率在t={t_val}时变化', fontsize=16)
plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)


# --- 6. 显示图像 ---
plt.show()