---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.6
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Python 数据分析实战：从原始数据到业务洞察


## 前言

想象一下这个场景——

你刚入职一家中型电商公司的数据团队，工位还没坐热，主管就拉了把椅子坐到你旁边，递过来一个 U 盘：

"小李，这是咱们过去一年的销售数据。你这周熟悉一下，下周一给我一份分析报告。不用太花哨，但我需要你回答这几个问题。"

他在白板上写下了五个问题：

1. **各品类的销售额和利润率如何？哪些品类最赚钱？**
2. **销售额的月度趋势如何？有没有明显的淡旺季？**
3. **不同城市的消费能力和偏好有什么差异？**
4. **不同会员等级的用户在消费行为上有什么区别？**
5. **哪些商品是明星产品？哪些可能需要调整策略？**

你点了点头，心里却在盘算：数据长什么样？干不干净？要用什么工具来分析？

别担心，这正是本教程要带你走过的完整旅程。

### 我们要做什么

本教程以一个真实的业务场景为主线，带你用 Python 完成一次完整的数据分析流程。
我们不会从枯燥的函数列表开始，而是像真正的数据分析师一样，从拿到数据的那一刻起，
一步步推进，直到最终交付一份能回答业务问题的分析报告。

整个学习路径如下：

```
数据集构建 → 数据探索 → 数据清洗 → 数据转换 → 分析建模 → 可视化呈现 → 回答业务问题
```

- **前面的章节**（本篇）：环境准备、数据集构建、数据加载与初步探索
- **下一节**（后续）：数据清洗与预处理
- **后续章节**（后续）：数据分析与可视化
- **最后**（后续）：综合分析，回答五个业务问题，撰写报告

每一部分都围绕上面的五个业务问题展开，让你始终知道"我为什么要做这一步"。

### 课程目标

完成本教程的前面后，你将能够：

1. **搭建数据分析环境**：安装和配置 pandas、numpy、matplotlib、seaborn 等核心库，并解决中文显示问题
2. **构建结构化数据集**：使用 numpy 和 pandas 生成贴近真实业务场景的模拟数据，理解电商数据的典型结构
3. **掌握数据探索的基本方法**：使用 `.shape`、`.dtypes`、`.describe()`、`.head()` 等方法快速了解数据全貌
4. **识别常见的数据质量问题**：发现缺失值、重复值、异常值和格式不一致等问题
5. **制定数据清洗计划**：根据探索结果，列出需要处理的问题和对应的策略

> 💡 **小贴士**：本教程的所有代码都可以在 Jupyter Notebook 或 JupyterLab 中逐个单元格运行。建议你一边阅读一边动手敲代码，不要只是"看"。

### 阅读本教程需要的前置知识

- Python 基础语法（变量、列表、字典、函数、循环）
- 对数据表格有基本的认识（行、列、单元格）
- 知道什么是 CSV 文件

如果你对 pandas 完全陌生也没关系，本教程会从最基础的操作讲起。


## Section 1: 环境准备与数据集构建

在动手分析之前，让我们先把工具准备好，再造一份"像模像样"的电商数据。

### 1.1 安装与导入依赖库

数据分析离不开几个核心 Python 库。如果你的环境中还没有安装它们，先运行下面的安装命令。

下面这段代码使用 pip 安装本教程需要的四个核心库：

```python
# 如果尚未安装，请在终端或 Notebook 中执行以下命令
# !pip install pandas numpy matplotlib seaborn
```

安装完成后，让我们把它们导入进来，并做一些基本配置。

下面这段代码导入所有必要的库，并设置 matplotlib 的中文显示和绘图风格：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 忽略不影响结果的警告信息，让输出更清爽
warnings.filterwarnings('ignore')

# ---------- matplotlib 中文字体设置 ----------
# 如果你在 macOS 上运行，使用 'Arial Unicode MS' 或 'PingFang SC'
# 如果你在 Windows 上运行，使用 'SimHei' 或 'Microsoft YaHei'
# 如果你在 Linux 上运行，需要先安装中文字体

import platform

system = platform.system()
if system == 'Darwin':  # macOS
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
elif system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC']

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# 设置绘图风格
sns.set_style('whitegrid')

# Pandas 显示设置
pd.set_option('display.max_columns', 20)    # 最多显示 20 列
pd.set_option('display.max_rows', 20)       # 最多显示 20 行
pd.set_option('display.float_format', '{:.2f}'.format)  # 浮点数保留两位小数
pd.set_option('display.width', 120)         # 显示宽度

print("✅ 所有库导入成功！")
```

运行后你会看到"所有库导入成功！"的提示信息。如果出现 `ModuleNotFoundError`，说明对应的库还没有安装，请回到上一步执行安装命令。

> 💡 **小贴士**：`plt.rcParams['axes.unicode_minus'] = False` 这行非常重要。不设置的话，图表中的负号会显示为一个小方块，这是中文字体环境下的常见问题。

让我们验证一下各个库的版本，确保环境没有问题：

```python
print(f"pandas  版本: {pd.__version__}")
print(f"numpy   版本: {np.__version__}")
import matplotlib
print(f"matplotlib 版本: {matplotlib.__version__}")
print(f"seaborn 版本: {sns.__version__}")
```

你会看到各个库的版本号。本教程基于 pandas 1.5+、numpy 1.20+、matplotlib 3.5+、seaborn 0.12+ 编写，如果你的版本较低，建议升级到最新版。

> **扩展阅读：为什么选择这些库？**
>
> - **pandas**：Python 数据分析的"瑞士军刀"，提供了 DataFrame 这个强大的数据结构，让你可以像操作 Excel 表格一样处理数据，但速度快得多
> - **numpy**：数值计算的基础库，pandas 底层就依赖它。我们主要用它来生成随机数据
> - **matplotlib**：Python 最基础的绘图库，几乎所有其他可视化库都建立在它之上
> - **seaborn**：基于 matplotlib 的高级可视化库，用更少的代码画出更美观的统计图表

### 1.2 构建模拟电商数据集

你可能会问："为什么不直接用真实数据？"好问题。我们使用合成数据有三个原因：

1. **可控性**：我们可以精确控制数据的特征，确保教程的每个知识点都能覆盖到
2. **可复现性**：使用固定的随机种子（`np.random.seed(42)`），你每次运行都会得到完全一样的结果
3. **隐私安全**：真实的电商数据涉及用户隐私，不适合在教程中公开

我们要构建三张表，它们之间的关系如下：

```
用户表 (users_df)          商品表 (products_df)
   |                           |
   | user_id                   | product_id
   |                           |
   +--------→ 订单表 (orders_df) ←--------+
```

- **用户表**：记录每个用户的基本信息（500 个用户）
- **商品表**：记录每个商品的信息（50 个商品，5 个品类）
- **订单表**：记录每笔订单的详情（5000 条订单记录）

这三张表通过 `user_id` 和 `product_id` 关联起来，构成一个典型的电商数据模型。

让我们开始构建吧。

#### 构建商品表 (products_df)

首先，让我们设置随机种子，然后定义商品数据。

下面这段代码定义了五个品类的商品信息，包括商品名称和价格范围：

```python
np.random.seed(42)

# 定义品类数据：品类名 -> (商品名列表, 价格范围)
categories_data = {
    '电子产品': (['智能手机', '蓝牙耳机', '平板电脑', '智能手表', '移动电源',
                  '机械键盘', '无线鼠标', '显示器', 'USB集线器', '摄像头'],
                 (200, 8000)),  # price range
    '服装':     (['T恤', '牛仔裤', '运动鞋', '连衣裙', '外套',
                  '衬衫', '短裤', '帽子', '围巾', '手套'],
                 (50, 800)),
    '食品':     (['坚果礼盒', '进口巧克力', '有机茶叶', '咖啡豆', '蜂蜜',
                  '橄榄油', '即食燕麦', '果干', '饼干', '牛肉干'],
                 (20, 300)),
    '家居':     (['台灯', '抱枕', '收纳盒', '保温杯', '地毯',
                  '香薰蜡烛', '花瓶', '相框', '桌布', '衣架套装'],
                 (30, 500)),
    '图书':     (['Python编程', '数据科学入门', '经济学原理', '人工智能导论', '项目管理',
                  '设计思维', '心理学基础', '历史通识', '科幻小说', '传记文学'],
                 (20, 120)),
}
```

这个字典的结构很清晰：键是品类名称，值是一个元组，包含该品类下的商品名列表和价格范围。比如电子产品的价格在 200 到 8000 之间，图书在 20 到 120 之间，符合我们的常识。

接下来，让我们用这些数据生成商品表。

下面这段代码遍历每个品类，为每个商品生成唯一的 ID、随机价格和成本：

```python
product_records = []
product_id_counter = 1

for category, (product_names, (price_min, price_max)) in categories_data.items():
    for name in product_names:
        # 生成产品 ID，格式为 PRD-001, PRD-002, ...
        pid = f"PRD-{product_id_counter:03d}"

        # 在价格范围内随机生成价格，保留两位小数
        price = round(np.random.uniform(price_min, price_max), 2)

        # 成本是价格的 30%~70%，模拟不同商品的毛利率差异
        cost_ratio = np.random.uniform(0.3, 0.7)
        cost = round(price * cost_ratio, 2)

        product_records.append({
            'product_id': pid,
            'product_name': name,
            'category': category,
            'price': price,
            'cost': cost,
        })
        product_id_counter += 1

products_df = pd.DataFrame(product_records)
print(f"商品表构建完成：{products_df.shape[0]} 行 × {products_df.shape[1]} 列")
print(products_df.head(10))
```

运行后你会看到商品表包含 50 行和 5 列。前 10 行展示的是电子产品品类的商品，每个商品有唯一的 `product_id`、名称、品类、价格和成本。

注意 `cost` 列——它是通过 `price * random(0.3, 0.7)` 计算出来的，这意味着不同商品的毛利率是不同的。有些商品成本占售价的 30%（高利润），有些占到 70%（低利润），这和真实的电商场景是一致的。

让我们快速看看各品类的价格分布：

```python
print("\n各品类价格统计：")
print(products_df.groupby('category')['price'].agg(['min', 'max', 'mean']).round(2))
```

输出会显示每个品类的最低价、最高价和平均价。你会发现电子产品的均价最高，图书和食品相对便宜，这符合我们的预期。

#### 构建用户表 (users_df)

接下来构建用户表。我们需要 500 个模拟用户，每个用户有性别、年龄、城市、注册日期和会员等级。

下面这段代码定义了用户数据需要的各种维度值和它们的分布比例：

```python
# 城市列表 —— 选取了 15 个代表性的中国城市
cities = ['北京', '上海', '广州', '深圳', '杭州',
          '成都', '武汉', '南京', '重庆', '西安',
          '苏州', '长沙', '青岛', '郑州', '东莞']

# 会员等级及其分布比例
membership_levels = ['普通', '银卡', '金卡', '钻石']
membership_probs = [0.50, 0.25, 0.15, 0.10]  # 普通最多，钻石最少

# 性别
genders = ['男', '女']

num_users = 500
```

这些设置反映了真实场景：大部分用户是普通会员，只有少数能达到钻石等级。城市选择覆盖了一线到新一线城市，便于后续做地域分析。

下面这段代码使用 numpy 的随机函数生成 500 个用户的完整信息：

```python
# 生成注册日期范围：2022-01-01 到 2024-12-31
register_start = pd.Timestamp('2022-01-01')
register_end = pd.Timestamp('2024-12-31')
register_range_days = (register_end - register_start).days

user_records = []
for i in range(num_users):
    uid = f"USR-{i+1:04d}"
    gender = np.random.choice(genders)
    age = np.random.randint(18, 66)  # 18 到 65 岁
    city = np.random.choice(cities)

    # 随机注册日期
    random_days = np.random.randint(0, register_range_days + 1)
    reg_date = register_start + pd.Timedelta(days=random_days)

    # 按概率分配会员等级
    membership = np.random.choice(membership_levels, p=membership_probs)

    user_records.append({
        'user_id': uid,
        'gender': gender,
        'age': age,
        'city': city,
        'register_date': reg_date.strftime('%Y-%m-%d'),
        'membership_level': membership,
    })

users_df = pd.DataFrame(user_records)
print(f"用户表构建完成：{users_df.shape[0]} 行 × {users_df.shape[1]} 列")
print(users_df.head())
```

运行后你会看到用户表包含 500 行和 6 列。每个用户有一个格式为 `USR-0001` 的唯一 ID。注意 `register_date` 列的日期范围是 2022 年到 2024 年——这意味着有些用户是老用户，有些是新用户，这会影响后续的消费行为分析。

让我们快速看看用户的基本分布情况：

```python
print("\n会员等级分布：")
print(users_df['membership_level'].value_counts())
print(f"\n性别分布：")
print(users_df['gender'].value_counts())
print(f"\n年龄统计：")
print(users_df['age'].describe())
```

输出会显示：普通会员最多（约 250 人），钻石会员最少（约 50 人）；男女比例大致均衡；年龄覆盖 18 到 65 岁。这些分布与我们设定的概率参数一致。

#### 构建订单表 (orders_df)

订单表是最核心的数据表，它连接了用户和商品。我们要生成 5000 条订单记录。

下面这段代码定义了订单相关的维度值和它们的分布概率：

```python
# 订单状态及其分布比例
order_statuses = ['已完成', '已取消', '已退款']
status_probs = [0.80, 0.12, 0.08]  # 80% 完成，12% 取消，8% 退款

# 支付方式及其分布比例
payment_methods = ['支付宝', '微信支付', '信用卡', '花呗']
payment_probs = [0.35, 0.35, 0.15, 0.15]  # 支付宝和微信各占 35%

# 订单日期范围：2024 年全年
order_start = pd.Timestamp('2024-01-01')
order_end = pd.Timestamp('2024-12-31')
order_range_days = (order_end - order_start).days

num_orders = 5000
```

注意订单日期范围是 2024 年全年。这是有意为之——整整一年的数据可以让我们分析月度趋势、发现淡旺季。

下面这段代码为每条订单随机分配用户、商品、数量、日期、支付金额、状态和支付方式：

```python
# 获取所有用户 ID 和商品 ID 列表
all_user_ids = users_df['user_id'].tolist()
all_product_ids = products_df['product_id'].tolist()

# 构建商品价格查找字典，方便后续计算支付金额
product_price_map = dict(zip(products_df['product_id'], products_df['price']))

order_records = []
for i in range(num_orders):
    oid = f"ORD-{i+1:05d}"
    uid = np.random.choice(all_user_ids)
    pid = np.random.choice(all_product_ids)

    # 购买数量：1~5 件
    quantity = np.random.randint(1, 6)

    # 随机订单日期
    random_days = np.random.randint(0, order_range_days + 1)
    o_date = order_start + pd.Timedelta(days=random_days)

    # 支付金额 = 数量 × 单价 × 折扣系数（0.85 ~ 1.0）
    base_price = product_price_map[pid]
    discount = np.random.uniform(0.85, 1.0)
    payment = round(quantity * base_price * discount, 2)

    # 订单状态和支付方式按概率分配
    status = np.random.choice(order_statuses, p=status_probs)
    pay_method = np.random.choice(payment_methods, p=payment_probs)

    order_records.append({
        'order_id': oid,
        'user_id': uid,
        'product_id': pid,
        'quantity': quantity,
        'order_date': o_date.strftime('%Y-%m-%d'),
        'payment_amount': payment,
        'order_status': status,
        'payment_method': pay_method,
    })

orders_df = pd.DataFrame(order_records)
print(f"订单表构建完成：{orders_df.shape[0]} 行 × {orders_df.shape[1]} 列")
print(orders_df.head())
```

运行后你会看到订单表包含 5000 行和 8 列。注意 `payment_amount`（支付金额）并不是简单的 `quantity × price`，而是乘了一个 0.85 到 1.0 之间的折扣系数。这模拟了电商平台常见的满减、优惠券等促销活动。

让我们看看订单的一些基本统计：

```python
print("\n订单状态分布：")
print(orders_df['order_status'].value_counts())
print(f"\n支付方式分布：")
print(orders_df['payment_method'].value_counts())
print(f"\n购买数量分布：")
print(orders_df['quantity'].value_counts().sort_index())
```

输出会显示：约 80% 的订单已完成；支付宝和微信支付占了大头；购买数量在 1~5 之间均匀分布。

> **扩展阅读：电商数据模型**
>
> 我们构建的三张表（用户、商品、订单）是典型的 **星型模型（Star Schema）**。订单表是 **事实表（Fact Table）**，记录业务事件；用户表和商品表是 **维度表（Dimension Table）**，描述业务实体的属性。这种模型在数据仓库和 BI 分析中非常常见。理解这个结构，对你以后做更复杂的数据分析项目会很有帮助。

### 1.3 注入数据质量问题

到目前为止，我们的数据是"完美"的——没有缺失值，没有重复记录，没有异常数据。但真实世界的数据很少是干净的。

作为一名数据分析师，你会经常遇到以下问题：

- **缺失值**：用户没有填写某些字段，或者系统故障导致数据丢失
- **重复记录**：网络超时导致订单被重复提交
- **异常值**：输入错误或系统 bug 产生的不合理数值
- **格式不一致**：不同系统或时间段产生的数据格式可能不统一

为了让你在后续的清洗章节中有"活"可干，让我们故意往数据里"埋"一些问题。

> 💡 **小贴士**：在真实项目中，你不需要"制造"问题——数据自带各种"惊喜"。这里我们手动注入问题，是为了确保教程能覆盖所有常见的数据质量场景。

#### 注入缺失值

下面这段代码在订单表和用户表中随机制造缺失值：

```python
# 订单表：约 5% 的 payment_amount 设为 NaN
payment_nan_indices = np.random.choice(
    orders_df.index,
    size=int(len(orders_df) * 0.05),
    replace=False
)
orders_df.loc[payment_nan_indices, 'payment_amount'] = np.nan
print(f"已在 orders_df 的 payment_amount 列注入 {len(payment_nan_indices)} 个缺失值")

# 用户表：约 3% 的 age 设为 NaN
age_nan_indices = np.random.choice(
    users_df.index,
    size=int(len(users_df) * 0.03),
    replace=False
)
users_df.loc[age_nan_indices, 'age'] = np.nan
print(f"已在 users_df 的 age 列注入 {len(age_nan_indices)} 个缺失值")

# 用户表：约 2% 的 city 设为 NaN
city_nan_indices = np.random.choice(
    users_df.index,
    size=int(len(users_df) * 0.02),
    replace=False
)
users_df.loc[city_nan_indices, 'city'] = np.nan
print(f"已在 users_df 的 city 列注入 {len(city_nan_indices)} 个缺失值")

# 用户表：约 1% 的 gender 设为 NaN
gender_nan_indices = np.random.choice(
    users_df.index,
    size=int(len(users_df) * 0.01),
    replace=False
)
users_df.loc[gender_nan_indices, 'gender'] = np.nan
print(f"已在 users_df 的 gender 列注入 {len(gender_nan_indices)} 个缺失值")
```

运行后你会看到每个字段被注入的缺失值数量。这些缺失值模拟了实际场景中的数据丢失——比如支付系统偶尔没有返回金额，用户注册时跳过了年龄和城市字段。

#### 注入重复记录

下面这段代码随机挑选 50 条订单，复制后追加到订单表末尾，模拟重复提交：

```python
# 随机选取 50 条订单进行复制，模拟网络超时导致的重复提交
duplicate_indices = np.random.choice(
    orders_df.index,
    size=50,
    replace=False
)
duplicate_rows = orders_df.loc[duplicate_indices].copy()
orders_df = pd.concat([orders_df, duplicate_rows], ignore_index=True)
print(f"已注入 {len(duplicate_rows)} 条重复记录")
print(f"订单表当前行数：{len(orders_df)}")
```

运行后你会发现订单表从 5000 行增加到了 5050 行。这 50 条重复记录和原始记录完全一样——同样的订单号、同样的商品、同样的金额。在真实场景中，这种情况通常是因为用户点击"提交订单"后没收到响应，又点了一次。

#### 注入异常值

下面这段代码在 `quantity` 列中注入一些不合理的大数值：

```python
# 在 quantity 列随机 10 个位置注入异常值
abnormal_quantities = [50, 80, 99, 100, 50, 80, 99, 100, 50, 80]
abnormal_indices = np.random.choice(
    orders_df.index,
    size=10,
    replace=False
)
for idx, val in zip(abnormal_indices, abnormal_quantities):
    orders_df.loc[idx, 'quantity'] = val

print(f"已在 quantity 列注入 {len(abnormal_indices)} 个异常值")
print(f"注入的异常值为：{abnormal_quantities}")
```

正常情况下，一个订单的购买数量是 1 到 5 件。如果有人一次买了 100 件同一个商品，这要么是批发订单（需要单独分析），要么是系统 bug。我们注入这些异常值，是为了练习如何识别和处理它们。

#### 注入日期格式不一致

下面这段代码把部分订单的日期格式从 `YYYY-MM-DD` 改为 `YYYY/MM/DD`：

```python
# 随机选取 30 条订单，将日期格式从 "2024-01-15" 改为 "2024/01/15"
date_format_indices = np.random.choice(
    orders_df.index,
    size=30,
    replace=False
)
for idx in date_format_indices:
    original_date = orders_df.loc[idx, 'order_date']
    orders_df.loc[idx, 'order_date'] = original_date.replace('-', '/')

print(f"已将 {len(date_format_indices)} 条订单的日期格式改为 '/' 分隔")

# 展示几个被修改的日期，让你看看差异
print("\n被修改的日期样例：")
print(orders_df.loc[date_format_indices[:5], 'order_date'].values)
```

输出会显示一些格式为 `2024/03/15` 的日期。在真实项目中，日期格式不一致是非常常见的问题——可能因为数据来源于不同的系统，或者不同时间段的导出格式发生了变化。

让我们总结一下注入的所有数据质量问题：

```python
print("=" * 60)
print("数据质量问题注入汇总")
print("=" * 60)
print(f"1. 缺失值：")
print(f"   - orders_df.payment_amount: ~{len(payment_nan_indices)} 个 NaN")
print(f"   - users_df.age: ~{len(age_nan_indices)} 个 NaN")
print(f"   - users_df.city: ~{len(city_nan_indices)} 个 NaN")
print(f"   - users_df.gender: ~{len(gender_nan_indices)} 个 NaN")
print(f"2. 重复记录：orders_df 中有 ~50 条重复行")
print(f"3. 异常值：quantity 列有 10 个异常大值 (50-100)")
print(f"4. 格式不一致：order_date 中有 30 条使用 '/' 分隔符")
print("=" * 60)
```

> 💡 **小贴士**：记住这些问题的类型和数量，当你在 Section 2 中做数据质量检查时，看看能不能全部发现它们。这就像是一个"寻宝游戏"——你知道宝藏的数量，但不知道它们藏在哪里。

### 1.4 保存数据到 CSV

数据构建完成，让我们把三张表保存为 CSV 文件。这样做有两个好处：一是模拟真实场景（你从主管手里拿到的通常是 CSV 或 Excel 文件），二是后续章节可以直接用 `pd.read_csv()` 加载，无需重新运行数据生成代码。

下面这段代码将三张表保存为 CSV 文件，并展示每张表的前几行作为"存档快照"：

```python
# 保存到当前工作目录
products_df.to_csv('products.csv', index=False, encoding='utf-8-sig')
users_df.to_csv('users.csv', index=False, encoding='utf-8-sig')
orders_df.to_csv('orders.csv', index=False, encoding='utf-8-sig')

print("三张数据表已保存为 CSV 文件：")
print("  - products.csv")
print("  - users.csv")
print("  - orders.csv")
```

这里使用了 `encoding='utf-8-sig'`，这是为了确保在 Windows 的 Excel 中打开时中文不会乱码。`index=False` 表示不把 DataFrame 的索引写入文件（我们已经有了自己的 ID 列）。

让我们最后看一眼每张表的样子，作为一个"存档快照"：

```python
print("\n" + "=" * 60)
print("商品表 (products_df) 预览")
print("=" * 60)
print(products_df.head())
print(f"\n形状：{products_df.shape}")

print("\n" + "=" * 60)
print("用户表 (users_df) 预览")
print("=" * 60)
print(users_df.head())
print(f"\n形状：{users_df.shape}")

print("\n" + "=" * 60)
print("订单表 (orders_df) 预览")
print("=" * 60)
print(orders_df.head())
print(f"\n形状：{orders_df.shape}")
```

你会看到三张表的前五行和各自的行列数。商品表 50 行，用户表 500 行，订单表 5050 行（原始 5000 + 50 条重复）。

到这里，我们的数据集构建工作就完成了。接下来，让我们假装自己是第一次看到这些数据——像真正的分析师一样，从加载 CSV 文件开始探索。


## Section 2: 数据加载与初步探索

现在，让我们切换角色。假设你刚收到主管给的三个 CSV 文件，你对里面的数据一无所知。第一步该做什么？

答案是：**先看看数据长什么样**。

数据探索（**Exploratory Data Analysis**，简称 **EDA**）是数据分析的第一步，也是最重要的一步。它的目的不是得出结论，而是建立对数据的直觉——有多少行？���哪些列？数据类型是什么？有没有明显的问题？

让我们开始吧。

### 2.1 加载数据

下面这段代码使用 `pd.read_csv()` 从 CSV 文件中加载三张数据表：

```python
# 从 CSV 文件加载数据
products_df = pd.read_csv('products.csv')
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

print("数据加载完成！")
print(f"  商品表: {products_df.shape[0]} 行 × {products_df.shape[1]} 列")
print(f"  用户表: {users_df.shape[0]} 行 × {users_df.shape[1]} 列")
print(f"  订单表: {orders_df.shape[0]} 行 × {orders_df.shape[1]} 列")
```

`pd.read_csv()` 是 pandas 中最常用的数据加载函数。它自动识别逗号分隔符、自动推断数据类型、自动处理表头。大部分时候，你只需要传一个文件路径就够了。

> 💡 **小贴士**：`pd.read_csv()` 有很多实用的参数，以下是最常用的几个：
>
> | 参数 | 说明 | 示例 |
> |------|------|------|
> | `sep` | 分隔符，默认逗号 | `sep='\t'` 用于 TSV 文件 |
> | `encoding` | 编码格式 | `encoding='gbk'` 用于部分中文文件 |
> | `header` | 表头行号 | `header=None` 表示文件没有表头 |
> | `usecols` | 只读取指定列 | `usecols=['name', 'age']` |
> | `nrows` | 只读取前 N 行 | `nrows=100` 用于快速预览大文件 |
> | `dtype` | 指定列的数据类型 | `dtype={'id': str}` |
> | `parse_dates` | 自动解析日期列 | `parse_dates=['date']` |
> | `na_values` | 自定义缺失值标记 | `na_values=['NA', 'missing']` |

### 2.2 快速了解数据全貌

拿到数据后，让我们用几个基本方法快速建立对数据的整体印象。

#### 查看行列数

下面这段代码使用 `.shape` 属性查看每张表的行数和列数：

```python
print("各表的行列数（行, 列）：")
print(f"  商品表: {products_df.shape}")
print(f"  用户表: {users_df.shape}")
print(f"  订单表: {orders_df.shape}")
```

`.shape` 返回一个元组 `(行数, 列数)`。这是你拿到数据后应该做的第一件事——知道数据的"大小"。

#### 查看数据类型

下面这段代码使用 `.dtypes` 查看每张表各列的数据类型：

```python
print("=" * 40)
print("商品表的数据类型：")
print("=" * 40)
print(products_df.dtypes)

print("\n" + "=" * 40)
print("用户表的数据类型：")
print("=" * 40)
print(users_df.dtypes)

print("\n" + "=" * 40)
print("订单表的数据类型：")
print("=" * 40)
print(orders_df.dtypes)
```

你会看到类似这样的输出：

- `object`：表示字符串类型（如 product_id、product_name）
- `float64`：表示浮点数（如 price、payment_amount）
- `int64`：表示整数（如 quantity）

> 💡 **小贴士**：注意 `order_date` 和 `register_date` 的类型是 `object` 而不是 `datetime64`。这是因为 `pd.read_csv()` 默认不会自动将字符串解析为日期。我们在清洗阶段需要手动转换它们。

#### 预览数据内容

下面这段代码使用 `.head()` 和 `.tail()` 查看数据的前几行和最后几行：

```python
print("=" * 60)
print("商品表 - 前 5 行")
print("=" * 60)
print(products_df.head())

print("\n" + "=" * 60)
print("商品表 - 后 5 行")
print("=" * 60)
print(products_df.tail())
```

`.head(n)` 显示前 n 行（默认 5 行），`.tail(n)` 显示后 n 行。查看最后几行很重要，因为有时数据末尾会有汇总行或空行。

让我们也看看用户表和订单表：

```python
print("=" * 60)
print("用户表 - 前 5 行")
print("=" * 60)
print(users_df.head())

print("\n" + "=" * 60)
print("订单表 - 前 5 行")
print("=" * 60)
print(orders_df.head())
```

通过预览，你可以直观地看到每一列长什么样。比如 `product_id` 是 `PRD-001` 格式，`user_id` 是 `USR-0001` 格式，`order_date` 是日期字符串。

#### 查看列名

下面这段代码使用 `.columns` 查看每张表的列名：

```python
print("商品表列名：", products_df.columns.tolist())
print("用户表列名：", users_df.columns.tolist())
print("订单表列名：", orders_df.columns.tolist())
```

`.columns.tolist()` 把列名转为 Python 列表，方便查看。当表的列数很多时，直接打印 `.columns` 可能会折行，用 `.tolist()` 更清晰。

> **扩展阅读：`.info()` 方法**
>
> 如果你想一次性查看数据的行列数、列名、数据类型和非空值计数，可以使用 `.info()` 方法。它是 `.shape`、`.dtypes` 和 `.isnull().sum()` 的"合体版"。

让我们用 `.info()` 来获取更完整的信息：

```python
print("=" * 60)
print("订单表详细信息")
print("=" * 60)
orders_df.info()
```

`.info()` 的输出会告诉你每列有多少非空值（non-null count）。如果某列的非空值少于总行数，说明该列存在缺失值。���是发现缺失值的另一种方式。

### 2.3 统计摘要

了解了数据的"外貌"后，让我们看看数据的"内涵"——通过统计摘要来了解数值的分布范围。

#### 数值列统计

下面这段代码使用 `.describe()` 查看数值列的统计摘要：

```python
print("=" * 60)
print("商品表 - 数值列统计摘要")
print("=" * 60)
print(products_df.describe())
```

`.describe()` 会为每个数值列计算 8 个统计量：

| 统计量 | 含义 |
|--------|------|
| `count` | 非空值数量 |
| `mean` | 平均值 |
| `std` | 标准差（衡量数据分散程度） |
| `min` | 最小值 |
| `25%` | 第一四分位数（25% 的数据小于此值） |
| `50%` | 中位数（也叫第二四分位数） |
| `75%` | 第三四分位数 |
| `max` | 最大值 |

让我们重点看一下订单表的统计：

```python
print("\n" + "=" * 60)
print("订单表 - 数值列统计摘要")
print("=" * 60)
print(orders_df.describe())
```

你会看到 `quantity` 列的统计结果。观察一下 `max` 值——它会显示一个远大于 5 的数字。还记得我们注入的异常值吗？`quantity` 的正常范围应该是 1~5，但 `max` 可能是 100。这就是异常值的信号。

同样，`payment_amount` 的 `count` 会小于总行数，因为我们注入了缺失值。`count` 和总行数的差值就是缺失值的数量。

再看看用户表：

```python
print("\n" + "=" * 60)
print("用户表 - 数值列统计摘要")
print("=" * 60)
print(users_df.describe())
```

`age` 列的 `count` 同样会少于 500，说明有缺失值。`min` 应该是 18，`max` 应该是 65，符合我们的设定范围。

#### 分类列统计

`.describe()` 默认只统计数值列。要查看分类列（字符串列）的统计信息，需要加上 `include='object'` 参数。

下面这段代码查看分类列的统计摘要：

```python
print("=" * 60)
print("订单表 - 分类列统计摘要")
print("=" * 60)
print(orders_df.describe(include='object'))
```

分类列的 `.describe()` 会显示：

| 统计量 | 含义 |
|--------|------|
| `count` | 非空值数量 |
| `unique` | 唯一值的数量 |
| `top` | 出现频率最高的值 |
| `freq` | 最高频率值的出现次数 |

比如 `order_status` 的 `unique` 应该是 3（已完成、已取消、已退款），`top` 应该是"已完成"（因为它占了 80%）。

```python
print("\n" + "=" * 60)
print("用户表 - 分类列统计摘要")
print("=" * 60)
print(users_df.describe(include='object'))
```

查看用户表的分类列统计，你会发现 `city` 有 15 个唯一值（对应我们设定的 15 个城市），`membership_level` 有 4 个唯一值。

> 💡 **小贴士**：`describe()` 是"数据体检报告"。养成习惯：每次拿到新数据，先跑一遍 `describe()`，快速发现异常值和缺失值。

### 2.4 数据质量初步检查

统计摘要给了我们一些线索，但要全面检查数据质量，还需要更细致的方法。让我们逐项检查。

#### 检查缺失值

下面这段代码使用 `.isnull().sum()` 统计每张表每列的缺失值数量：

```python
print("=" * 60)
print("缺失值检查")
print("=" * 60)

print("\n商品表缺失值：")
print(products_df.isnull().sum())

print("\n用户表缺失值：")
print(users_df.isnull().sum())

print("\n订单表缺失值：")
print(orders_df.isnull().sum())
```

`.isnull()` 对每个单元格返回 `True`（缺失）或 `False`（非缺失），`.sum()` 把 `True` 加起来，得到每列的缺失值数量。

你会发现：
- 商品表没有缺失值（我们没有对它做手脚）
- 用户表的 `age`、`city`、`gender` 列有缺失值
- 订单表的 `payment_amount` 列有缺失值

让我们进一步看看缺失值的占比：

```python
print("\n" + "=" * 60)
print("缺失值占比")
print("=" * 60)

print("\n用户表缺失比例：")
print((users_df.isnull().sum() / len(users_df) * 100).round(2))

print("\n订单表缺失比例：")
print((orders_df.isnull().sum() / len(orders_df) * 100).round(2))
```

输出会以百分比形式展示每列的缺失率。一般来说，缺失率低于 5% 的列，可以用均值、中位数或众数填充；缺失率过高（比如超过 50%）的列，可能需要考虑直接删除。

#### 检查重复值

下面这段代码使用 `.duplicated().sum()` 统计重复行的数量：

```python
print("=" * 60)
print("重复值检查")
print("=" * 60)

print(f"商品表重复行数：{products_df.duplicated().sum()}")
print(f"用户表重复行数：{users_df.duplicated().sum()}")
print(f"订单表重复行数：{orders_df.duplicated().sum()}")
```

`.duplicated()` 标记每一行是否是前面某行的完全复制。你会发现订单表存在重复行。

让我们看看这些重复的订单长什么样：

```python
# 找出重复的行
duplicated_mask = orders_df.duplicated(keep=False)  # keep=False 同时标记原始行和重复行
duplicated_orders = orders_df[duplicated_mask].sort_values('order_id')
print(f"\n涉及重复的总行数（含原始行）：{len(duplicated_orders)}")
print("\n重复订单示例（前 10 行）：")
print(duplicated_orders.head(10))
```

`keep=False` 参数会标记所有参与重复的行（包括"原始"行和"复制"行），这样你可以完整地看到哪些订单被重复了。

#### 查看分类列的值分布

下面这段代码使用 `.value_counts()` 查看分类列中每个值出现的频次：

```python
print("=" * 60)
print("分类列值分布")
print("=" * 60)

print("\n订单状态分布：")
print(orders_df['order_status'].value_counts())

print("\n支付方式分布：")
print(orders_df['payment_method'].value_counts())

print("\n商品品类分布：")
print(products_df['category'].value_counts())

print("\n会员等级分布：")
print(users_df['membership_level'].value_counts())

print("\n城市分布（前 10 名）：")
print(users_df['city'].value_counts().head(10))
```

`.value_counts()` 默认按频次降序排列。通过观察分布，你可以判断数据是否合理。比如"已完成"状态应该占大多数，如果"已取消"占了 80%，那就需要调查原因了。

#### 发现异常值

下面这段代码通过条件筛选来发现 `quantity` 列中的异常值：

```python
print("=" * 60)
print("异常值检查")
print("=" * 60)

# 正常的购买数量应该在 1-5 之间
abnormal_quantity = orders_df[orders_df['quantity'] > 10]
print(f"\n购买数量 > 10 的订单数：{len(abnormal_quantity)}")
print("\n异常订单详情：")
print(abnormal_quantity[['order_id', 'product_id', 'quantity', 'payment_amount']])
```

你会看到有若干条订单的 `quantity` 值远超正常范围。这些异常值需要在清洗阶段处理——要么删除，要么替换为合理值，取决于业务逻辑。

让我们也用箱线图的思路来检查异常值：

```python
# 使用四分位距（IQR）方法检测 payment_amount 的异常值
Q1 = orders_df['payment_amount'].quantile(0.25)
Q3 = orders_df['payment_amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = orders_df[
    (orders_df['payment_amount'] < lower_bound) |
    (orders_df['payment_amount'] > upper_bound)
]
print(f"\npayment_amount 的 IQR 异常值检测：")
print(f"  Q1 = {Q1:.2f}, Q3 = {Q3:.2f}, IQR = {IQR:.2f}")
print(f"  正常范围: [{lower_bound:.2f}, {upper_bound:.2f}]")
print(f"  异常值数量: {len(outliers)}")
```

**IQR（四分位距）** 方法是检测异常值的经典方法。任何低于 `Q1 - 1.5 * IQR` 或高于 `Q3 + 1.5 * IQR` 的值都被视为潜在异常值。不过要注意，这个方法有时会把正常的高价商品标记为异常，所以需要结合业务理解来判断。

> **扩展阅读：异常值检测方法**
>
> 除了 IQR 方法，常见的异常值检测方法还有：
> - **Z-score 方法**：计算每个值偏离均值的标准差数，通常认为 |Z| > 3 为异常值
> - **修改后的 Z-score**：使用中位数和 MAD（中位绝对偏差）替代均值和标准差，对偏态分布更稳健
> - **业务规则法**：根据业务逻辑设定合理范围（比如我们知道购买数量应该在 1~5 之间）

#### 发现日期格式不一致

下面这段代码检查 `order_date` 列中是否存在格式不一致的问题：

```python
print("=" * 60)
print("日期格式一致性检查")
print("=" * 60)

# 检查是否存在使用 "/" 分隔符的日期
slash_dates = orders_df[orders_df['order_date'].str.contains('/', na=False)]
print(f"\n使用 '/' 分隔符的日期数量：{len(slash_dates)}")
print("\n示例：")
print(slash_dates[['order_id', 'order_date']].head())

# 对比正常格式
normal_dates = orders_df[orders_df['order_date'].str.contains('-', na=False)]
print(f"\n使用 '-' 分隔符的日期数量：{len(normal_dates)}")
```

你会发现大部分日期使用 `-` 分隔（如 `2024-01-15`），但有一小部分使用 `/` 分隔（如 `2024/01/15`）。这种不一致会导致后续的日期排序和时间序列分析出错，必须在清洗阶段统一格式。

### 2.5 小结：制定清洗计划

经过上面的探索，让我们把发现的所有数据质量问题汇总起来，并制定清洗策略。

下面这段代码整理发现的问题并输出清洗计划：

```python
print("=" * 60)
print("数据质量问题汇总与清洗计划")
print("=" * 60)

print("""
┌──────────────────────────────────────────────────────────┐
│  问题类型        │  涉及表/列              │  建议策略      │
├──────────────────────────────────────────────────────────┤
│  1. 缺失值       │  orders_df.payment_amount  │  用中位数填充   │
│                  │  users_df.age              │  用中位数填充   │
│                  │  users_df.city             │  用众数填充     │
│                  │  users_df.gender           │  用众数填充     │
├──────────────────────────────────────────────────────────┤
│  2. 重复记录     │  orders_df 全表             │  删除重复行     │
├──────────────────────────────────────────────────────────┤
│  3. 异常值       │  orders_df.quantity         │  限制在合理范围 │
├──────────────────────────────────────────────────────────┤
│  4. 格式不一致   │  orders_df.order_date       │  统一为标准格式 │
├──────────────────────────────────────────────────────────┤
│  5. 类型转换     │  orders_df.order_date       │  转为 datetime  │
│                  │  users_df.register_date     │  转为 datetime  │
└──────────────────────────────────────────────────────────┘
""")
```

让我们也输出一些关键的数据质量指标：

```python
print("关键数据质量指标：")
print(f"  订单表总行数（含重复）：{len(orders_df)}")
print(f"  订单表重复行数：{orders_df.duplicated().sum()}")
print(f"  订单表缺失值总数：{orders_df.isnull().sum().sum()}")
print(f"  用户表缺失值总数：{users_df.isnull().sum().sum()}")
print(f"  quantity 异常值数量（>10）：{len(orders_df[orders_df['quantity'] > 10])}")
print(f"  日期格式不一致数量：{len(orders_df[orders_df['order_date'].str.contains('/', na=False)])}")
```

> 💡 **小贴士**：在真实项目中，数据探索阶段不需要急于"修复"问题。先把问题全部列出来，评估严重程度，再制定优先级和处理策略。有些问题可能不影响分析结果，可以暂时搁置。

现在，让我们把清洗策略更详细地记录下来，作为 下一节 的行动指南：

```python
cleaning_plan = {
    '第一步': '删除重复记录 —— 使用 drop_duplicates()',
    '第二步': '统一日期格式 —— 将 "/" 替换为 "-"',
    '第三步': '转换数据类型 —— 将日期列转为 datetime 类型',
    '第四步': '处理缺失值 —— 数值列用中位数，分类列用众数',
    '第五步': '处理异常值 —— 将 quantity > 10 的值替换或删除',
    '第六步': '数据验证 —— 确认所有问题已解决',
}

print("\n清洗步骤：")
for step, action in cleaning_plan.items():
    print(f"  {step}: {action}")

print("\n" + "=" * 60)
print("前面的章节 完成！")
print("=" * 60)
print("接下来，我们将按照上面的计划逐步清洗数据，")
print("让这份'脏'数据变成可以用于分析的高质量数据集。")
```

<!-- #region -->
## Section 3: 数据清洗

前面我们已经加载了三张数据表，并通过初步探索发现了不少数据质量问题。现在，让我们动手把这些"脏数据"清理干净。

数据清洗是数据分析中最耗时、也最重要的环节。业界有一句老话："数据分析 80% 的时间花在数据清洗上。"虽然这个比例因项目而异，但它说明了一个事实——如果数据本身有问题，后续所有的分析结论都不可信。

在这一节中，我们会对 前面发现的每个问题，按照**"发现 → 处理 → 验证"**的三步模式逐一处理。这个模式非常重要：处理完一个问题后，一定要验证它确实被修复了，否则你可能会在后续分析中踩坑。

让我们先回顾一下 前面发现的数据质量问题清单：

1. `orders_df` 有约 50 条重复行
2. `order_date` 有约 30 条格式不一致（用了 `/` 而非 `-`）
3. `quantity` 有约 10 个异常值（50、80、99、100 等）
4. `users_df` 的 `age` 约 3% 缺失、`city` 约 2% 缺失、`gender` 约 1% 缺失
5. `orders_df` 的 `payment_amount` 约 5% 缺失

我们按照从简单到复杂的顺序来处理它们。


### 3.1 处理重复数据

**重复数据**是最常见的数据质量问题之一。它可能来自数据导入时的重复提交、系统 bug，或者多个数据源合并时的交叉重叠。不管原因是什么，重复数据会导致统计结果偏高，必须在分析前清除。

#### 第一步：发现

让我们先确认重复数据的数量。
<!-- #endregion -->

```python
# 检查重复行的数量
dup_count = orders_df.duplicated().sum()
print(f"orders_df 中的重复行数: {dup_count}")
```

`duplicated()` 方法会逐行检查，如果某一行的所有列值都和前面的某一行完全相同，就标记为 `True`。`.sum()` 对这些布尔值求和，得到重复行的总数。

确认有重复行之后，让我们看看这些重复行长什么样。

```python
# 查看所有重复的行（包括"原始"行和"重复"行）
dup_rows = orders_df[orders_df.duplicated(keep=False)]
print(f"涉及重复的总行数: {len(dup_rows)}")
print(dup_rows.sort_values('order_id').head(10))
```

注意这里用了 `keep=False` 参数。这会标记所有涉及重复的行，包括第一次出现的那行。这样你可以看到完整的重复组，判断它们是否真的是完全一样的。

> 💡 **小贴士**：`duplicated()` 的 `keep` 参数有三个选项，理解它们的区别很重要：
> - `keep='first'`（默认）：第一次出现的行标记为 `False`，后续重复的标记为 `True`
> - `keep='last'`：最后一次出现的行标记为 `False`，前面的重复标记为 `True`
> - `keep=False`：所有涉及重复的行都标记为 `True`，不保留任何一个
>
> 在检查数据时用 `keep=False` 能看到全貌，在删除数据时用 `keep='first'` 或 `keep='last'` 保留其中一条。

#### 第二步：处理

确认这些确实是应该删除的重复行后，让我们去重。

```python
# 记录去重前的行数
rows_before = len(orders_df)

# 去除重复行，保留第一次出现的记录
orders_df.drop_duplicates(inplace=True)

# 重置索引（去重后索引会不连续）
orders_df.reset_index(drop=True, inplace=True)

rows_after = len(orders_df)
print(f"去重前: {rows_before} 行")
print(f"去重后: {rows_after} 行")
print(f"删除了 {rows_before - rows_after} 条重复记录")
```

`drop_duplicates()` 默认使用 `keep='first'`，也就是保留每组重复行中第一次出现的那条。`inplace=True` 表示直接在原 DataFrame 上修改，而不是返回一个新的副本。

#### 第三步：验证

去重后一定要验证结果。

```python
# 验证：确认没有重复行了
remaining_dups = orders_df.duplicated().sum()
print(f"去重后剩余重复行: {remaining_dups}")
assert remaining_dups == 0, "仍然存在重复行！"
print("✓ 重复数据处理完毕")
```

<!-- #region -->
如果断言没有抛出异常，说明重复数据已经完全清除。让我们继续处理下一个问题。


### 3.2 统一日期格式

在前面的探索中，我们发现 `order_date` 列中大部分日期用的是 `2024-01-15` 这种格式（用 `-` 分隔），但有约 30 条记录使用了 `2024/01/15` 这种格式（用 `/` 分隔）。格式不统一会导致后续转换为 datetime 类型时出错，必须先修复。

#### 第一步：发现

让我们先找出这些格式不一致的行。
<!-- #endregion -->

```python
# 找出使用 "/" 分隔符的日期记录
slash_dates = orders_df[orders_df['order_date'].str.contains('/', na=False)]
print(f"使用 '/' 格式的日期数量: {len(slash_dates)}")
print("示例：")
print(slash_dates[['order_id', 'order_date']].head(10))
```

`str.contains('/')` 会检查每个值中是否包含斜杠字符。`na=False` 参数确保如果遇到缺失值不会报错，而是返回 `False`。

#### 第二步：处理

修复方法很直接——把所有的 `/` 替换成 `-`。

```python
# 将日期中的 "/" 统一替换为 "-"
orders_df['order_date'] = orders_df['order_date'].str.replace('/', '-')
```

这行代码对 `order_date` 列的每个值执行字符串替换。对于原本就用 `-` 的日期，替换操作不会产生影响，所以不需要只针对问题行操作。

#### 第三步：验证

```python
# 验证：确认没有 "/" 格式的日期了
remaining_slash = orders_df[orders_df['order_date'].str.contains('/', na=False)]
print(f"修复后仍使用 '/' 格式的数量: {len(remaining_slash)}")

# 查看修复后日期的格式样本
print("\n修复后的日期样本：")
print(orders_df['order_date'].sample(5).values)
print("✓ 日期格式统一完毕")
```

<!-- #region -->
日期格式问题处理起来相对简单，但如果忽略它，后续转换 datetime 类型时可能会导致部分数据解析失败或被解析为错误的日期。


### 3.3 处理异常值

**异常值**（Outlier）是指那些明显偏离正常范围的数据点。在我们的数据中，`quantity`（订单数量）列出现了 50、80、99、100 等极端值，而正常订单的数量通常在 1-10 之间。

处理异常值之前，你需要先回答一个关键问题：这些极端值是"错误数据"还是"真实但罕见的情况"？这个问题没有标准答案，需要结合**业务背景**来判断。

在我们的电商场景中，一个用户在一笔订单中购买 100 件同一商品是极不合理的——这很可能是录入错误或测试数据。

#### 第一步：发现
<!-- #endregion -->

```python
# 查看 quantity 的基本统计信息
print("quantity 的统计描述：")
print(orders_df['quantity'].describe())
print(f"\n最大值: {orders_df['quantity'].max()}")
print(f"最小值: {orders_df['quantity'].min()}")
```

```python
# 查看异常订单的详细信息
abnormal_orders = orders_df[orders_df['quantity'] > 10]
print(f"\nquantity > 10 的订单数量: {len(abnormal_orders)}")
print(abnormal_orders[['order_id', 'product_id', 'quantity', 'payment_amount']].to_string(index=False))
```

可以看到，正常订单的 `quantity` 集中在 1-10 的范围，而这些异常值远远超出了这个范围。

#### 第二步：处理

面对异常值，常见的处理策略有三种：

| 策略 | 做法 | 适用场景 |
|------|------|----------|
| **删除** | 直接删掉异常行 | 异常值占比极小，且确认是错误数据 |
| **截断（Winsorize）** | 将超出范围的值替换为边界值 | 希望保留记录但修正极端值 |
| **标记** | 新增一列标记异常值 | 不确定是否为错误，先标记后续再分析 |

在这里，我们选择**截断策略**，将超过 10 的 `quantity` 值截断为 10。为什么不直接删除？因为这些订单虽然数量异常，但订单本身可能是真实的（有真实的用户、真实的支付），删除会丢失其他维度的信息。截断可以保留订单记录，同时消除数量上的极端影响。

```python
# 记录处理前的异常值数量
abnormal_count_before = (orders_df['quantity'] > 10).sum()

# 截断策略：将 quantity > 10 的值设为 10
orders_df.loc[orders_df['quantity'] > 10, 'quantity'] = 10

abnormal_count_after = (orders_df['quantity'] > 10).sum()
print(f"截断前异常值数量: {abnormal_count_before}")
print(f"截断后异常值数量: {abnormal_count_after}")
```

`.loc[condition, column]` 是 pandas 中按条件定位并修改数据的标准方式。它只修改满足条件的行，不影响其他数据。

#### 第三步：验证

```python
# 验证 quantity 的范围
print(f"quantity 范围: [{orders_df['quantity'].min()}, {orders_df['quantity'].max()}]")
print(f"\nquantity 分布：")
print(orders_df['quantity'].value_counts().sort_index())
print("✓ 异常值处理完毕")
```

<!-- #region -->
验证结果应该显示 `quantity` 的最大值现在是 10，所有值都在合理范围内。

> 💡 **小贴士**：除了基于业务规则的判断外，还有一种常用的统计方法来检测异常值——**IQR（四分位距）方法**。它的原理是：计算数据的第一四分位数 Q1 和第三四分位数 Q3，然后用 IQR = Q3 - Q1 计算四分位距，将低于 Q1 - 1.5 * IQR 或高于 Q3 + 1.5 * IQR 的值视为异常值。下面是代码示例：
>
> ```python
> Q1 = orders_df['quantity'].quantile(0.25)
> Q3 = orders_df['quantity'].quantile(0.75)
> IQR = Q3 - Q1
> lower_bound = Q1 - 1.5 * IQR
> upper_bound = Q3 + 1.5 * IQR
> outliers = orders_df[(orders_df['quantity'] < lower_bound) | (orders_df['quantity'] > upper_bound)]
> print(f"IQR 方法检测到的异常值数量: {len(outliers)}")
> ```
>
> 不过在本场景中，我们用业务规则（quantity > 10 即为异常）更加直观和可解释。IQR 方法更适合那些没有明确业务边界的连续型数值变量。

> **扩展阅读：常用的异常值检测方法**
>
> 在数据分析实践中，有三种最常用的异常值检测方法，各有适用场景：
>
> 1. **Z-score 方法**：计算每个数据点偏离均值多少个标准差。通常将 |Z| > 3 的值视为异常值。这种方法假设数据服从正态分布，对于偏态数据效果不佳。公式：`Z = (x - mean) / std`。
>
> 2. **IQR 方法**：基于四分位距检测异常值，不依赖正态分布假设，对偏态数据更加稳健。如上面小贴士中所述，将超出 `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]` 范围的值视为异常值。
>
> 3. **箱线图（Box Plot）方法**：其实就是 IQR 方法的可视化版本。箱线图中，箱子的上下边界分别是 Q3 和 Q1，从箱子延伸出去的"须"到达 1.5 倍 IQR 的位置，须外面的散点就是异常值。用 `df.boxplot(column='quantity')` 一行代码就能直观看到。
>
> 在实际工作中，建议先用业务知识设定合理范围，再用统计方法作为补充参考。毕竟，数据分析最终服务于业务，业务逻辑比纯统计更可靠。


### 3.4 处理缺失值

**缺失值**是数据分析中最常见的问题，几乎每个真实数据集都有。缺失值的处理策略取决于缺失比例、缺失原因和后续分析需求。盲目删除或填充都可能引入偏差，所以我们需要"对症下药"。

#### 第一步：全面发现

在逐个处理之前，让我们先对所有表的缺失值做一个全面的盘点。
<!-- #endregion -->

```python
# 定义一个函数来生成缺失值报告
def missing_report(df, name):
    """生成 DataFrame 的缺失值报告"""
    missing_count = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    report = pd.DataFrame({
        '缺失数量': missing_count,
        '缺失比例(%)': missing_pct
    })
    # 只显示有缺失值的列
    report = report[report['缺失数量'] > 0]
    if len(report) == 0:
        print(f"\n{name}: 无缺失值 ✓")
    else:
        print(f"\n{name} 的缺失值情况：")
        print(report)
    return report

# 分别检查三张表
missing_orders = missing_report(orders_df, 'orders_df')
missing_products = missing_report(products_df, 'products_df')
missing_users = missing_report(users_df, 'users_df')
```

输出结果应该显示：`orders_df` 的 `payment_amount` 有约 5% 缺失，`users_df` 的 `age`、`city`、`gender` 分别有约 3%、2%、1% 的缺失，`products_df` 没有缺失值。

#### 第二步：分列处理

面对缺失值，常见的处理策略如下：

| 策略 | 做法 | 适用场景 |
|------|------|----------|
| **删除行** | `df.dropna()` | 缺失比例极低（< 1%），且删除后不影响样本分布 |
| **填充** | `df.fillna(value)` | 有合理的填充值可用 |
| **保留** | 不做处理 | 后续算法能处理缺失值，或者等获取更多信息后再处理 |

让我们逐个处理。

**处理 users_df 的 age 缺失值——中位数填充**

```python
# 查看 age 的分布情况，决定填充策略
print("age 的描述统计：")
print(users_df['age'].describe())
print(f"\n均值: {users_df['age'].mean():.1f}")
print(f"中位数: {users_df['age'].median():.1f}")
```

你会注意到均值和中位数可能有所不同。我们选择用**中位数**填充而不是**均值**，原因有两个：

1. 中位数对异常值不敏感。如果 `age` 中有极端值（比如 0 岁或 150 岁这样的错误数据），均值会被拉偏，而中位数不受影响。
2. 年龄数据通常不是完美的正态分布，中位数能更好地代表"典型用户"的年龄。

```python
# 用中位数填充 age 的缺失值
age_median = users_df['age'].median()
users_df['age'] = users_df['age'].fillna(age_median)
print(f"age 缺失值已用中位数 {age_median} 填充")
print(f"填充后 age 缺失数量: {users_df['age'].isnull().sum()}")
```

**处理 users_df 的 city 缺失值——用"未知"填充**

```python
# 用 "未知" 填充 city 的缺失值
users_df['city'] = users_df['city'].fillna('未知')
print(f"city 缺失值已用 '未知' 填充")
print(f"填充后 city 缺失数量: {users_df['city'].isnull().sum()}")
```

对于类别型变量，用"未知"填充是一个安全的选择。它既不会引入虚假信息（比如随机指定一个城市），又能保留该记录的其他信息。在后续分析中，你可以把"未知"当作一个单独的类别来看待。

**处理 users_df 的 gender 缺失值——用"未知"填充**

```python
# 用 "未知" 填充 gender 的缺失值
users_df['gender'] = users_df['gender'].fillna('未知')
print(f"gender 缺失值已用 '未知' 填充")
print(f"填充后 gender 缺失数量: {users_df['gender'].isnull().sum()}")
```

**关于 orders_df 的 payment_amount——暂不处理**

你可能会问：`payment_amount` 的缺失值怎么不处理？好问题。`payment_amount` 代表的是订单支付金额，它应该等于 `quantity * price`。但是 `price` 信息在 `products_df` 表中，而现在我们还没有合并这两张表。所以我们先标记这个待办事项，等到 Section 4 合并表之后再处理。

```python
# payment_amount 暂不处理，记录待办
print(f"\n⚠ orders_df 的 payment_amount 仍有 {orders_df['payment_amount'].isnull().sum()} 个缺失值")
print("  → 需要商品价格信息，等合表后再用 quantity * price 填充")
```

#### 第三步：验证

```python
# 全面验证填充结果
print("=" * 50)
print("缺失值处理后的验证报告")
print("=" * 50)
missing_report(orders_df, 'orders_df')
missing_report(products_df, 'products_df')
missing_report(users_df, 'users_df')
```

<!-- #region -->
验证结果应该显示：`users_df` 已经没有缺失值了，`orders_df` 只剩 `payment_amount` 的缺失值待处理，`products_df` 一直没有缺失值。

> 💡 **小贴士**：`fillna()` 还有一些高级用法，适用于时间序列数据：
> - `method='ffill'`（前向填充）：用前一个非缺失值填充当前缺失值。比如股票价格数据中，某天没有交易记录，就用前一天的收盘价填充。
> - `method='bfill'`（后向填充）：用后一个非缺失值填充当前缺失值。方向和 ffill 相反。
>
> 注意：在较新版本的 pandas 中，推荐使用 `df.ffill()` 和 `df.bfill()` 代替 `fillna(method=...)`，功能一样，写法更简洁。
>
> ```python
> # 前向填充示例（时间序列场景）
> # df['stock_price'] = df['stock_price'].ffill()
> # 后向填充示例
> # df['stock_price'] = df['stock_price'].bfill()
> ```


### 3.5 清洗结果验证

所有清洗步骤都做完了，让我们做一次全面的"体检"，确保数据质量达标。
<!-- #endregion -->

```python
print("=" * 60)
print("         数 据 清 洗 报 告")
print("=" * 60)

# 1. 重复数据检查
print("\n【1. 重复数据】")
print(f"  orders_df 重复行: {orders_df.duplicated().sum()}")
print(f"  products_df 重复行: {products_df.duplicated().sum()}")
print(f"  users_df 重复行: {users_df.duplicated().sum()}")

# 2. 日期格式检查
print("\n【2. 日期格式】")
slash_count = orders_df['order_date'].str.contains('/', na=False).sum()
print(f"  order_date 含 '/' 的记录: {slash_count}")

# 3. 异常值检查
print("\n【3. 异常值】")
print(f"  quantity 范围: [{orders_df['quantity'].min()}, {orders_df['quantity'].max()}]")
print(f"  quantity > 10 的记录: {(orders_df['quantity'] > 10).sum()}")

# 4. 缺失值检查
print("\n【4. 缺失值】")
for name, df_check in [('orders_df', orders_df), ('products_df', products_df), ('users_df', users_df)]:
    missing = df_check.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) == 0:
        print(f"  {name}: 无缺失值 ✓")
    else:
        for col, cnt in missing.items():
            print(f"  {name}.{col}: {cnt} 个缺失值 (待处理)")

# 5. 数据规模
print("\n【5. 数据规模】")
print(f"  orders_df: {orders_df.shape[0]} 行 × {orders_df.shape[1]} 列")
print(f"  products_df: {products_df.shape[0]} 行 × {products_df.shape[1]} 列")
print(f"  users_df: {users_df.shape[0]} 行 × {users_df.shape[1]} 列")

print("\n" + "=" * 60)
print("除 payment_amount 外，所有数据质量问题已修复 ✓")
print("payment_amount 将在合表后用 quantity * price 填充")
print("=" * 60)
```

这份清洗报告清晰地展示了每项检查的结果。你应该看到：重复数据为 0、日期格式已统一、异常值已截断、`users_df` 的缺失值已填充。唯一剩余的问题是 `orders_df` 的 `payment_amount`，我们已经计划好在合表后处理。

到这里，数据清洗的工作基本完成。让我们进入下一个阶段——数据转换与特征工程。

<!-- #region -->
## Section 4: 数据转换与特征工程

清洗完的数据已经"干净"了，但它们仍然分散在三张表中，字段类型可能不对，也缺少一些对分析有用的衍生指标。在这一节中，我们要完成三件事：

1. **合并多张表**：把分散的信息汇聚到一张宽表中
2. **转换数据类型**：确保每个字段的类型正确
3. **特征工程**：从现有字段中提取新的、有业务含义的特征

**特征工程**（Feature Engineering）是数据科学中最具创造力的环节。好的特征可以让简单的模型产生出色的结果，而差的特征会让复杂的模型也束手无策。虽然我们目前做的是描述性分析而非建模，但构造有意义的衍生指标同样会让分析更加深入。


### 4.1 多表合并

目前我们有三张独立的表：

- `orders_df`：订单信息，知道谁买了什么、买了多少
- `products_df`：商品信息，知道商品的名称、类别、价格、成本
- `users_df`：用户信息，知道用户的性别、年龄、城市、会员等级

如果你想回答"不同年龄段的用户偏好购买哪类商品"这样的问题，你需要同时用到三张表的信息。这就是为什么我们需要**表合并**。

让我们分两步合并：先把订单和商品关联起来，再把用户信息加进去。

**第一步：合并 orders_df 和 products_df**
<!-- #endregion -->

```python
# 合并订单表和商品表
df = orders_df.merge(products_df, on='product_id', how='left')
print(f"合并后: {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"\n新增的列: {[col for col in df.columns if col not in orders_df.columns]}")
print(df.head(3))
```

`merge()` 函数通过 `on='product_id'` 参数，将两张表中 `product_id` 相同的行匹配在一起。`how='left'` 表示以左表（`orders_df`）为基准，即使某些订单的 `product_id` 在 `products_df` 中找不到对应的商品，也保留这些订单行（对应的商品信息会显示为 NaN）。

**第二步：合并用户信息**

```python
# 继续合并用户表
df = df.merge(users_df, on='user_id', how='left')
print(f"合并后: {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"\n新增的列: {[col for col in df.columns if col not in orders_df.columns and col not in products_df.columns]}")
print(df.head(3))
```

现在 `df` 这张宽表包含了订单、商品、用户三方面的完整信息。让我们确认一下合并结果。

```python
# 检查合并后的数据
print("合并后的所有列：")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")
print(f"\n总行数: {df.shape[0]}")
print(f"总列数: {df.shape[1]}")
```

<!-- #region -->
> 💡 **小贴士**：`merge()` 的 `how` 参数决定了合并方式，可以用集合的交集和并集来理解：
> - `how='inner'`：取**交集**，只保留两张表中都有匹配的行。如果订单中的某个 `product_id` 在商品表中找不到，这条订单会被丢弃。
> - `how='left'`：以**左表为基准**，左表的所有行都保留，右表没有匹配的部分填 NaN。
> - `how='right'`：以**右表为基准**，右表的所有行都保留，左表没有匹配的部分填 NaN。
> - `how='outer'`：取**并集**，两张表的所有行都保留，没有匹配的部分填 NaN。
>
> 在大多数业务场景中，`left` 是最安全的选择——你不想因为商品表缺少某个商品的信息就丢掉一整条订单。

> **扩展阅读：pd.merge vs join vs concat**
>
> pandas 提供了三种合并数据的方式，初学者容易混淆，其实它们各有擅长的场景：
>
> 1. **`pd.merge()`**：基于列值做关联合并，类似 SQL 中的 JOIN。适合根据共同字段（如 product_id、user_id）合并不同来源的数据表。这是最常用的合并方式。
>
> 2. **`df.join()`**：基于索引做合并。如果你的 DataFrame 已经把关联键设为了索引，用 `join()` 会更简洁。本质上 `join()` 是 `merge()` 的一个便捷封装。
>
> 3. **`pd.concat()`**：将多个 DataFrame 沿行方向（纵向堆叠）或列方向（横向拼接）拼在一起。适合合并结构相同的数据（比如把 1 月和 2 月的订单数据上下拼接），不需要基于某个键做匹配。
>
> 简单记忆：需要"关联"用 `merge()`，需要"堆叠"用 `concat()`。


### 4.2 填充剩余缺失值

现在我们有了合并后的宽表，可以回过头来处理之前搁置的 `payment_amount` 缺失值了。
<!-- #endregion -->

```python
# 查看 payment_amount 当前的缺失情况
payment_missing = df['payment_amount'].isnull().sum()
print(f"payment_amount 缺失值数量: {payment_missing}")
print(f"payment_amount 缺失比例: {payment_missing / len(df) * 100:.2f}%")
```

合并之后，我们可以用 `quantity * price` 来估算缺失的支付金额。这个逻辑很合理：支付金额应该等于购买数量乘以商品单价。

```python
# 用 quantity * price 填充 payment_amount 的缺失值
df['payment_amount'] = df['payment_amount'].fillna(df['quantity'] * df['price'])

# 验证填充结果
remaining_missing = df['payment_amount'].isnull().sum()
print(f"填充后 payment_amount 缺失值: {remaining_missing}")
```

```python
# 全面验证：检查所有列的缺失值
all_missing = df.isnull().sum()
all_missing = all_missing[all_missing > 0]
if len(all_missing) == 0:
    print("所有缺失值已处理完毕 ✓")
else:
    print("以下列仍有缺失值：")
    print(all_missing)
```

<!-- #region -->
太好了！到这里，所有的缺失值都已经处理完毕。我们的数据终于"干净"又"完整"了。


### 4.3 日期类型转换

虽然日期的格式已经统一了，但 `order_date` 和 `register_date` 目前仍然是字符串类型（`object`）。让我们把它们转换为 pandas 的 **datetime** 类型。
<!-- #endregion -->

```python
# 查看当前的数据类型
print("转换前的类型：")
print(f"  order_date: {df['order_date'].dtype}")
print(f"  register_date: {df['register_date'].dtype}")
```

```python
# 转换为 datetime 类型
df['order_date'] = pd.to_datetime(df['order_date'])
df['register_date'] = pd.to_datetime(df['register_date'])

# 验证转换结果
print("转换后的类型：")
print(f"  order_date: {df['order_date'].dtype}")
print(f"  register_date: {df['register_date'].dtype}")
```

为什么要做这个类型转换？因为字符串类型的日期只是"看起来像日期"，pandas 并不知道它是日期。转换为 datetime 类型后，你才能使用 pandas 提供的丰富的时间操作功能：

- 提取年、月、日、星期等时间成分
- 计算两个日期之间的时间差
- 按月份、季度等进行分组聚合
- 对时间范围进行筛选（比如"只看 2024 年 Q1 的订单"）

```python
# 转换后可以轻松做时间操作，比如查看订单的时间范围
print(f"\n订单时间范围: {df['order_date'].min()} 至 {df['order_date'].max()}")
print(f"用户注册时间范围: {df['register_date'].min()} 至 {df['register_date'].max()}")
```

### 4.4 提取时间特征

有了 datetime 类型的日期列，我们可以从中提取出多个有业务含义的**时间特征**。这些特征在后续的分析和可视化中非常有用。

```python
# 从 order_date 中提取时间特征
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['weekday'] = df['order_date'].dt.dayofweek        # 0=周一, 6=周日
df['day_of_week_name'] = df['order_date'].dt.day_name()  # 英文星期名

print("新增的时间特征：")
print(df[['order_date', 'year', 'month', 'weekday', 'day_of_week_name']].head(8))
```

让我们理解每个特征的业务含义：

| 特征 | 含义 | 业务用途 |
|------|------|----------|
| `year` | 订单年份 | 年度趋势分析、同比增长计算 |
| `month` | 订单月份（1-12） | 月度趋势分析、季节性分析 |
| `weekday` | 星期几（0=周一, 6=周日） | 工作日 vs 周末的消费差异分析 |
| `day_of_week_name` | 星期名称（英文） | 用于可视化时显示更友好的标签 |

这些特征看似简单，但在实际分析中价值很大。比如你可能会发现：周末的客单价比工作日高，或者每年 11 月（双十一）的订单量会出现明显的峰值。

```python
# 快速验证：查看各月份的订单分布
print("\n各月份订单数量：")
print(df['month'].value_counts().sort_index())
```

```python
# 快速验证：查看各星期的订单分布
print("\n各星期订单数量：")
weekday_counts = df['day_of_week_name'].value_counts()
# 按正确的星期顺序排列
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in day_order:
    if day in weekday_counts.index:
        print(f"  {day}: {weekday_counts[day]}")
```

### 4.5 计算业务指标

原始数据中的字段是"记录性"的——它们记录了发生了什么事实。但真正能驱动业务决策的是**衍生指标**。让我们基于现有字段计算一些关键的业务指标。

```python
# 计算核心业务指标
df['revenue'] = df['payment_amount']                    # 收入（语义重命名）
df['total_cost'] = df['cost'] * df['quantity']          # 总成本
df['profit'] = df['revenue'] - df['total_cost']         # 利润
df['profit_rate'] = df['profit'] / df['revenue']        # 利润率

print("新增的业务指标：")
print(df[['revenue', 'total_cost', 'profit', 'profit_rate']].head(8))
```

让我们理解每个指标：

- **`revenue`（收入）**：就是 `payment_amount`，我们给它起了一个更具业务语义的名字。在后续分析中，说"收入"比说"支付金额"更直观。

- **`total_cost`（总成本）**：`cost`（单品成本）乘以 `quantity`（购买数量）。注意这里的 `cost` 来自 `products_df`，是商品的进货成本或生产成本。

- **`profit`（利润）**：收入减去成本。这是衡量每笔订单赚了多少钱的最直接指标。

- **`profit_rate`（利润率）**：利润占收入的比例。它消除了金额大小的影响，让你能够公平地比较不同价位商品的盈利能力。一个售价 1000 元、利润 200 元的商品和一个售价 100 元、利润 30 元的商品，谁更赚钱？看利润率就知道了（前者 20%，后者 30%）。

```python
# 查看利润率的分布
print("profit_rate 的描述统计：")
print(df['profit_rate'].describe())
```

```python
# 查看利润率的分布范围
print(f"\n利润率范围: {df['profit_rate'].min():.2%} ~ {df['profit_rate'].max():.2%}")
print(f"平均利润率: {df['profit_rate'].mean():.2%}")
print(f"中位数利润率: {df['profit_rate'].median():.2%}")
```

```python
# 查看是否有亏损订单（利润率为负的情况）
loss_orders = df[df['profit'] < 0]
print(f"\n亏损订单数量: {len(loss_orders)}")
if len(loss_orders) > 0:
    print(f"亏损订单占比: {len(loss_orders) / len(df) * 100:.2f}%")
    print("亏损订单示例：")
    print(loss_orders[['order_id', 'product_name', 'revenue', 'total_cost', 'profit', 'profit_rate']].head(5))
```

<!-- #region -->
如果没有亏损订单，那很好；如果有，就值得深入调查——是某些商品定价有问题，还是促销活动导致的临时亏损？这种洞察在后续分析中会非常有价值。


### 4.6 用户特征工程

除了订单维度的特征，让我们从用户维度也提取一些有意义的特征。

**年龄分箱**

`age` 是一个连续变量，直接使用它做分组分析会产生太多组别。我们可以用 `pd.cut()` 将连续的年龄值分成几个有业务含义的区间。
<!-- #endregion -->

```python
# 将年龄分为 5 个区间
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 25, 35, 45, 55, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '56+']
)

print("年龄分组分布：")
print(df['age_group'].value_counts().sort_index())
```

`pd.cut()` 的工作原理：
- `bins=[0, 25, 35, 45, 55, 100]` 定义了分箱的边界。它会创建 5 个区间：(0,25]、(25,35]、(35,45]、(45,55]、(55,100]。
- `labels` 为每个区间指定一个可读的标签。
- 默认情况下，区间是**左开右闭**的，即 (0, 25] 表示大于 0 且小于等于 25。

这种分箱方式在业务分析中非常常见。比如你可能会发现，26-35 岁的用户是消费主力，而 56+ 的用户虽然人数少但客单价更高。

```python
# 查看各年龄组的平均消费
print("\n各年龄组的平均消费金额：")
age_spending = df.groupby('age_group')['revenue'].mean()
print(age_spending.round(2))
```

**用户活跃天数**

另一个有价值的用户特征是**活跃天数**——从用户注册到下单之间经过了多少天。这个指标能反映用户的忠诚度和平台粘性。

```python
# 计算用户活跃天数（订单日期 - 注册日期）
df['user_tenure_days'] = (df['order_date'] - df['register_date']).dt.days

print("用户活跃天数的描述统计：")
print(df['user_tenure_days'].describe())
```

```python
# 查看活跃天数的分布
print(f"\n活跃天数范围: {df['user_tenure_days'].min()} ~ {df['user_tenure_days'].max()} 天")
print(f"平均活跃天数: {df['user_tenure_days'].mean():.0f} 天")
print(f"中位数活跃天数: {df['user_tenure_days'].median():.0f} 天")
```

`(df['order_date'] - df['register_date'])` 计算两个 datetime 列的差值，结果是 `Timedelta` 类型。`.dt.days` 将 `Timedelta` 转换为天数的整数值。

如果你发现某些 `user_tenure_days` 是负数，说明有用户的注册日期晚于订单日期——这可能是数据录入错误，值得关注。

```python
# 检查是否有异常的负值
negative_tenure = df[df['user_tenure_days'] < 0]
if len(negative_tenure) > 0:
    print(f"\n⚠ 发现 {len(negative_tenure)} 条记录的活跃天数为负值（注册日期晚于订单日期）")
    print(negative_tenure[['user_id', 'order_date', 'register_date', 'user_tenure_days']].head())
else:
    print("\n所有记录的活跃天数均为正值 ✓")
```

### 4.7 数据转换小结

所有的数据清洗和特征工程工作都完成了。让我们来看看最终成果。

```python
# 查看最终的数据结构
print("=" * 60)
print("         最 终 数 据 结 构")
print("=" * 60)
print(df.info())
```

```python
# 列出所有列名
print("\n所有列名：")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")
print(f"\n共 {len(df.columns)} 个字段")
```

让我们把这些列按来源和含义分个类：

```python
# 按来源分类展示各列
original_order_cols = ['order_id', 'user_id', 'product_id', 'quantity',
                       'order_date', 'payment_amount', 'order_status', 'payment_method']
original_product_cols = ['product_name', 'category', 'price', 'cost']
original_user_cols = ['gender', 'age', 'city', 'register_date', 'membership_level']
derived_time_cols = ['year', 'month', 'weekday', 'day_of_week_name']
derived_business_cols = ['revenue', 'total_cost', 'profit', 'profit_rate']
derived_user_cols = ['age_group', 'user_tenure_days']

print("\n字段分类：")
print(f"  订单原始字段 ({len(original_order_cols)}): {original_order_cols}")
print(f"  商品原始字段 ({len(original_product_cols)}): {original_product_cols}")
print(f"  用户原始字段 ({len(original_user_cols)}): {original_user_cols}")
print(f"  时间衍生字段 ({len(derived_time_cols)}): {derived_time_cols}")
print(f"  业务衍生字段 ({len(derived_business_cols)}): {derived_business_cols}")
print(f"  用户衍生字段 ({len(derived_user_cols)}): {derived_user_cols}")
```

```python
# 查看最终数据的前几行
print("\n最终数据预览（前 5 行）：")
# 选择关键列展示，避免列太多显示不全
key_cols = ['order_id', 'product_name', 'category', 'quantity', 'revenue',
            'profit', 'profit_rate', 'age_group', 'city', 'membership_level']
print(df[key_cols].head())
```

```python
# 最终数据质量检查
print("\n最终数据质量检查：")
print(f"  总行数: {len(df)}")
print(f"  总列数: {len(df.columns)}")
print(f"  缺失值总计: {df.isnull().sum().sum()}")
print(f"  重复行数: {df.duplicated().sum()}")
print(f"  数据类型概览:")
print(f"    数值型: {len(df.select_dtypes(include='number').columns)} 列")
print(f"    字符串型: {len(df.select_dtypes(include='object').columns)} 列")
print(f"    日期型: {len(df.select_dtypes(include='datetime').columns)} 列")
print(f"    分类型: {len(df.select_dtypes(include='category').columns)} 列")
```

最后，让我们把清洗转换后的数据保存到文件，方便后续分析使用。

```python
# 保存清洗后的数据
df.to_csv('orders_cleaned.csv', index=False)
print(f"\n数据已保存到 orders_cleaned.csv")
print(f"文件包含 {len(df)} 行 × {len(df.columns)} 列")
```

让我们总结一下这两个 Section 中做了什么：

```python
print("=" * 60)
print("         下一节 总 结")
print("=" * 60)
print("""
【数据清洗】
  ✓ 删除了约 50 条重复订单
  ✓ 统一了约 30 条日期格式（'/' → '-'）
  ✓ 截断了约 10 个异常的 quantity 值（> 10 → 10）
  ✓ 填充了 users_df 的缺失值（age→中位数, city/gender→'未知'）
  ✓ 填充了 payment_amount 的缺失值（quantity × price）

【数据转换与特征工程】
  ✓ 合并了三张表为一张宽表
  ✓ 转换了日期列的数据类型（object → datetime）
  ✓ 提取了时间特征：year, month, weekday, day_of_week_name
  ✓ 计算了业务指标：revenue, total_cost, profit, profit_rate
  ✓ 构造了用户特征：age_group, user_tenure_days
  ✓ 保存了清洗后的数据到 CSV 文件

从三张"脏"表到一张干净的宽表，数据已经为下一步的
探索性数据分析（EDA）和可视化做好了准备。
""")
```

在 后续章节 中，我们将利用这张清洗好的宽表，通过分组聚合和可视化来发现数据中隐藏的业务洞察。那才是数据分析最有趣的部分——让数据"说话"。


## Section 5: 数据聚合与统计分析

经过前面的数据清洗和转换，我们的 `df` 已经是一张干净、完整的宽表了。现在，是时候从数据中提炼出真正有价值的信息了。

在实际的数据分析工作中，原始数据就像散落在地上的拼图碎片——你需要把它们按照某种规则分组、汇总、计算，才能看到完整的画面。这就是**数据聚合**（Data Aggregation）要做的事情。

在开始分析之前，让我们先过滤出已完成的订单。很多业务分析只关心真正完成的交易——已取消和已退款的订单虽然也有分析价值，但放在销售额统计中会造成误导。

下面这段代码从 `df` 中筛选出订单状态为"已完成"的记录，创建一个独立的副本用于后续分析：

```python
completed_df = df[df['order_status'] == '已完成'].copy()
print(f"已完成订单数: {len(completed_df)}")
print(f"占总订单比例: {len(completed_df) / len(df):.1%}")
```

你会看到已完成的订单大约占总订单的 80%，这是我们后续分析的主要数据集。当然，在某些场景下（比如分析退款率），我们还会用到完整的 `df`。

### 5.1 基础聚合：groupby 入门

pandas 中最强大的聚合工具是 `groupby()`。它的工作原理可以用三个词概括：**拆分-应用-合并**（Split-Apply-Combine）：

1. **拆分**（Split）：按照某个列的值，把数据拆分成多个小组
2. **应用**（Apply）：对每个小组分别执行计算（求和、平均、计数等）
3. **合并**（Combine）：把各组的计算结果合并成一个新的表格

让我们从最简单的例子开始——按品类计算总销售额：

```python
category_revenue = completed_df.groupby('category')['revenue'].sum()
print(category_revenue)
print(f"\n总销售额: {category_revenue.sum():,.2f}")
```

这段代码做了什么？`groupby('category')` 把数据按品类拆成 5 组（电子产品、服装、食品、家居、图书），然后对每组的 `revenue` 列求和。结果是一个 Series，索引是品类名，值是对应的总销售额。

但在实际分析中，你往往不只想看一个指标。让我们用 `.agg()` 方法同时计算多个指标：

```python
category_stats = completed_df.groupby('category').agg({
    'revenue': 'sum',
    'order_id': 'count',
    'profit': 'sum'
})

# 重命名列，让结果更易读
category_stats.columns = ['总销售额', '订单数', '总利润']

# 按总销售额降序排列
category_stats = category_stats.sort_values('总销售额', ascending=False)

# 添加利润率列
category_stats['利润率'] = (category_stats['总利润'] / category_stats['总销售额'] * 100).round(1)

print(category_stats)
print(f"\n销售额最高的品类: {category_stats.index[0]}")
print(f"利润率最高的品类: {category_stats['利润率'].idxmax()}")
```

输出会展示每个品类的销售全貌。你可能会发现，销售额最高的品类不一定利润率最高——这就是多维度分析的价值。

> 💡 **小贴士**：`agg()` 支持多种写法。除了上面的字典写法，你还可以用列表 `['sum', 'mean', 'count']` 对同一列计算多个指标，或者用**命名聚合**（Named Aggregation）来直接指定结果列名：
> ```python
> completed_df.groupby('category').agg(
>     总销售额=('revenue', 'sum'),
>     平均客单价=('revenue', 'mean'),
>     订单数=('order_id', 'count')
> )
> ```

让我们再来看一个格式化输出的例子，让数字更易于阅读：

```python
# 格式化输出品类统计
print("=" * 60)
print(f"{'品类':^10} {'销售额':>12} {'订单数':>8} {'利润率':>8}")
print("-" * 60)
for category, row in category_stats.iterrows():
    print(f"{category:^10} {row['总销售额']:>12,.0f} {row['订单数']:>8.0f} {row['利润率']:>7.1f}%")
print("=" * 60)
```

这种格式化输出在写报告或给领导展示数据时非常实用。

### 5.2 月度销售趋势

了解销售的时间趋势是商业分析中最基础也最重要的任务之一。让我们按月汇总销售数据，看看是否存在明显的波动或趋势。

下面的代码按月份进行聚合，计算每月的关键指标：

```python
monthly = completed_df.groupby('month').agg(
    月销售额=('revenue', 'sum'),
    月订单量=('order_id', 'count'),
    月利润=('profit', 'sum'),
    月均客单价=('revenue', 'mean')
).reset_index()

print(monthly.to_string(index=False))
```

现在计算月均指标和环比增长率。**环比增长率**是指相邻两个月之间的变化百分比，是衡量业务健康度的重要指标：

```python
# 计算环比增长率
monthly['销售额环比'] = monthly['月销售额'].pct_change()
monthly['订单量环比'] = monthly['月订单量'].pct_change()

# 格式化输出
print("月度销售趋势:")
print("-" * 80)
for _, row in monthly.iterrows():
    growth = f"{row['销售额环比']:+.1%}" if pd.notna(row['销售额环比']) else "  N/A"
    print(f"  {int(row['month']):>2}月  "
          f"销售额: {row['月销售额']:>12,.0f}  "
          f"订单量: {row['月订单量']:>5.0f}  "
          f"客单价: {row['月均客单价']:>8,.0f}  "
          f"环比: {growth}")
```

`pct_change()` 是 pandas 提供的计算环比变化率的便捷方法。第一个月没有前一个月的数据做对比，所以会显示 NaN。

让我们找出销售额最高和最低的月份：

```python
best_month = monthly.loc[monthly['月销售额'].idxmax()]
worst_month = monthly.loc[monthly['月销售额'].idxmin()]

print(f"销售额最高月份: {int(best_month['month'])}月, 销售额: {best_month['月销售额']:,.0f}")
print(f"销售额最低月份: {int(worst_month['month'])}月, 销售额: {worst_month['月销售额']:,.0f}")
print(f"最高/最低比值: {best_month['月销售额'] / worst_month['月销售额']:.2f}x")
```

在电商数据中，销售额通常会呈现**季节性**（Seasonality）特征。比如 11 月（双十一）和 6 月（618）可能出现高峰，而春节期间可能有所下降。虽然我们这份模拟数据不一定完全符合真实的电商节奏，但你可以尝试观察是否有类似的波动。

让我们进一步计算季度汇总，从更宏观的视角看趋势：

```python
# 按季度汇总
monthly['quarter'] = ((monthly['month'] - 1) // 3 + 1).astype(int)
quarterly = monthly.groupby('quarter').agg({
    '月销售额': 'sum',
    '月订单量': 'sum'
})
quarterly.columns = ['季度销售额', '季度订单量']
quarterly['季度客单价'] = quarterly['季度销售额'] / quarterly['季度订单量']

print("\n季度汇总:")
print(quarterly.round(0))
```

### 5.3 品类深度分析

接下来让我们深入到品类维度，做一个更全面的分析。

首先，汇总每个品类的核心指标：

```python
category_deep = completed_df.groupby('category').agg(
    销售额=('revenue', 'sum'),
    订单数=('order_id', 'count'),
    平均客单价=('revenue', 'mean'),
    总利润=('profit', 'sum'),
    平均利润率=('profit_rate', 'mean'),
    不同商品数=('product_id', 'nunique'),
    不同用户数=('user_id', 'nunique')
).round(2)

category_deep = category_deep.sort_values('销售额', ascending=False)
print(category_deep)
```

`nunique()` 是一个非常实用的聚合函数，它统计的是**不重复值的数量**。用它来计算"有多少种不同的商品"和"有多少不同的用户"非常方便。

现在让我们找出每个品类中销售最好的 Top 5 商品：

```python
print("各品类 Top 5 商品:")
print("=" * 70)

for category in completed_df['category'].unique():
    cat_data = completed_df[completed_df['category'] == category]
    top5 = cat_data.groupby('product_name').agg(
        销售额=('revenue', 'sum'),
        销量=('quantity', 'sum')
    ).sort_values('销售额', ascending=False).head(5)

    print(f"\n【{category}】")
    for i, (name, row) in enumerate(top5.iterrows(), 1):
        print(f"  {i}. {name:20s}  销售额: {row['销售额']:>10,.0f}  销量: {row['销量']:>5.0f}")
```

品类之间的对比往往需要从多个维度来看。让我们用 `pd.pivot_table` 创建一个**品类-月份交叉表**，看看不同品类在不同月份的销售表现：

```python
# 创建品类-月份的交叉表
category_month_pivot = pd.pivot_table(
    completed_df,
    values='revenue',
    index='category',
    columns='month',
    aggfunc='sum',
    fill_value=0
)

# 格式化输出
print("品类-月份销售额交叉表:")
print(category_month_pivot.round(0).to_string())
```

**透视表**（Pivot Table）是数据分析中的利器，它把"长格式"的数据重新组织成"宽格式"的交叉表。你在 Excel 中可能用过数据透视表，pandas 的 `pd.pivot_table()` 功能更为强大——你可以指定多个聚合函数、多层索引、填充缺失值等。

让我们再看一个用透视表做品类间对比分析的例子：

```python
# 品类-支付方式的交叉分析
category_payment = pd.pivot_table(
    completed_df,
    values='order_id',
    index='category',
    columns='payment_method',
    aggfunc='count',
    fill_value=0
)

# 转为百分比
category_payment_pct = category_payment.div(category_payment.sum(axis=1), axis=0) * 100
print("\n品类-支付方式占比 (%):")
print(category_payment_pct.round(1).to_string())
```

这个交叉表可以帮助你了解不同品类的用户是否有不同的支付偏好——比如电子产品用户是否更倾向使用信用卡，而食品用户是否更喜欢移动支付。

### 5.4 用户行为分析

理解用户行为是精细化运营的基础。让我们从多个维度来刻画用户画像。

首先，按**会员等级**分析消费行为：

```python
membership_stats = completed_df.groupby('membership_level').agg(
    用户数=('user_id', 'nunique'),
    订单数=('order_id', 'count'),
    总消费=('revenue', 'sum'),
    平均客单价=('revenue', 'mean'),
    平均利润=('profit', 'mean')
).round(2)

# 计算人均订单数和人均消费
membership_stats['人均订单数'] = (membership_stats['订单数'] / membership_stats['用户数']).round(1)
membership_stats['人均消费'] = (membership_stats['总消费'] / membership_stats['用户数']).round(0)

print("按会员等级分析:")
print(membership_stats)
```

你可以观察到，会员等级越高的用户，人均消费和人均订单数通常也越高。这正是会员体系发挥作用的体现——高等级会员往往是忠诚度更高的核心用户。

接下来，按**年龄段**分析消费偏好：

```python
age_stats = completed_df.groupby('age_group').agg(
    用户数=('user_id', 'nunique'),
    订单数=('order_id', 'count'),
    总消费=('revenue', 'sum'),
    平均客单价=('revenue', 'mean')
).round(2)

age_stats['人均消费'] = (age_stats['总消费'] / age_stats['用户数']).round(0)

print("按年龄段分析:")
print(age_stats)
```

让我们进一步看看不同年龄段的品类偏好：

```python
# 年龄段-品类的交叉分析
age_category = pd.pivot_table(
    completed_df,
    values='revenue',
    index='age_group',
    columns='category',
    aggfunc='sum',
    fill_value=0
)

# 转为行百分比，看每个年龄段的消费结构
age_category_pct = age_category.div(age_category.sum(axis=1), axis=0) * 100
print("\n各年龄段的品类消费占比 (%):")
print(age_category_pct.round(1).to_string())
```

这个交叉表能揭示一些有趣的消费模式——比如年轻人可能在电子产品和服装上花费更多，而年长的用户可能更偏向家居和食品。

按**城市**分析消费情况：

```python
city_stats = completed_df.groupby('city').agg(
    用户数=('user_id', 'nunique'),
    订单数=('order_id', 'count'),
    总消费=('revenue', 'sum')
).round(0)

city_stats['人均消费'] = (city_stats['总消费'] / city_stats['用户数']).round(0)
city_stats = city_stats.sort_values('总消费', ascending=False)

print("按城市分析 (按总消费降序):")
print(city_stats)
```

最后，找出**Top 10 高价值用户**：

```python
top_users = completed_df.groupby('user_id').agg(
    订单数=('order_id', 'count'),
    总消费=('revenue', 'sum'),
    总利润=('profit', 'sum'),
    首次购买=('order_date', 'min'),
    最近购买=('order_date', 'max'),
    常购品类=('category', lambda x: x.value_counts().index[0])
).sort_values('总消费', ascending=False)

print("Top 10 高价值用户:")
print(top_users.head(10).to_string())
```

这里的 `lambda x: x.value_counts().index[0]` 是一个自定义聚合函数，它返回出现次数最多的品类——也就是该用户最常购买的品类。这种自定义聚合的灵活性是 pandas 的强���之处。

### 5.5 相关性分析

在做完各维度的汇总分析后，让我们换一个视角——看看数值变量之间是否存在**相关性**（Correlation）。

**相关系数**取值在 -1 到 1 之间：
- 接近 1：强正相关（一个变量增大，另一个也倾向增大）
- 接近 -1：强负相关（一个变量增大，另一个倾向减小）
- 接近 0：没有线性相关关系

让我们计算几个关键数值列之间的相关系数矩阵：

```python
corr_cols = ['quantity', 'revenue', 'profit', 'age', 'user_tenure_days']
corr_matrix = completed_df[corr_cols].corr()

print("相关系数矩阵:")
print(corr_matrix.round(3).to_string())
```

让我们逐对解读一些有意义的相关关系：

```python
print("\n关键相关系数解读:")
print(f"  revenue vs profit:        {corr_matrix.loc['revenue', 'profit']:.3f}  — 销售额与利润的关系")
print(f"  revenue vs quantity:      {corr_matrix.loc['revenue', 'quantity']:.3f}  — 销售额与数量的关系")
print(f"  age vs revenue:           {corr_matrix.loc['age', 'revenue']:.3f}  — 年龄与消费金额的关系")
print(f"  user_tenure_days vs revenue: {corr_matrix.loc['user_tenure_days', 'revenue']:.3f}  — 注册天数与消费金额的关系")
```

`revenue` 和 `profit` 之间通常会有较强的正相关，这很容易理解——卖得越多，赚得越多。但 `age` 和消费金额之间的关系就不一定那么明显了。

> 💡 **小贴士**：**相关性不等于因果性**（Correlation does not imply causation）。这是数据分析中最重要的原则之一。即使两个变量高度相关，也不能直接断定一个导致了另一个。比如冰淇淋销量和溺水事件高度正相关，但原因是它们都受气温影响，而不是吃冰淇淋导致溺水。在解读相关分析结果时��一定要结合业务逻辑来判断。

### 5.6 RFM 分析（简化版）

**RFM 分析**是客户价值评估中最经典的模型之一，被广泛应用于电商、零售和金融行业。RFM 是三个维度的首字母缩写：

- **R（Recency）**：最近一次消费距今多久？越近说明用户越活跃
- **F（Frequency）**：消费了多少次？次数越多说明越忠诚
- **M（Monetary）**：总共消费了多少钱？金额越大说明价值越高

让我们来实现一个简化版的 RFM 分析。

首先，设定一个分析基准日期，并计算每个用户的 R、F、M 值：

```python
# 设定分析基准日期为数据中最大日期的下一天
analysis_date = completed_df['order_date'].max() + pd.Timedelta(days=1)
print(f"分析基准日期: {analysis_date.date()}")

# 计算每个用户的 RFM 值
rfm = completed_df.groupby('user_id').agg(
    R=('order_date', lambda x: (analysis_date - x.max()).days),  # 最近一次购买距今天数
    F=('order_id', 'count'),                                      # 购买次数
    M=('revenue', 'sum')                                           # 总消费金额
).round(2)

print(f"\nRFM 表 (共 {len(rfm)} 个用户):")
print(rfm.describe().round(1))
```

输出中的 `describe()` 可以让你快速了解 R、F、M 三个维度的分布情况——均值、中位数、标准差等。

接下来，用 `pd.qcut()` 将每个维度分成 4 个等级（1-4 分）。注意 R 的评分逻辑是反转的——距今天数越少（越近），得分越高：

```python
# 用 qcut 分箱，分成 4 个等级
# R 分数：天数越小越好，所以用 ascending=False 的逻辑
rfm['R_score'] = pd.qcut(rfm['R'], q=4, labels=[4, 3, 2, 1]).astype(int)
# F 分数：频次越高越好
rfm['F_score'] = pd.qcut(rfm['F'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
# M 分数：金额越大越好
rfm['M_score'] = pd.qcut(rfm['M'], q=4, labels=[1, 2, 3, 4]).astype(int)

# 生成 RFM 组合标签
rfm['RFM_label'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

print("RFM 分箱结果示例:")
print(rfm.head(10).to_string())
```

`pd.qcut()` 会根据数据分位数来分箱，保证每个箱中的数据量大致相等。对于 F（频次），由于可能存在很多相同的值导致分箱边界重复，我们用 `rank(method='first')` 先做排名再分箱，避免报错。

现在，让我们根据 RFM 得分来识别不同类型的用户：

```python
# 定义用户分类规则
def classify_customer(row):
    r, f, m = row['R_score'], row['F_score'], row['M_score']
    if r >= 3 and f >= 3 and m >= 3:
        return '高价值用户'
    elif r >= 3 and f >= 3 and m < 3:
        return '忠诚用户'
    elif r >= 3 and f < 3 and m >= 3:
        return '潜力用户'
    elif r < 3 and f >= 3 and m >= 3:
        return '流失风险(高价值)'
    elif r < 3 and f >= 3 and m < 3:
        return '流失风险(一般)'
    elif r >= 3 and f < 3 and m < 3:
        return '新用户/低频用户'
    elif r < 3 and f < 3 and m >= 3:
        return '沉睡用户'
    else:
        return '低价值用户'

rfm['用户类型'] = rfm.apply(classify_customer, axis=1)

# 统计各类用户的数量和占比
user_type_stats = rfm['用户类型'].value_counts()
user_type_pct = (user_type_stats / len(rfm) * 100).round(1)

print("用户分类统计:")
print("-" * 40)
for utype, count in user_type_stats.items():
    pct = user_type_pct[utype]
    print(f"  {utype:15s}  {count:>5d} 人  ({pct}%)")
```

让我们进一步查看每种类型用户的平均 RFM 值，验证分类是否合理：

```python
# 各类型用户的平均 RFM 指标
type_rfm_avg = rfm.groupby('用户类型').agg(
    平均R天数=('R', 'mean'),
    平均F次数=('F', 'mean'),
    平均M金额=('M', 'mean'),
    用户数=('R', 'count')
).round(1)

type_rfm_avg = type_rfm_avg.sort_values('平均M金额', ascending=False)
print("\n各类型用户的平均 RFM:")
print(type_rfm_avg.to_string())
```

从结果中可以看出，"高价值用户"的特征是最近有购买（R小）、购买频次高（F大）、消费金额大（M大），这些用户是企业最需要维护的核心客户。而"流失风险(高价值)"用户曾经消费较多但近期没有购买，需要通过召回活动来挽留。

> **扩展阅读：RFM 分析在电商中的应用** —— RFM 模型的真正价值在于驱动**精准营销**。针对不同类型的用户，可以制定差异化的营销策略：高价值用户可以获得专属优惠和 VIP 服务；流失风险用户需要定向发送召回优惠券；潜力用户可以通过交叉推荐来提升购买频次。在工业级应用中，RFM 通常会与机器学习模型（如聚类分析）结合使用，实现更精细的用户分群。阿里云的机器学习平台 PAI 就提供了内置的 RFM 分析组件，可以在可视化界面中快速完成用户分群。


## Section 6: 数据可视化

数据分析如果只停留在数字层面，很难让人快速抓住重点。而一张好的图表可以在几秒钟内传达出数据背后的故事。这就是为什么**数据可视化**（Data Visualization）是每个数据分析师的必备技能。

在 Section 5 中，我们已经计算了大量的汇总数据。现在，让我们把它们"画"出来。

### 6.1 可视化基础

在 Python 的可视化生态中，**matplotlib** 和 **seaborn** 是最常用的两个库。它们的关系是这样的：

- **matplotlib** 是底层绑定库，功能全面但语法较为繁琐——你可以把它理解为"画板"和"画笔"
- **seaborn** 是基于 matplotlib 的高级封装，提供了更简洁的 API 和更美观的默认样式——你可以把它理解为"画笔套装"，帮你预调了好看的颜色

在动手画图之前，让我们先理解两个核心概念：

- **Figure**：整张画布。一个 Figure 可以包含一个或多个子图
- **Axes**：子图（坐标轴区域）。每个 Axes 就是一张独立的图表

下面我们设置全局样式，让后续所有图表都有统一的视觉风格：

```python
# 设置全局样式
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# 定义一个统一的调���板
COLORS = sns.color_palette('Set2', n_colors=8)
print("可视化全局样式已设置完成")
```

`sns.set_style('whitegrid')` 设置了白底带网格线的清爽风格，适合大多数商业分析图表。`Set2` 是一个柔和的配色方案，视觉上比较舒适。

### 6.2 柱状图：品类销售额对比

**柱状图**（Bar Chart）是展示分类数据对比最直观的图表类型。让我们用它来展示各品类的销售额对比。

首先准备数据，然后用 seaborn 的 `barplot` 绑制柱状图：

```python
# 准备品类销售数据（按销售额降序）
cat_revenue = completed_df.groupby('category')['revenue'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(len(cat_revenue)), cat_revenue.values, color=COLORS[:len(cat_revenue)])
ax.set_xticks(range(len(cat_revenue)))
ax.set_xticklabels(cat_revenue.index, fontsize=12)
ax.set_title('各品类销售额对比', fontsize=16, fontweight='bold')
ax.set_xlabel('品类', fontsize=12)
ax.set_ylabel('销售额 (元)', fontsize=12)

# 在柱子上方添加数值标注
for bar_item in bars:
    height = bar_item.get_height()
    ax.text(bar_item.get_x() + bar_item.get_width() / 2., height,
            f'{height:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# 设置 y 轴从 0 开始，上方留出标注空间
ax.set_ylim(0, cat_revenue.max() * 1.15)

plt.tight_layout()
plt.show()
```

这段代码的几个关键点：
- `sort_values(ascending=False)` 让柱子按销售额从高到低排列，读者一眼就能看出谁是第一
- 在柱子顶部添加数值标注，不需要去比对 Y 轴就能读出精确值
- `set_ylim` 留出 15% 的空间给顶部标注，避免数字被截断

让图表"说话"的三个要素：**排序**（按大小排列）、**颜色**（用不同颜色区分）、**标注**（在关键位置标出数值）。

接下来，让我们用**水平柱状图**展示 Top 10 热销商品——当类别标签较长时，水平布局更易于阅读：

```python
# Top 10 商品销售额
top10_products = completed_df.groupby('product_name')['revenue'].sum().nlargest(10)

fig, ax = plt.subplots(figsize=(10, 7))
# 反转顺序，让最大的在最上面
bars = ax.barh(range(len(top10_products)), top10_products.values[::-1], color=COLORS[1])
ax.set_yticks(range(len(top10_products)))
ax.set_yticklabels(top10_products.index[::-1], fontsize=11)
ax.set_title('Top 10 热销商品', fontsize=16, fontweight='bold')
ax.set_xlabel('销售额 (元)', fontsize=12)

# 在条形右侧添加数值
for bar_item in bars:
    width = bar_item.get_width()
    ax.text(width, bar_item.get_y() + bar_item.get_height() / 2.,
            f' {width:,.0f}',
            ha='left', va='center', fontsize=10)

ax.set_xlim(0, top10_products.max() * 1.2)
plt.tight_layout()
plt.show()
```

注意这里用了 `nlargest(10)` 来直接获取前 10 名，比 `sort_values().head(10)` 更简洁。水平柱状图中，我们习惯把最大值放在最上面（`[::-1]` 反转），符合从上到下的阅读习惯。

### 6.3 折线图：月度趋势

**折线图**（Line Chart）是展示时间序列数据的首选图表。让我们绘制月度销售额和订单量的趋势变化。

下面的代码使用**双 Y 轴**（twinx）技巧，在同一张图中同时展示销售额和订单量这两个量纲不同的指标：

```python
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左 Y 轴：销售额（柱状图）
months = monthly['month'].astype(int)
bars = ax1.bar(months, monthly['月销售额'], color=COLORS[0], alpha=0.6, label='销售额')
ax1.set_xlabel('月份', fontsize=12)
ax1.set_ylabel('销售额 (元)', fontsize=12, color=COLORS[0])
ax1.tick_params(axis='y', labelcolor=COLORS[0])
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels([f'{m}月' for m in range(1, 13)])

# 右 Y 轴：订单量（折线图）
ax2 = ax1.twinx()
line = ax2.plot(months, monthly['月订单量'], color=COLORS[3],
                marker='o', linewidth=2.5, markersize=8, label='订单量')
ax2.set_ylabel('订单量', fontsize=12, color=COLORS[3])
ax2.tick_params(axis='y', labelcolor=COLORS[3])

# 标注最高月份
max_rev_month = monthly.loc[monthly['月销售额'].idxmax()]
ax1.annotate(f'峰值: {max_rev_month["月销售额"]:,.0f}',
             xy=(max_rev_month['month'], max_rev_month['月销售额']),
             xytext=(max_rev_month['month'] + 1.5, max_rev_month['月销售额'] * 0.95),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=11, color='red', fontweight='bold')

# 标注最低月份
min_rev_month = monthly.loc[monthly['月销售额'].idxmin()]
ax1.annotate(f'谷值: {min_rev_month["月销售额"]:,.0f}',
             xy=(min_rev_month['month'], min_rev_month['月销售额']),
             xytext=(min_rev_month['month'] + 1.5, min_rev_month['月销售额'] * 1.2),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=11, color='blue', fontweight='bold')

# 合并图例
bars_legend = plt.Rectangle((0, 0), 1, 1, fc=COLORS[0], alpha=0.6)
fig.legend([bars_legend, line[0]], ['销售额', '订单量'],
           loc='upper center', ncol=2, fontsize=11,
           bbox_to_anchor=(0.5, 0.98))

ax1.set_title('月度销售额与订单量趋势', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()
```

这张图包含了丰富的信息量：
- 柱状图展示了每月的销售额绝对值
- 折线图叠加了订单量的走势
- 红色箭头标注了销售额的峰值月��
- 蓝色箭头标注了谷值月份

双 Y 轴的使用需要谨慎——只有当两个指标的趋势确实有对比意义时才推荐使用，否则容易让读者困惑。

### 6.4 饼图与环形图：支付方式分布

**饼图**（Pie Chart）最适合展示"部分占整体的比例"这类数据。让我们看看不同支付方式的使用占比。

先绘制一个标准饼图：

```python
payment_counts = completed_df['payment_method'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 左图：标准饼图
colors_pie = sns.color_palette('pastel', n_colors=len(payment_counts))
wedges, texts, autotexts = axes[0].pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    textprops={'fontsize': 11}
)
for autotext in autotexts:
    autotext.set_fontweight('bold')
axes[0].set_title('支付方式分布（饼图）', fontsize=14, fontweight='bold')

# 右图：环形图（Donut Chart）
wedges2, texts2, autotexts2 = axes[1].pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    pctdistance=0.8,
    textprops={'fontsize': 11},
    wedgeprops=dict(width=0.45)  # 关键参数：控制环的宽度
)
for autotext in autotexts2:
    autotext.set_fontweight('bold')

# 在环形图中央添加文字
axes[1].text(0, 0, f'总订单\n{payment_counts.sum():,}',
             ha='center', va='center', fontsize=14, fontweight='bold')
axes[1].set_title('支付方式分布（环形图）', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
```

环形图和饼图本质上传达的信息一样，但环形图的中空区域可以用来放置总数、标题或图标，视觉上也更现代。

> 💡 **小贴士**：饼图适合展示**3-5 个类别**的占比关系。当类别超过 5-6 个时，小扇区会变得难以区分，此时改用水平柱状图更合适。另外，如果你需要精确对比各部分的大小差异，柱状图也优于饼图，因为人眼对长度的判断比对角度更准确。

### 6.5 散点图：价格与销量的关系

**散点图**（Scatter Plot）是探索两个连续变量之间关系的最佳工具。让我们看看商品价格和总销量之间是否存在某种规律。

首先准备每个商品的汇总数据，然后绘制散点图：

```python
# 准备商品级别的汇总数据
product_stats = completed_df.groupby(['product_name', 'category']).agg(
    总销量=('quantity', 'sum'),
    平均单价=('price', 'mean'),
    总利润=('profit', 'sum')
).reset_index()

fig, ax = plt.subplots(figsize=(12, 8))

# 按品类分色绘制散点
categories = product_stats['category'].unique()
scatter_colors = sns.color_palette('Set2', n_colors=len(categories))

for i, cat in enumerate(categories):
    mask = product_stats['category'] == cat
    cat_data = product_stats[mask]
    scatter = ax.scatter(
        cat_data['平均单价'],
        cat_data['总销量'],
        s=cat_data['总利润'].clip(lower=0) / cat_data['总利润'].clip(lower=0).max() * 300 + 30,
        c=[scatter_colors[i]] * len(cat_data),
        alpha=0.7,
        edgecolors='white',
        linewidths=0.8,
        label=cat
    )

ax.set_title('商品价格 vs 总销量（气泡大小 = 利润）', fontsize=16, fontweight='bold')
ax.set_xlabel('平均单价 (元)', fontsize=12)
ax.set_ylabel('总销量 (件)', fontsize=12)
ax.legend(title='品类', fontsize=10, title_fontsize=11)

plt.tight_layout()
plt.show()
```

在这张散点图中：
- **X 轴** 表示商品的平均单价
- **Y 轴** 表示该商品的总销量
- **颜色** 区分不同的品类
- **气泡大小** 表示利润，利润越大气泡越大

你可能会发现一些有趣的模式：低价商品往往销量更高（比如食品和图书），而高价商品虽然销量较低但单笔利润可能更大（比如电子产品）。这就是散点图能讲述的"故事"。

### 6.6 热力图：品类-月份销售矩阵

**热力图**（Heatmap）用颜色深浅来展示矩阵中数值的大小，特别适合展示交叉表数据。让我们用它来可视化品类在各月份的销售分布。

我们使用 Section 5.3 中创建的 `category_month_pivot` 数据：

```python
# 重新创建品类-月份交叉表（确保数据可用）
cat_month_data = pd.pivot_table(
    completed_df,
    values='revenue',
    index='category',
    columns='month',
    aggfunc='sum',
    fill_value=0
)

fig, ax = plt.subplots(figsize=(14, 6))

# 绘制热力图
heatmap = sns.heatmap(
    cat_month_data,
    annot=True,           # 在格子中显示数值
    fmt=',.0f',           # 数值格式：千分位分隔
    cmap='YlOrRd',        # 颜色方案：从黄到红
    linewidths=0.5,       # 格子之间的线宽
    linecolor='white',    # 格子之间的线颜色
    cbar_kws={'label': '销售额 (元)', 'shrink': 0.8},
    ax=ax
)

ax.set_title('品类-月份销售额热力图', fontsize=16, fontweight='bold')
ax.set_xlabel('月份', fontsize=12)
ax.set_ylabel('品类', fontsize=12)
ax.set_xticklabels([f'{int(m)}月' for m in cat_month_data.columns], rotation=0)

plt.tight_layout()
plt.show()
```

热力图中颜色越深（红色），表示该品类在该月的销售额越高。你可以快速地：
- 横向对比：某个品类在哪几个月卖得最好
- 纵向对比：某个月份中哪个品类表现最突出
- 找出整张图中的"热点"：颜色最深的格子

`cmap='YlOrRd'` 设置了从黄色（低值）到橙色再到红色（高值）的渐变色。这种色彩映射既直觉又美观。其他常用的 colormap 还有 `'Blues'`、`'Greens'`、`'coolwarm'`（蓝到红的双色）等。

让我们再画一个相关系数矩阵的热力图，用来可视化 Section 5.5 的分析结果：

```python
corr_cols = ['quantity', 'revenue', 'profit', 'age', 'user_tenure_days']
corr_matrix = completed_df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 7))

# 使用 mask 隐藏上三角（避免重复）
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,                # 以 0 为中心，正负对称
    vmin=-1, vmax=1,
    linewidths=1,
    linecolor='white',
    square=True,
    cbar_kws={'shrink': 0.8, 'label': '相关系数'},
    ax=ax
)

ax.set_title('数值变量相关系数矩阵', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
```

在这个热力图中，红色表示正相关，蓝色表示负相关，颜色越深相关性越强。`mask` 参数用来隐藏上三角区域，避免展示重复的信息（因为相关系数矩阵是对称的）。

### 6.7 组合图表：分析仪表盘

在实际工作中，你经常需要把多个图表组合在一起，形成一个**分析仪表盘**（Dashboard）。这不仅看起来专业，还能让领导或同事在一页中看到全局。

下面的代码创建一个 2x2 的子图布局，组合四种不同的图表：

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('电商数据分析仪表盘', fontsize=20, fontweight='bold', y=1.02)

# ---- 子图1: 品类销售额柱状图 ----
cat_rev = completed_df.groupby('category')['revenue'].sum().sort_values(ascending=True)
axes[0, 0].barh(cat_rev.index, cat_rev.values, color=COLORS[:len(cat_rev)])
axes[0, 0].set_title('各品类销售额', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('销售额 (元)')
for i, (val, name) in enumerate(zip(cat_rev.values, cat_rev.index)):
    axes[0, 0].text(val, i, f' {val:,.0f}', va='center', fontsize=10)
axes[0, 0].set_xlim(0, cat_rev.max() * 1.25)

# ---- 子图2: 月度趋势折线图 ----
axes[0, 1].plot(monthly['month'], monthly['月销售额'],
                marker='o', linewidth=2, color=COLORS[1], markersize=6)
axes[0, 1].fill_between(monthly['month'], monthly['月销售额'],
                         alpha=0.15, color=COLORS[1])
axes[0, 1].set_title('月度销售额趋势', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('月份')
axes[0, 1].set_ylabel('销售额 (元)')
axes[0, 1].set_xticks(range(1, 13))
axes[0, 1].set_xticklabels([f'{m}月' for m in range(1, 13)], rotation=45)

# ---- 子图3: 会员等级消费对比 ----
mem_stats = completed_df.groupby('membership_level').agg(
    人均消费=('revenue', 'mean')
).reset_index()
# 按合理顺序排列
level_order = ['普通', '银卡', '金卡', '钻石']
mem_stats['membership_level'] = pd.Categorical(
    mem_stats['membership_level'], categories=level_order, ordered=True
)
mem_stats = mem_stats.sort_values('membership_level')

bars3 = axes[1, 0].bar(mem_stats['membership_level'].astype(str),
                         mem_stats['人均消费'], color=COLORS[2:6])
axes[1, 0].set_title('各会员等级平均客单价', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('会员等级')
axes[1, 0].set_ylabel('平均客单价 (元)')
for bar_item in bars3:
    height = bar_item.get_height()
    axes[1, 0].text(bar_item.get_x() + bar_item.get_width() / 2., height,
                     f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
axes[1, 0].set_ylim(0, mem_stats['人均消费'].max() * 1.2)

# ---- 子图4: 城市消费 Top 10 ----
city_top10 = completed_df.groupby('city')['revenue'].sum().nlargest(10).sort_values()
axes[1, 1].barh(city_top10.index, city_top10.values, color=COLORS[4])
axes[1, 1].set_title('消费总额 Top 10 城市', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('销售额 (元)')
for i, val in enumerate(city_top10.values):
    axes[1, 1].text(val, i, f' {val:,.0f}', va='center', fontsize=10)
axes[1, 1].set_xlim(0, city_top10.max() * 1.25)

plt.tight_layout()
plt.savefig('dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()
print("仪表盘已保存为 dashboard.png")
```

这个仪表盘包含了四个视角的分析：品类对比、时间趋势、会员等级、地域分布。在实际项目中，这样的仪表盘经常会出现在周报、月报或数据汇报 PPT 中。

`plt.savefig()` 将图表保存为 PNG 文件，几个关键参数：
- `dpi=150`：设置分辨率，150 dpi 适合屏幕查看和报告，印刷品建议用 300
- `bbox_inches='tight'`：自动裁切空白边距
- `facecolor='white'`：确保背景是白色（有些环境默认透明背景）

> 💡 **小贴士**：在 Jupyter Notebook 中，`plt.show()` 会在 cell 下方直接显示图表。如果你在脚本中运行，可能需要在开头加上 `plt.switch_backend('Agg')` 来使用非交互式后端（仅保存不显示）。

### 6.8 箱线图：异常值可视化

**箱线图**（Box Plot，也叫盒须图）是观察数据分布和发现异常值的得力工具。让我们用它来展示各品类的价格分布情况。

先来理解箱线图的组成部分：

- **箱子的上下边**：分别是第三四分位数（Q3，75%）和第一四分位数（Q1，25%）
- **箱子中间的线**：中位数（Q2，50%）
- **须（Whiskers）**：从箱子延伸出去的线，通常到 1.5 倍 IQR（四分位距）范围内的最远数据点
- **圆点**：超出须范围的数据点，即**异常值**（Outliers）

下面的代码绘制各品类的价格分布箱线图：

```python
fig, ax = plt.subplots(figsize=(12, 7))

# 使用 seaborn 绘制箱线图
box = sns.boxplot(
    data=completed_df,
    x='category',
    y='price',
    palette='Set2',
    width=0.6,
    flierprops=dict(marker='o', markerfacecolor='red', markersize=5, alpha=0.5),
    ax=ax
)

ax.set_title('各品类价格分布（箱线图）', fontsize=16, fontweight='bold')
ax.set_xlabel('品类', fontsize=12)
ax.set_ylabel('价格 (元)', fontsize=12)

# 在每个箱子旁边标注中位数
medians = completed_df.groupby('category')['price'].median()
for i, cat in enumerate(completed_df['category'].unique()):
    if cat in medians.index:
        ax.text(i, medians[cat], f' {medians[cat]:.0f}',
                ha='left', va='center', fontsize=10, color='darkblue', fontweight='bold')

plt.tight_layout()
plt.show()
```

从箱线图中你可以一眼看出：
- 哪个品类的价格跨度最大（箱子+须的范围）
- 哪个品类的价格最集中（箱子最窄）
- 哪些品类存在价格异常值（红色圆点）
- 各品类的价格中位数大致在什么水平

箱线图在数据分析中的主要用途包括：发现异常值、比较不同组的分布差异、评估数据的偏态程度。如果箱子上方的须明显比下方长，说明数据**右偏**（存在少量高价格的商品拉高了均值）。

让我们再画一个更细致的箱线图——同时展示价格分布和各个数据点：

```python
fig, ax = plt.subplots(figsize=(12, 7))

# 使用 stripplot 叠加在 boxplot 上，展示每个数据点
sns.boxplot(
    data=completed_df,
    x='category',
    y='revenue',
    palette='Set2',
    width=0.5,
    showfliers=False,  # 关闭默认的异常值点
    ax=ax
)

sns.stripplot(
    data=completed_df,
    x='category',
    y='revenue',
    color='black',
    alpha=0.15,
    size=3,
    jitter=True,
    ax=ax
)

ax.set_title('各品类订单金额分布（箱线图 + 散点）', fontsize=16, fontweight='bold')
ax.set_xlabel('品类', fontsize=12)
ax.set_ylabel('订单金额 (元)', fontsize=12)

plt.tight_layout()
plt.show()
```

通过叠加 `stripplot`，你可以看到每个数据点的具体位置，对数据分布有更直观的感受。`jitter=True` 让数据点在水平方向上有轻微的随机偏移，避免完全重叠。`alpha=0.15` 设置了较低的透明度，在数据点密集的区域会自然形成"深色团块"，直观地展示数据的密度。


到这里，你已经掌握了数据聚合与统计分析的核心方法，也学会了用多种图表来可视化你的分析结果。让我们回顾一下 Section 5 和 Section 6 的要点：

**数据聚合方面：**
- `groupby()` 是核心工具，理解"拆分-应用-合并"的思路
- `agg()` 支持同时计算多个指标，灵活且强大
- `pd.pivot_table()` 可以创建多维交叉表，揭示维度之间的交互模式
- RFM 分析是一种经典的用户分层方法，简单却实用

**数据可视化方面：**
- 选择合适的图表类型：柱状图比较、折线图看趋势、饼图看占比、散点图看关系、热力图看矩阵、箱线图看分布
- 让图表"说话"：排序、颜色、标注缺一不可
- 组合仪表盘可以在一页中展示多维分析结果
- `plt.savefig()` 将图表保存为文件用于报告分享

在 最后 中，我们将学习如何把这些分析成果整理成完整的数据分析报告，以及一些进阶技巧。


## Section 7: 综合实战——回答业务问题

到这里，你已经掌握了数据加载、清洗、统计分析和可视化的全套工具。是时候回到最初的问题了——主管提出的 5 个业务问题，还记得吗？让我们逐一击破，用数据给出清晰的答案。

在真实工作场景中，分析的最终目的不是画出漂亮的图表，而是**回答业务问题、驱动决策**。这一节，我们会把前面学到的技能串联起来，模拟一次完整的业务分析汇报。


### 7.1 问题一：各品类的销售额和利润率如何？哪些品类最赚钱？

主管最关心的第一个问题就是品类表现。让我们从多个维度构建一个品类全景表。

下面这段代码按品类聚合关键指标，并将结果格式化为易读的 DataFrame。

```python
# 按品类聚合核心指标
category_performance = completed_df.groupby('category').agg(
    总销售额=('revenue', 'sum'),
    总利润=('profit', 'sum'),
    总成本=('total_cost', 'sum'),
    订单数量=('order_id', 'nunique'),
    销售件数=('quantity', 'sum'),
    平均客单价=('payment_amount', 'mean')
).reset_index()

# 计算利润率
category_performance['利润率'] = (
    category_performance['总利润'] / category_performance['总销售额'] * 100
)

# 按销售额降序排列
category_performance = category_performance.sort_values('总销售额', ascending=False)

# 格式化展示
display_df = category_performance.copy()
display_df['总销售额'] = display_df['总销售额'].apply(lambda x: f'¥{x:,.0f}')
display_df['总利润'] = display_df['总利润'].apply(lambda x: f'¥{x:,.0f}')
display_df['平均客单价'] = display_df['平均客单价'].apply(lambda x: f'¥{x:,.1f}')
display_df['利润率'] = display_df['利润率'].apply(lambda x: f'{x:.1f}%')

print("=== 各品类销售表现 ===\n")
print(display_df[['category', '总销售额', '总利润', '利润率',
                   '订单数量', '平均客单价']].to_string(index=False))
```

上面的输出给了你一张品类"成绩单"。但光看数字还不够直观，让我们用**双轴图**把销售额和利润率放在同一张图里对比。

```python
fig, ax1 = plt.subplots(figsize=(10, 6))

# 排序后的品类数据
cat_sorted = category_performance.sort_values('总销售额', ascending=True)
categories = cat_sorted['category']
sales = cat_sorted['总销售额']
profit_rates = cat_sorted['利润率']

# 左轴：柱状图表示销售额
bars = ax1.barh(categories, sales, color='#4ECDC4', alpha=0.85, label='销售额')
ax1.set_xlabel('销售额（元）', fontsize=12)
ax1.set_ylabel('')
ax1.tick_params(axis='y', labelsize=11)

# 在柱状图上标注数值
for bar, val in zip(bars, sales):
    ax1.text(bar.get_width() + sales.max() * 0.01, bar.get_y() + bar.get_height() / 2,
             f'¥{val:,.0f}', va='center', fontsize=9)

# 右轴：折线图表示利润率
ax2 = ax1.twiny()
ax2.plot(profit_rates, categories, 'o-', color='#FF6B6B', linewidth=2,
         markersize=8, label='利润率')
ax2.set_xlabel('利润率（%）', fontsize=12, color='#FF6B6B')
ax2.tick_params(axis='x', labelcolor='#FF6B6B')

# 添加标题和图例
plt.title('各品类销售额与利润率对比', fontsize=14, fontweight='bold', pad=40)
fig.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95))
plt.tight_layout()
plt.savefig('category_sales_profit.png', dpi=150, bbox_inches='tight')
plt.show()
```

从图中你可以清晰地看到每个品类的"赚钱能力"。有些品类销售额高但利润率未必最优，有些品类虽然体量不大但利润率惊人——这正是业务决策需要关注的差异。

> 💡 **小贴士**：**双轴图**在业务汇报中非常常用。它能同时展示量级差异很大的两个指标，避免一个指标"压扁"另一个。但要注意，双轴图也容易误导读者，使用时务必清晰标注左右轴的含义。

**业务结论：** 通过品类分析可以发现，销售额最高的品类往往是高频刚需品，但利润率未必最高；而某些小众品类虽然销售规模有限，利润率却很可观。建议团队在保持核心品类销量的同时，加大高利润率品类的推广力度，优化整体利润结构。


### 7.2 问题二：销售额的月度趋势如何？有没有明显的淡旺季？

了解业务的**季节性规律**对制定全年预算和营销计划至关重要。让我们看看销售额和订单量的月度变化趋势。

首先，按月聚合销售数据并计算环比变化。

```python
# 按月聚合
monthly_trend = completed_df.groupby(['year', 'month']).agg(
    月销售额=('revenue', 'sum'),
    月订单量=('order_id', 'nunique'),
    月均客单价=('payment_amount', 'mean')
).reset_index()

# 构建月份标签
monthly_trend['月份标签'] = monthly_trend.apply(
    lambda row: f"{int(row['year'])}-{int(row['month']):02d}", axis=1
)

# 计算环比变化（MoM）
monthly_trend['销售额环比'] = monthly_trend['月销售额'].pct_change() * 100
monthly_trend['订单量环比'] = monthly_trend['月订单量'].pct_change() * 100

print("=== 月度销售趋势 ===\n")
trend_display = monthly_trend[['月份标签', '月销售额', '月订单量', '销售额环比']].copy()
trend_display['月销售额'] = trend_display['月销售额'].apply(lambda x: f'¥{x:,.0f}')
trend_display['销售额环比'] = trend_display['销售额环比'].apply(
    lambda x: f'{x:+.1f}%' if pd.notna(x) else '-'
)
print(trend_display.to_string(index=False))
```

环比数据能帮你快速识别哪些月份增长、哪些月份下滑。接下来让我们用图表直观展现趋势。

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

x = range(len(monthly_trend))
labels = monthly_trend['月份标签']

# 上图：销售额趋势
ax1.plot(x, monthly_trend['月销售额'], 'o-', color='#2196F3',
         linewidth=2.5, markersize=7, label='月销售额')
ax1.fill_between(x, monthly_trend['月销售额'], alpha=0.15, color='#2196F3')
ax1.set_ylabel('销售额（元）', fontsize=11)
ax1.set_title('月度销售趋势分析', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)

# 标注最高和最低月份
max_idx = monthly_trend['月销售额'].idxmax()
min_idx = monthly_trend['月销售额'].idxmin()
ax1.annotate(f"最高\n¥{monthly_trend.loc[max_idx, '月销售额']:,.0f}",
             xy=(max_idx, monthly_trend.loc[max_idx, '月销售额']),
             fontsize=9, color='red', fontweight='bold',
             ha='center', va='bottom')
ax1.annotate(f"最低\n¥{monthly_trend.loc[min_idx, '月销售额']:,.0f}",
             xy=(min_idx, monthly_trend.loc[min_idx, '月销售额']),
             fontsize=9, color='green', fontweight='bold',
             ha='center', va='top')

# 下图：订单量趋势
ax2.bar(x, monthly_trend['月订单量'], color='#FF9800', alpha=0.75, label='月订单量')
ax2.set_ylabel('订单量', fontsize=11)
ax2.set_xlabel('月份', fontsize=11)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=45, ha='right')
ax2.legend(loc='upper left')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=150, bbox_inches='tight')
plt.show()
```

这张双面板图的上半部分展示了销售额的连续走势，下半部分用柱状图辅助呈现订单量变化。两者结合，你能更立体地理解业务节奏。

让我们进一步识别旺季和淡季。

```python
# 计算各月平均销售额，识别淡旺季
monthly_avg = monthly_trend.groupby('month')['月销售额'].mean()
overall_avg = monthly_avg.mean()

print("=== 淡旺季识别 ===\n")
print(f"月均销售额基准线：¥{overall_avg:,.0f}\n")
for m, val in monthly_avg.items():
    diff_pct = (val - overall_avg) / overall_avg * 100
    tag = "🔥 旺季" if diff_pct > 10 else ("❄️ 淡季" if diff_pct < -10 else "   平季")
    print(f"  {int(m):2d}月：¥{val:>10,.0f}  ({diff_pct:+6.1f}%)  {tag}")
```

上面的输出以月均基准线为参照，超过 10% 标记为旺季，低于 -10% 标记为淡季，帮你一眼看清全年的业务节奏。

**业务结论：** 从月度趋势可以看出，业务存在明显的季节性波动。建议在旺季来临前提前备货、加大营销投放，而在淡季则侧重用户运营和品牌建设，用促销活动拉动低谷期的消费。环比增长数据还能帮你评估每次营销活动的效果。


### 7.3 问题三：不同城市的消费能力和偏好有什么差异？

中国市场地域差异显著，理解城市间的消费差异能帮助团队做更精准的区域营销。让我们从多个角度分析城市维度的数据。

先计算每个城市的核心消费指标。

```python
# 按城市聚合
city_stats = completed_df.groupby('city').agg(
    总消费额=('revenue', 'sum'),
    订单数=('order_id', 'nunique'),
    用户数=('user_id', 'nunique'),
    平均客单价=('payment_amount', 'mean')
).reset_index()

# 计算人均消费
city_stats['人均消费'] = city_stats['总消费额'] / city_stats['用户数']
city_stats = city_stats.sort_values('总消费额', ascending=False)

print("=== 城市消费排名 Top 10 ===\n")
top10_display = city_stats.head(10).copy()
top10_display['总消费额'] = top10_display['总消费额'].apply(lambda x: f'¥{x:,.0f}')
top10_display['人均消费'] = top10_display['人均消费'].apply(lambda x: f'¥{x:,.0f}')
top10_display['平均客单价'] = top10_display['平均客单价'].apply(lambda x: f'¥{x:,.1f}')
print(top10_display.to_string(index=False))
```

接下来绘制 Top 10 城市的消费排名图。

```python
top10 = city_stats.head(10)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 左图：总消费额排名
axes[0].barh(top10['city'][::-1], top10['总消费额'][::-1],
             color='#26A69A', alpha=0.85)
axes[0].set_xlabel('总消费额（元）', fontsize=11)
axes[0].set_title('Top 10 城市 — 总消费额', fontsize=13, fontweight='bold')
for i, (city, val) in enumerate(zip(top10['city'][::-1], top10['总消费额'][::-1])):
    axes[0].text(val + top10['总消费额'].max() * 0.01, i,
                 f'¥{val:,.0f}', va='center', fontsize=9)

# 右图：人均消费排名
axes[1].barh(top10['city'][::-1], top10['人均消费'][::-1],
             color='#FF7043', alpha=0.85)
axes[1].set_xlabel('人均消费（元）', fontsize=11)
axes[1].set_title('Top 10 城市 — 人均消费', fontsize=13, fontweight='bold')
for i, (city, val) in enumerate(zip(top10['city'][::-1], top10['人均消费'][::-1])):
    axes[1].text(val + top10['人均消费'].max() * 0.01, i,
                 f'¥{val:,.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('city_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
```

注意左右两张图的排名可能不同——总消费额高的城市未必人均消费也高。这是因为大城市用户基数大，总量领先；而某些中型城市的用户购买力可能更强。

现在让我们进一步分析不同城市的品类偏好。下面构建一个**城市-品类交叉表**。

```python
# 构建城市-品类交叉表（取 Top 8 城市）
top8_cities = city_stats.head(8)['city'].tolist()
city_category = completed_df[completed_df['city'].isin(top8_cities)].pivot_table(
    index='city',
    columns='category',
    values='revenue',
    aggfunc='sum',
    fill_value=0
)

# 计算每个城市各品类的占比
city_category_pct = city_category.div(city_category.sum(axis=1), axis=0) * 100

print("=== 主要城市的品类消费占比（%） ===\n")
print(city_category_pct.round(1).to_string())
```

这张交叉表揭示了城市间的品类偏好差异。让我们用热力图更直观地展示。

```python
plt.figure(figsize=(10, 6))
sns.heatmap(city_category_pct, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=0.5, cbar_kws={'label': '消费占比 (%)'})
plt.title('城市-品类消费偏好热力图', fontsize=14, fontweight='bold')
plt.xlabel('品类', fontsize=11)
plt.ylabel('城市', fontsize=11)
plt.tight_layout()
plt.savefig('city_category_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
```

热力图中颜色越深的格子，代表该城市在对应品类上的消费占比越高。通过对比行与行之间的色块分布，你能快速发现城市间的偏好差异。

> 💡 **小贴士**：在实际工作中，城市分析常常需要结合一线/新一线/二线等**城市等级**维度。你可以外接一份城市等级映射表，用 `merge` 合并后再做聚合分析，获得更有层次的洞察。

**业务结论：** 不同城市在总消费规模和人均消费水平上存在明显差异，且品类偏好各有侧重。建议根据区域特点制定差异化运营策略——对高消费城市保持品类深度运营，对高人均消费城市加大高端品类推荐，对消费潜力城市开展拉新促活活动。


### 7.4 问题四：不同会员等级的用户在消费行为上有什么区别？

会员体系是用户运营的核心抓手。弄清楚不同等级会员的行为差异，能帮你优化会员权益设计和升级激励策略。

让我们从多个维度对比各会员等级。

```python
# 按会员等级聚合用户行为
member_stats = completed_df.groupby('membership_level').agg(
    用户数=('user_id', 'nunique'),
    总订单数=('order_id', 'nunique'),
    总消费额=('revenue', 'sum'),
    平均客单价=('payment_amount', 'mean'),
    平均购买件数=('quantity', 'mean')
).reset_index()

# 计算人均指标
member_stats['人均订单数'] = member_stats['总订单数'] / member_stats['用户数']
member_stats['人均消费额'] = member_stats['总消费额'] / member_stats['用户数']

print("=== 各会员等级消费行为对比 ===\n")
ms_display = member_stats.copy()
ms_display['总消费额'] = ms_display['总消费额'].apply(lambda x: f'¥{x:,.0f}')
ms_display['人均消费额'] = ms_display['人均消费额'].apply(lambda x: f'¥{x:,.0f}')
ms_display['平均客单价'] = ms_display['平均客单价'].apply(lambda x: f'¥{x:,.1f}')
ms_display['人均订单数'] = ms_display['人均订单数'].apply(lambda x: f'{x:.1f}')
print(ms_display[['membership_level', '用户数', '人均订单数',
                   '人均消费额', '平均客单价']].to_string(index=False))
```

接下来看看不同会员等级的品类偏好和支付方式偏好。

```python
# 会员等级 × 品类偏好
member_category = completed_df.groupby(['membership_level', 'category'])[
    'revenue'].sum().reset_index()
member_top_category = member_category.loc[
    member_category.groupby('membership_level')['revenue'].idxmax()
][['membership_level', 'category', 'revenue']]
member_top_category.columns = ['会员等级', '最爱品类', '该品类消费额']

print("\n=== 各等级会员的偏好品类 ===\n")
print(member_top_category.to_string(index=False))

# 会员等级 × 支付方式偏好
member_payment = completed_df.groupby(['membership_level', 'payment_method'])[
    'order_id'].nunique().reset_index()
member_payment.columns = ['membership_level', 'payment_method', 'order_count']
member_top_payment = member_payment.loc[
    member_payment.groupby('membership_level')['order_count'].idxmax()
][['membership_level', 'payment_method', 'order_count']]
member_top_payment.columns = ['会员等级', '首选支付方式', '使用次数']

print("\n=== 各等级会员的支付偏好 ===\n")
print(member_top_payment.to_string(index=False))
```

让我们用图表直观对比各等级的消费行为差异。

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

levels = member_stats['membership_level']
colors = ['#FFCA28', '#78909C', '#FFB300', '#5C6BC0']

# 图1：人均订单数
axes[0].bar(levels, member_stats['人均订单数'], color=colors[:len(levels)], alpha=0.85)
axes[0].set_title('人均订单数', fontsize=13, fontweight='bold')
axes[0].set_ylabel('订单数')
for i, v in enumerate(member_stats['人均订单数']):
    axes[0].text(i, v + 0.05, f'{v:.1f}', ha='center', fontsize=10)

# 图2：人均消费额
axes[1].bar(levels, member_stats['人均消费额'], color=colors[:len(levels)], alpha=0.85)
axes[1].set_title('人均消费额', fontsize=13, fontweight='bold')
axes[1].set_ylabel('金额（元）')
for i, v in enumerate(member_stats['人均消费额']):
    axes[1].text(i, v + v * 0.02, f'¥{v:,.0f}', ha='center', fontsize=10)

# 图3：平均客单价
axes[2].bar(levels, member_stats['平均客单价'], color=colors[:len(levels)], alpha=0.85)
axes[2].set_title('平均客单价', fontsize=13, fontweight='bold')
axes[2].set_ylabel('金额（元）')
for i, v in enumerate(member_stats['平均客单价']):
    axes[2].text(i, v + v * 0.02, f'¥{v:,.0f}', ha='center', fontsize=10)

for ax in axes:
    ax.tick_params(axis='x', rotation=15)

plt.suptitle('不同会员等级消费行为对比', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('member_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
```

三张并排的柱状图清晰地展示了会员等级与消费行为的关系。通常你会看到等级越高的会员，各项人均指标也越高——这验证了会员体系的有效性。

**业务结论：** 高等级会员在人均消费和购买频次上显著优于低等级会员，说明会员升级能有效拉动消费。建议加大对中等级会员的升级激励（如积分加速、专属折扣），推动他们向高等级跃迁；同时针对低等级会员设计轻量级激活方案，降低流失风险。


### 7.5 问题五：哪些商品是明星产品？哪些可能需要调整策略？

最后一个问题需要我们用更高级的分析框架。借鉴经典的 **BCG 矩阵**思想，我们用"销售额"和"利润率"两个维度把商品分成四个象限。

先计算每个商品的销售额和利润率。

```python
# 按商品聚合
product_stats = completed_df.groupby(['product_id', 'product_name', 'category']).agg(
    销售额=('revenue', 'sum'),
    总利润=('profit', 'sum'),
    总成本=('total_cost', 'sum'),
    销售件数=('quantity', 'sum'),
    订单数=('order_id', 'nunique')
).reset_index()

# 计算利润率
product_stats['利润率'] = product_stats['总利润'] / product_stats['销售额'] * 100

print(f"共计 {len(product_stats)} 个商品参与分析")
print(f"销售额范围：¥{product_stats['销售额'].min():,.0f} ~ ¥{product_stats['销售额'].max():,.0f}")
print(f"利润率范围：{product_stats['利润率'].min():.1f}% ~ {product_stats['���润率'].max():.1f}%")
```

接下来，以销售额和利润率的中位数为分界线，将商品划分到四个象限。

```python
# 确定分界线（使用中位数）
sales_median = product_stats['销售额'].median()
profit_rate_median = product_stats['利润率'].median()

print(f"销售额中位数：¥{sales_median:,.0f}")
print(f"利润率中位数：{profit_rate_median:.1f}%")

# 分类
def classify_product(row):
    high_sales = row['销售额'] >= sales_median
    high_profit = row['利润率'] >= profit_rate_median
    if high_sales and high_profit:
        return '明星商品'
    elif high_sales and not high_profit:
        return '引流商品'
    elif not high_sales and high_profit:
        return '潜力商品'
    else:
        return '问题商品'

product_stats['象限'] = product_stats.apply(classify_product, axis=1)

# 统计各象限商品数量
quadrant_counts = product_stats['象限'].value_counts()
print("\n=== 商品四象限分布 ===\n")
for q, cnt in quadrant_counts.items():
    print(f"  {q}：{cnt} 个")
```

现在让我们绘制经典的**四象限散点图**，这是商品组合分析中最常用的可视化方式。

```python
fig, ax = plt.subplots(figsize=(12, 8))

# 定义象限颜色
quadrant_colors = {
    '明星商品': '#4CAF50',
    '引流商品': '#FF9800',
    '潜力商品': '#2196F3',
    '问题商品': '#F44336'
}

# 按象限绘制散点
for quadrant, color in quadrant_colors.items():
    mask = product_stats['象限'] == quadrant
    subset = product_stats[mask]
    ax.scatter(subset['销售额'], subset['利润率'],
               c=color, s=subset['销售件数'] * 2, alpha=0.65,
               label=f'{quadrant} ({len(subset)}个)', edgecolors='white', linewidth=0.5)

# 绘制分界线
ax.axvline(x=sales_median, color='gray', linestyle='--', alpha=0.6, linewidth=1)
ax.axhline(y=profit_rate_median, color='gray', linestyle='--', alpha=0.6, linewidth=1)

# 标注象限名称
xlim = ax.get_xlim()
ylim = ax.get_ylim()
text_props = dict(fontsize=12, alpha=0.3, fontweight='bold', ha='center', va='center')
ax.text((sales_median + xlim[1]) / 2, (profit_rate_median + ylim[1]) / 2,
        '明星商品\n高销售·高利润', **text_props, color='#4CAF50')
ax.text((xlim[0] + sales_median) / 2, (profit_rate_median + ylim[1]) / 2,
        '潜力商品\n低销售·高利润', **text_props, color='#2196F3')
ax.text((sales_median + xlim[1]) / 2, (ylim[0] + profit_rate_median) / 2,
        '引流商品\n高销售·低利润', **text_props, color='#FF9800')
ax.text((xlim[0] + sales_median) / 2, (ylim[0] + profit_rate_median) / 2,
        '问题商品\n低销售·低利润', **text_props, color='#F44336')

ax.set_xlabel('销售额（元）', fontsize=12)
ax.set_ylabel('利润率（%）', fontsize=12)
ax.set_title('商品四象限分析（气泡大小 = 销售件数）', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(alpha=0.2)
plt.tight_layout()
plt.savefig('product_quadrant.png', dpi=150, bbox_inches='tight')
plt.show()
```

图中每个点代表一个商品，位置由销售额和利润率决定，气泡大小反映销售件数。四个象限清晰地把商品分成了四类。

让我们列出每个象限的代表商品。

```python
print("=== 各象限代表商品 ===\n")

for quadrant in ['明星商品', '引流商品', '潜力商品', '问题商品']:
    subset = product_stats[product_stats['象限'] == quadrant].sort_values(
        '销售额', ascending=False
    )
    print(f"【{quadrant}】（共 {len(subset)} 个）")
    print(f"  策略建议：", end='')
    if quadrant == '明星商品':
        print("持续投入资源，保持竞争优势，考虑扩展相关产品线")
    elif quadrant == '引流商品':
        print("优化成本结构、提升利润率，或将其作为引流入口带动高利润品")
    elif quadrant == '潜力商品':
        print("加大营销推广力度，提升曝光和销量，挖掘增长空间")
    else:
        print("评估是否保留，考虑调价、换品或淘汰")

    top_n = min(3, len(subset))
    for _, row in subset.head(top_n).iterrows():
        print(f"    - {row['product_name']}（{row['category']}）"
              f"  销售额 ¥{row['销售额']:,.0f}  利润率 {row['利润率']:.1f}%")
    print()
```

> 💡 **小贴士**：在实际工作中，商品分析还应结合**库存周转率**、**退货率**、**用户评价**等维度综合评判。单看销售额和利润率只是第一步，更完整的商品评估需要多源数据支撑。

**业务结论：** 明星商品是公司的利润引擎，应持续投入资源维护其竞争力；引流商品虽然利润率偏低，但能带来流量和用户活跃度，可考虑搭配高利润品捆绑销售；潜力商品值得加大推广测试；问题商品则需要果断评估——是调整定价策略、还是逐步淘汰腾出资源给更优质的产品。


### 7.6 生成分析报告摘要

在实际工作中，分析结果最终要落到一份结构化的报告里。让我们用代码自动生成一份文本报告摘要，把前面所有分析的核心数据汇总起来。

```python
# 汇总关键数据
total_revenue = completed_df['revenue'].sum()
total_profit = completed_df['profit'].sum()
total_orders = completed_df['order_id'].nunique()
total_users = completed_df['user_id'].nunique()
avg_order_value = completed_df['payment_amount'].mean()
overall_profit_rate = total_profit / total_revenue * 100

# 最佳品类（按利润）
best_cat = category_performance.sort_values('总利润', ascending=False).iloc[0]
# 最佳月份（按销售额）
best_month = monthly_trend.loc[monthly_trend['月销售额'].idxmax()]
# 最佳城市（按总消费额）
best_city = city_stats.iloc[0]

# 打印报告
report = f"""
=====================================
        月度业务分析报告
=====================================
报告周期：{monthly_trend['月份标签'].iloc[0]} 至 {monthly_trend['月份标签'].iloc[-1]}
数据范围：{total_orders:,} 笔已完成订单
分析人员：数据分析团队
生成日期：自动生成

一、整体概况
  - 总销售额：¥{total_revenue:,.0f}
  - 总利润：¥{total_profit:,.0f}
  - 整体利润率：{overall_profit_rate:.1f}%
  - 总订单数：{total_orders:,} 笔
  - 独立用户数：{total_users:,} 人
  - 平均客单价：¥{avg_order_value:,.1f}

二、核心发现
  1. 品类表现：{best_cat['category']}品类利润贡献最大，
     总利润达 ¥{best_cat['总利润']:,.0f}
  2. 季节趋势：{best_month['月份标签']} 为全年销售高峰，
     当月销售额 ¥{best_month['月销售额']:,.0f}
  3. 城市格局：{best_city['city']}为消费额第一城市，
     总消费 ¥{best_city['总消费额']:,.0f}
  4. 会员价值：高等级会员的人均消费额显著高于
     低等级会员，会员升级机制有效
  5. 商品结构：明星商品 {quadrant_counts.get('明星商品', 0)} 个，
     问题商品 {quadrant_counts.get('问题商品', 0)} 个，需关注优化

三、建议措施
  1. 加大高利润品类的营销投放，优化低利润
     品类的成本结构
  2. 在旺季前 1-2 个月启动备货和预热活动，
     淡季侧重用户留存运营
  3. 针对不同城市制定差异化选品和定价策略
  4. 设计会员升级激励计划，推动中等级用户
     向高等级跃迁
  5. 对问题商品启动评估流程，释放资源聚焦
     明星和潜力商品
=====================================
"""
print(report)
```

这份报告摘要的每一个数字都是代码自动计算填入的，确保了数据的准确性和一致性。

在实际工作中，你可能会用 Jupyter 将 Notebook 导出为 HTML 或 PDF，方便发送给同事和领导；也可以用 `pandas` 的 `to_excel()` 方法将分析结果写入 Excel 文件，配合 `openpyxl` 还能设置格式和样式。更进一步，你还可以搭建定时任务（如 crontab + Python 脚本），实现报表的自动化生成和邮件发送。

```python
# 示例：将核心分析结果保存到 Excel（实际场景中很常用）
with pd.ExcelWriter('business_analysis_report.xlsx', engine='openpyxl') as writer:
    category_performance.to_excel(writer, sheet_name='品类分析', index=False)
    monthly_trend.to_excel(writer, sheet_name='月度趋势', index=False)
    city_stats.to_excel(writer, sheet_name='城市分析', index=False)
    member_stats.to_excel(writer, sheet_name='会员分析', index=False)
    product_stats.to_excel(writer, sheet_name='商品分析', index=False)

print("分析结果已保存至 business_analysis_report.xlsx")
```

> 💡 **小贴士**：`pd.ExcelWriter` 支持将多个 DataFrame 写入同一个 Excel 文件的不同 Sheet 页，这在制作多维度分析报告时非常实用。配合 `openpyxl` 库，你还可以为单元格设置字体、颜色、边框等格式，让报表更加美观专业。


## Section 8: 总结

恭喜你！完成了一次完整的 Python 数据分析实战之旅。让我们回顾一下从头到尾走过的路，然后聊聊接下来可以去哪里。

### 8.1 知识回顾

本教程从一份原始的电商数据出发，带你完整走过了数据分析的七个阶段。下面这张表帮你快速回顾每个阶段的核心技能。

| 阶段 | 关键技能 | 核心工具/函数 |
|------|---------|-------------|
| 数据加载 | 读取 CSV 文件，初步查看数据 | `pd.read_csv()`, `head()`, `tail()` |
| 数据探索 | 了解数据全貌、分布和缺失情况 | `shape`, `dtypes`, `describe()`, `isnull().sum()` |
| 数据清洗 | 处理重复值、缺失值、异常值 | `drop_duplicates()`, `fillna()`, 条件筛选 |
| 数据转换 | 多表合并、类型转换、特征工程 | `merge()`, `pd.to_datetime()`, `pd.cut()` |
| 统计分析 | 分组聚合、透视表、相关性分析 | `groupby()`, `agg()`, `pivot_table()`, `corr()` |
| 数据可视化 | 用图表直观呈现数据故事 | `matplotlib`, `seaborn`, 多种图表类型 |
| 业务分析 | 回答真实业务问题，输出洞察 | 综合运用以上所有工具 |

每个阶段都不是孤立的。数据分析的真实流程往往需要你在各个环节之间反复迭代——比如在可视化时发现了异常值，你可能需要回到清洗阶段重新处理；在回答业务问题时，你可能需要补充新的衍生指标。

掌握这七个阶段的核心技能后，面对绝大多数结构化数据分析任务，你都能从容应对。

### 8.2 进阶学习方向

数据分析是一个不断精进的领域。以下四个方向是自然的进阶路径，每个方向都能显著扩展你的能力边界。

**方向一：更多数据源**

本教程使用的是 CSV 文件，但在真实工作中你可能需要对接各种数据源。

```python
# SQL 数据库读取示例
# import sqlalchemy
# engine = sqlalchemy.create_engine('mysql+pymysql://user:pass@host/db')
# df = pd.read_sql('SELECT * FROM orders WHERE year = 2024', engine)

# API 数据读取示例
# import requests
# response = requests.get('https://api.example.com/sales', headers={'token': 'xxx'})
# df = pd.DataFrame(response.json()['data'])

# Excel 多 Sheet 读取示例
# df_dict = pd.read_excel('report.xlsx', sheet_name=None)  # 读取所有 Sheet
# for name, sheet_df in df_dict.items():
#     print(f"Sheet: {name}, 行数: {len(sheet_df)}")
```

掌握 `sqlalchemy` 连接数据库、`requests` 调用 API、以及 `pd.read_excel()` 处理 Excel 文件，能让你从更多渠道获取数据。

**方向二：高级可视化**

`matplotlib` 和 `seaborn` 是基础，但如果你需要制作可交互的动态图表，可以了解以下工具。

```python
# Plotly 交互图表示例
# import plotly.express as px
# fig = px.scatter(product_stats, x='销售额', y='利润率',
#                  color='象限', size='销售件数',
#                  hover_name='product_name',
#                  title='商品四象限分析（交互版）')
# fig.show()

# Pyecharts 中国风图表示例
# from pyecharts.charts import Map
# map_chart = Map()
# map_chart.add("消费额", [list(z) for z in zip(cities, values)], "china")
# map_chart.render("city_map.html")
```

**Plotly** 的交互图表支持鼠标悬停查看详情、缩放、平移等操作，特别适合在 Jupyter Notebook 或 Web 页面中使用。**Pyecharts** 则提供了大量中国风图表样式，包括地图、词云等，在国内业务场景中非常实用。

**方向三：机器学习入门**

当你积累了足够的数据分析经验后，可以开始接触机器学习，实现预测性分析。

```python
# scikit-learn 预测分析示例
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report
#
# # 用用户特征预测会员等级
# features = ['age', 'user_tenure_days', 'total_orders', 'total_spend']
# X = user_features[features]
# y = user_features['membership_level']
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model = RandomForestClassifier(n_estimators=100)
# model.fit(X_train, y_train)
# print(classification_report(y_test, model.predict(X_test)))
```

从描述性分析（发生了什么）到预测性分析（会发生什么），是数据从业者的一次重要跃升。`scikit-learn` 是入门机器学习的首选库，它的 API 设计简洁一致，学习曲线相对友好。

**方向四：自动化报表**

当你的分析流程固定下来后，可以考虑实现自动化——让机器定期帮你跑分析、生成报告、发送邮件。

```python
# 自动化报表流程示例
# import schedule
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
#
# def generate_weekly_report():
#     # 1. 从数据库拉取最新数据
#     df = pd.read_sql(query, engine)
#     # 2. 执行分析流程
#     results = run_analysis(df)
#     # 3. 生成 Excel 报告
#     results.to_excel('weekly_report.xlsx')
#     # 4. 发送邮件
#     send_email('weekly_report.xlsx', recipients=['boss@company.com'])
#
# # 每周一上午 9 点自动执行
# schedule.every().monday.at("09:00").do(generate_weekly_report)
```

将分析流程固化为脚本，再配合定时任务工具（Linux 的 `crontab`、Windows 的 Task Scheduler、或 Python 的 `schedule` 库），就能实现从数据拉取到报告送达的全流程自动化。这会极大地提升你的工作效率，也是从"分析师"向"数据工程师"迈进的第一步。

### 8.3 结束语

回顾这趟旅程：你从一堆 CSV 文件出发，一步步完成了数据加载、清洗、转换、统计分析、可视化，最终回答了主管提出的五个真实业务问题，并输出了一份结构化的分析报告。这就是数据分析的完整闭环。

技术本身并不难，难的是培养"用数据思考"的习惯——面对一个业务问题时，你能想到用什么数据、从什么角度切入、如何验证你的发现。这种能力只能通过不断实践来锻炼。

接下来，建议你找一份你感兴趣的真实数据集动手练习。可以是你公司的业务数据，也可以是 Kaggle 上的公开数据集。不需要追求复杂的技巧，先把今天学到的方法论跑通：提出问题、准备数据、分析探索、得出结论。每跑完一个项目，你的分析能力就会上一个台阶。

数据分析的世界很大，而你已经迈出了坚实的第一步。祝你在这条路上越走越远。
