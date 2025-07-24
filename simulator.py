from character import Character
from ProDistribution import ProDistribution
from type import Style
import random
import csv
import pandas as pd
from write import write_header_cell, write_percentage_cell, write_max_value_cell, write_gacha_legend, apply_data_bars

"""
优化方案：
1. 添加约束，stylecount = 3时，保证主攻流派在三个流派中
"""

class Simulator:
    """游戏模拟器"""
    
    def __init__(self):
        """初始化模拟器"""
        self.pro_distribution = ProDistribution()
        self.characters = []
        self.initialize_characters()
    
    def initialize_characters(self):
        """初始化六个角色"""
        # 创建六个角色：两个5级，两个18级，两个35级
        # 每种等级分别设置havetool为true和false，属性均为熔岩球
        
        # 5级角色
        char_5_false = Character("熔岩球", 5, havetool=False)
        char_5_true = Character("熔岩球", 5, havetool=True)
        
        # 18级角色
        char_18_false = Character("熔岩球", 18, havetool=False)
        char_18_true = Character("熔岩球", 18, havetool=True)
        
        # 35级角色
        char_35_false = Character("熔岩球", 35, havetool=False)
        char_35_true = Character("熔岩球", 35, havetool=True)
        
        # 添加到角色列表
        self.characters = [
            char_5_false, char_5_true,
            char_18_false, char_18_true,
            char_35_false, char_35_true
        ]
    
    def simulate_card_drawing(self, draw_count=15):
        """模拟抽卡过程"""
        print(f"\n=== 模拟{draw_count}次抽卡 ===")
        print("=" * 80)
        
        import random
        
        for i, character in enumerate(self.characters, 1):
            print(f"\n角色 {i} (等级{character.get_level()}, havetool={character.get_havetool()}):")
            
            # 记录初始状态
            initial_style_count = character.get_style_count()
            print(f"  初始流派拥有数量: {initial_style_count}")
            
            # 模拟抽卡过程
            draw_results = []
            for draw in range(draw_count):
                # 获取当前概率分布
                probabilities = self.pro_distribution.get_current_weight(character)
                # 展示当前各个流派的权重
                prob_str = ', '.join([f"{k}:{v:.3f}" for k, v in probabilities.items()])
                print(f"    第{draw+1}次抽卡前流派权重: {prob_str}")
                # 根据概率分布随机选择三个流派（可以重复）
                styles = list(probabilities.keys())
                probs = list(probabilities.values())
                
                # 使用random.choices进行加权随机选择三个流派
                three_cards = random.choices(styles, weights=probs, k=3)
                
                # 角色选择逻辑：优先选择和自身属性相同的流派
                character_attribute = character.attribute
                selected_style = None
                
                # 检查是否有与自身属性相同的流派
                for card in three_cards:
                    if card == character_attribute:
                        selected_style = card
                        break
                
                # 如果没有找到相同属性的流派，选择第一个
                if selected_style is None:
                    selected_style = three_cards[0]
                
                draw_results.append({
                    'cards': three_cards,
                    'selected': selected_style
                })
                
                # 增加对应流派的value
                character.increase_attribute_value(selected_style, 1)
                
                # 每5次抽卡显示一次进度
                if (draw + 1) % 5 == 0:
                    current_style_count = character.get_style_count()
                    print(f"    第{draw + 1}次抽卡后: 流派拥有数量 = {current_style_count}")
            
            # 显示最终结果
            final_style_count = character.get_style_count()
            print(f"  最终流派拥有数量: {final_style_count}")
            print(f"  流派获得情况:")
            
            # 显示所有流派的最终值
            for style, value in character.attribute_values.items():
                if value > 0:
                    print(f"    {style}: {value}")
            
            # 显示抽卡历史
            print(f"  抽卡历史:")
            for j, result in enumerate(draw_results, 1):
                cards_str = ", ".join(result['cards'])
                selected = result['selected']
                selection_reason = "优先选择" if selected == character.attribute else "默认选择"
                print(f"    第{j:2d}次: [{cards_str}] -> {selected} ({selection_reason})")
            
            print(f"  流派数量变化: {initial_style_count} -> {final_style_count}")
    
    def simulate_attribute_value_ratio(self, draw_count=15, rounds=10, threshold=7):
        """模拟多轮并统计角色自身流派属性值大于threshold的比例"""
        print(f"\n=== 模拟{rounds}轮，每轮{draw_count}次抽卡，统计自身流派属性值>{threshold}的比例 ===")
        print("=" * 80)
        for i, character in enumerate(self.characters, 1):
            success_count = 0
            no_main_attribute_count = 0  # 统计没有主攻属性的轮数
            print(f"\n角色 {i} (等级{character.get_level()}, havetool={character.get_havetool()}):")
            for round_idx in range(1, rounds+1):
                character.reset_all_attributes()
                for _ in range(draw_count):
                    probabilities = self.pro_distribution.get_current_weight(character)
                    styles = list(probabilities.keys())
                    probs = list(probabilities.values())
                    three_cards = random.choices(styles, weights=probs, k=3)
                    character_attribute = character.attribute
                    selected_style = None
                    for card in three_cards:
                        if card == character_attribute:
                            selected_style = card
                            break
                    if selected_style is None:
                        selected_style = three_cards[0]
                    character.increase_attribute_value(selected_style, 1)
                
                # 检查本轮结束时是否有主攻属性
                if character.get_attribute_value(character.attribute) == 0:
                    no_main_attribute_count += 1
                
                if character.get_attribute_value(character.attribute) > threshold:
                    success_count += 1
            
            ratio = success_count / rounds
            no_main_ratio = no_main_attribute_count / rounds
            print(f"  自身流派属性值>{threshold}的比例 = {ratio:.3f}")
            print(f"  属性池没有主攻属性的比例 = {no_main_ratio:.3f}")

    def simulate_and_generate_csv(self, draw_count=15, rounds=1000):
        print(f"\n=== 模拟{rounds}轮，每轮{draw_count}次抽卡，生成excel文件 ===")
        print("=" * 80)
        
        # 为每个角色创建统计数据结构
        character_stats = {}
        for i, character in enumerate(self.characters):
            # 初始化统计字典：{抽卡次数: {属性值: 出现次数}}
            stats = {}
            for draw in range(draw_count + 1):  # 0到draw_count，包含初始状态
                stats[draw] = {}
            character_stats[i] = stats
        
        # 执行多轮模拟
        for round_idx in range(rounds):
            if (round_idx + 1) % 100 == 0:
                print(f"  完成第{round_idx + 1}轮模拟...")
            
            # 重置所有角色
            for character in self.characters:
                character.reset_all_attributes()
            
            # 记录初始状态（第0次抽卡）
            for i, character in enumerate(self.characters):
                initial_value = character.get_attribute_value(character.attribute)
                if initial_value not in character_stats[i][0]:
                    character_stats[i][0][initial_value] = 0
                character_stats[i][0][initial_value] += 1
            
            # 执行抽卡过程
            for draw in range(draw_count):
                for i, character in enumerate(self.characters):
                    # 获取当前概率分布
                    probabilities = self.pro_distribution.get_current_weight(character)
                    styles = list(probabilities.keys())
                    probs = list(probabilities.values())
                    
                    # 使用random.choices进行加权随机选择三个流派
                    three_cards = random.choices(styles, weights=probs, k=3)
                    
                    # 角色选择逻辑：优先选择和自身属性相同的流派
                    character_attribute = character.attribute
                    selected_style = None
                    
                    # 检查是否有与自身属性相同的流派
                    for card in three_cards:
                        if card == character_attribute:
                            selected_style = card
                            break
                    
                    # 如果没有找到相同属性的流派，选择第一个
                    if selected_style is None:
                        selected_style = three_cards[0]
                    
                    # 增加对应流派的value
                    character.increase_attribute_value(selected_style, 1)
                    
                    # 记录当前状态
                    current_value = character.get_attribute_value(character.attribute)
                    if current_value not in character_stats[i][draw + 1]:
                        character_stats[i][draw + 1][current_value] = 0
                    character_stats[i][draw + 1][current_value] += 1
        
        # 生成Excel文件
        self._generate_excel_files(character_stats, draw_count, rounds)
        
        print("Excel文件生成完成！")
    
    def _generate_excel_files(self, character_stats, draw_count, rounds):
        """生成Excel文件"""
        filename = "simulation_results.xlsx"
        print(f"  生成文件: {filename}")
        
        # 按等级分组角色
        level_groups = {}
        for i, character in enumerate(self.characters):
            level = character.get_level()
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append((i, character))
        
        # 创建Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 按指定顺序处理等级：35, 18, 5
            level_order = [35, 18, 5]
            for level in level_order:
                if level not in level_groups:
                    continue
                characters = level_groups[level]
                # 创建工作表名称
                sheet_name = f"等级{level}"
                
                # 获取该等级所有角色可能的属性值
                all_values = set()
                for char_idx, character in characters:
                    for draw in range(draw_count + 1):
                        all_values.update(character_stats[char_idx][draw].keys())
                all_values = sorted(list(all_values))
                
                # 创建列名（包含两种tool状态）
                columns = [''] + [f"The {j}th gacha" for j in range(draw_count + 1)]
                
                # 为每个tool状态创建数据
                tool_data = {}
                for char_idx, character in characters:
                    havetool_text = "有灵器" if character.get_havetool() else "无灵器"
                    
                    data = []
                    for value in all_values:
                        row = [f"aimming_level{value}"]
                        for draw in range(draw_count + 1):
                            count = character_stats[char_idx][draw].get(value, 0)
                            ratio = count / rounds
                            row.append(ratio)
                        data.append(row)
                    
                    tool_data[havetool_text] = data
                
                # 创建上下摆放的DataFrame
                merged_data = []
                merged_columns = [''] + [f"The {j}th gacha" for j in range(draw_count + 1)]
                
                # 添加无灵器数据
                if "无灵器" in tool_data:
                    # 添加无灵器标题行
                    title_row = ["无灵器"] + [""] * draw_count
                    merged_data.append(title_row)
                    
                    # 添加无灵器数据
                    for value in all_values:
                        row = [f"aimming_level{value}"]
                        row.extend(tool_data["无灵器"][all_values.index(value)][1:])
                        merged_data.append(row)
                    
                    # 添加空行分隔
                    if "有灵器" in tool_data:
                        empty_row = [""] * (draw_count + 1)
                        merged_data.append(empty_row)
                
                # 添加有灵器数据
                if "有灵器" in tool_data:
                    # 添加有灵器标题行
                    title_row = ["有灵器"] + [""] * draw_count
                    merged_data.append(title_row)
                    
                    # 添加有灵器数据
                    for value in all_values:
                        row = [f"aimming_level{value}"]
                        row.extend(tool_data["有灵器"][all_values.index(value)][1:])
                        merged_data.append(row)
                
                # 创建DataFrame
                df = pd.DataFrame(merged_data, columns=merged_columns)
                
                # 写入Excel工作表
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 获取工作表对象进行格式化
                worksheet = writer.sheets[sheet_name]
                
                # 插入角色信息行
                worksheet.insert_rows(1, 3)
                
                # 写入角色信息
                from openpyxl.utils import get_column_letter
                
                # 角色信息样式
                info_style = {
                    'font': {
                        'name': '微软雅黑',
                        'size': 12,
                        'bold': True
                    },
                    'fill': {
                        'type': 'solid',
                        'color': 'E6E6FA'
                    }
                }
                
                from write import write_and_format_cell
                write_and_format_cell(worksheet, 'A1', f"等级 {level} 角色数据", info_style)
                write_and_format_cell(worksheet, 'A2', f"包含无灵器和有灵器两种状态", info_style)
                
                # 写入表头
                for col_idx, col_name in enumerate(merged_columns, 1):
                    cell_address = f"{get_column_letter(col_idx)}4"
                    write_header_cell(worksheet, cell_address, col_name)
                
                # 写入数据并格式化
                data_start_row = 5
                data_start_col = 2  # 从B列开始（跳过第一列标签）
                
                # 找到gacha=12, 15, 20对应的列索引
                gacha_columns = {}
                for col_idx, col_name in enumerate(merged_columns):
                    if any(gacha in col_name for gacha in ["12th", "15th", "20th"]):
                        # 从列名中提取gacha数字
                        for gacha_num in [12, 15, 20]:
                            if f"{gacha_num}th" in col_name:
                                gacha_columns[gacha_num] = col_idx
                                break
                
                # 分别收集无灵器和有灵器在gacha=12, 15, 20列的最大值
                max_values = {}
                
                # 直接从tool_data中获取数据，避免索引问题
                for gacha_num in [12, 15, 20]:
                    if gacha_num in gacha_columns:
                        col_idx = gacha_columns[gacha_num]
                        max_values[gacha_num] = {'no_tool': None, 'has_tool': None}
                        
                        # 找无灵器最大值
                        if "无灵器" in tool_data:
                            no_tool_max_value = 0
                            no_tool_max_cells = []
                            for row_idx, row_data in enumerate(tool_data["无灵器"]):
                                ratio = row_data[col_idx]
                                # 确保ratio是数值类型
                                if isinstance(ratio, str):
                                    try:
                                        ratio = float(ratio)
                                    except ValueError:
                                        continue
                                if ratio > no_tool_max_value:
                                    no_tool_max_value = ratio
                                    # 计算实际的行号（跳过标题行）
                                    actual_row = data_start_row + 1 + row_idx
                                    no_tool_max_cells = [f"{get_column_letter(col_idx + 1)}{actual_row}"]
                                elif ratio == no_tool_max_value:
                                    actual_row = data_start_row + 1 + row_idx
                                    no_tool_max_cells.append(f"{get_column_letter(col_idx + 1)}{actual_row}")
                            
                            max_values[gacha_num]['no_tool'] = {
                                'value': no_tool_max_value,
                                'cells': no_tool_max_cells
                            }
                        
                        # 找有灵器最大值
                        if "有灵器" in tool_data:
                            has_tool_max_value = 0
                            has_tool_max_cells = []
                            for row_idx, row_data in enumerate(tool_data["有灵器"]):
                                ratio = row_data[col_idx]
                                # 确保ratio是数值类型
                                if isinstance(ratio, str):
                                    try:
                                        ratio = float(ratio)
                                    except ValueError:
                                        continue
                                if ratio > has_tool_max_value:
                                    has_tool_max_value = ratio
                                    # 计算实际的行号（跳过标题行、数据行、空行、标题行）
                                    actual_row = data_start_row + 1 + len(all_values) + 2 + row_idx
                                    has_tool_max_cells = [f"{get_column_letter(col_idx + 1)}{actual_row}"]
                                elif ratio == has_tool_max_value:
                                    actual_row = data_start_row + 1 + len(all_values) + 2 + row_idx
                                    has_tool_max_cells.append(f"{get_column_letter(col_idx + 1)}{actual_row}")
                            
                            max_values[gacha_num]['has_tool'] = {
                                'value': has_tool_max_value,
                                'cells': has_tool_max_cells
                            }
                
                # 写入数据行
                current_row = data_start_row
                
                # 处理无灵器数据
                if "无灵器" in tool_data:
                    # 写入无灵器标题
                    title_cell = f"A{current_row}"
                    title_style = {
                        'font': {
                            'name': '微软雅黑',
                            'size': 12,
                            'bold': True
                        },
                        'fill': {
                            'type': 'solid',
                            'color': 'FFE6CC'
                        }
                    }
                    write_and_format_cell(worksheet, title_cell, "无灵器", title_style)
                    current_row += 1
                    
                    # 写入无灵器数据
                    for row_idx, value in enumerate(all_values):
                        # 写入行标签
                        label_cell = f"A{current_row}"
                        write_and_format_cell(worksheet, label_cell, f"aimming_level{value}")
                        
                        for col_idx, col_name in enumerate(merged_columns[1:], 1):  # 跳过第一列
                            cell_address = f"{get_column_letter(col_idx + 1)}{current_row}"
                            ratio = merged_data[current_row - data_start_row][col_idx]
                            
                            # 检查是否为gacha=12, 15, 20的列
                            gacha_num = None
                            for gacha_col in gacha_columns:
                                if col_idx == gacha_columns[gacha_col]:
                                    gacha_num = gacha_col
                                    break
                            
                            # 写入数据
                            if gacha_num is not None:
                                # 先写入普通格式，稍后更新为最大值格式
                                write_percentage_cell(worksheet, cell_address, ratio)
                            else:
                                write_percentage_cell(worksheet, cell_address, ratio)
                        
                        current_row += 1
                    
                    # 添加空行分隔
                    if "有灵器" in tool_data:
                        current_row += 1
                
                # 处理有灵器数据
                if "有灵器" in tool_data:
                    # 写入有灵器标题
                    title_cell = f"A{current_row}"
                    title_style = {
                        'font': {
                            'name': '微软雅黑',
                            'size': 12,
                            'bold': True
                        },
                        'fill': {
                            'type': 'solid',
                            'color': 'E6F3FF'
                        }
                    }
                    write_and_format_cell(worksheet, title_cell, "有灵器", title_style)
                    current_row += 1
                    
                    # 写入有灵器数据
                    for row_idx, value in enumerate(all_values):
                        # 写入行标签
                        label_cell = f"A{current_row}"
                        write_and_format_cell(worksheet, label_cell, f"aimming_level{value}")
                        
                        for col_idx, col_name in enumerate(merged_columns[1:], 1):  # 跳过第一列
                            cell_address = f"{get_column_letter(col_idx + 1)}{current_row}"
                            ratio = merged_data[current_row - data_start_row][col_idx]
                            
                            # 检查是否为gacha=12, 15, 20的列
                            gacha_num = None
                            for gacha_col in gacha_columns:
                                if col_idx == gacha_columns[gacha_col]:
                                    gacha_num = gacha_col
                                    break
                            
                            # 写入数据
                            if gacha_num is not None:
                                # 先写入普通格式，稍后更新为最大值格式
                                write_percentage_cell(worksheet, cell_address, ratio)
                            else:
                                write_percentage_cell(worksheet, cell_address, ratio)
                        
                        current_row += 1
                
                # 重新写入最大值单元格并设置颜色
                for gacha_num, max_info in max_values.items():
                    # 设置无灵器最大值
                    if max_info['no_tool']:
                        for cell_address in max_info['no_tool']['cells']:
                            write_max_value_cell(worksheet, cell_address, max_info['no_tool']['value'], gacha_num)
                    
                    # 设置有灵器最大值
                    if max_info['has_tool']:
                        for cell_address in max_info['has_tool']['cells']:
                            write_max_value_cell(worksheet, cell_address, max_info['has_tool']['value'], gacha_num)
                
                # 添加数据条
                data_end_row = current_row - 1
                data_end_col = len(merged_columns)
                apply_data_bars(worksheet, data_start_row, data_start_col, data_end_row, data_end_col)
                
                # 添加图例
                legend_start_row = data_end_row + 3
                write_gacha_legend(worksheet, legend_start_row, 1)



def main():
    """主函数"""
    simulator = Simulator()
    #simulator.simulate_attribute_value_ratio(draw_count=15, rounds=1000, threshold=7)
    #simulator.simulate_card_drawing(15)
    simulator.simulate_and_generate_csv(draw_count=20, rounds=1000)

if __name__ == "__main__":
    main()
