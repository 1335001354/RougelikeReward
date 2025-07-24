from character import Character
from ProDistribution import ProDistribution
from type import Style
import random
import csv
import pandas as pd

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
        """模拟多轮并生成CSV文件，统计每个角色在每次抽卡后自身流派属性值的分布"""
        print(f"\n=== 模拟{rounds}轮，每轮{draw_count}次抽卡，生成CSV文件 ===")
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
        character_names = [
            "熔岩球_lv5_无灵器",
            "熔岩球_lv5_有灵器", 
            "熔岩球_lv18_无灵器",
            "熔岩球_lv18_有灵器",
            "熔岩球_lv35_无灵器",
            "熔岩球_lv35_有灵器"
        ]
        
        filename = "simulation_results.xlsx"
        print(f"  生成文件: {filename}")
        
        # 创建Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for i, character in enumerate(self.characters):
                # 获取该角色所有可能的属性值
                all_values = set()
                for draw in range(draw_count + 1):
                    all_values.update(character_stats[i][draw].keys())
                all_values = sorted(list(all_values))
                
                # 创建数据框
                data = []
                for value in all_values:
                    row = [f"aimming_level{value}"]
                    for draw in range(draw_count + 1):
                        count = character_stats[i][draw].get(value, 0)
                        ratio = count / rounds
                        row.append(f"{ratio:.4f}")
                    data.append(row)
                
                # 创建列名
                columns = [''] + [f"The {j}th gacha" for j in range(draw_count + 1)]
                
                # 创建DataFrame
                df = pd.DataFrame(data, columns=columns)
                
                # 获取havetool的中文描述
                havetool_text = "有灵器" if character.get_havetool() else "无灵器"
                
                # 写入Excel工作表
                sheet_name = f"等级{character.get_level()}_{havetool_text}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 添加角色信息到工作表
                worksheet = writer.sheets[sheet_name]
                worksheet.insert_rows(1, 3)  # 在顶部插入3行
                worksheet['A1'] = f"角色信息: {character_names[i]}"
                worksheet['A2'] = f"等级: {character.get_level()}, 灵器: {havetool_text}"
                worksheet['A3'] = ""  # 空行



def main():
    """主函数"""
    simulator = Simulator()
    #simulator.simulate_attribute_value_ratio(draw_count=15, rounds=1000, threshold=7)
    #simulator.simulate_card_drawing(15)
    simulator.simulate_and_generate_csv(draw_count=20, rounds=1000)

if __name__ == "__main__":
    main()
