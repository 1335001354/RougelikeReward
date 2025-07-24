from character import Character
from ProDistribution import ProDistribution
from type import Style
import random
import csv

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
                if character.get_attribute_value(character.attribute) > threshold:
                    success_count += 1
            ratio = success_count / rounds
            print(f"  自身流派属性值>{threshold}的比例 = {ratio:.3f}")

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
        
        # 生成CSV文件
        self._generate_csv_files(character_stats, draw_count, rounds)
        
        print("CSV文件生成完成！")
    
    def _generate_csv_files(self, character_stats, draw_count, rounds):
        """生成CSV文件"""
        character_names = [
            "熔岩球_lv5_toolFalse",
            "熔岩球_lv5_toolTrue", 
            "熔岩球_lv18_toolFalse",
            "熔岩球_lv18_toolTrue",
            "熔岩球_lv35_toolFalse",
            "熔岩球_lv35_toolTrue"
        ]
        
        for i, character in enumerate(self.characters):
            filename = f"{character_names[i]}.csv"
            print(f"  生成文件: {filename}")
            
            # 获取该角色所有可能的属性值
            all_values = set()
            for draw in range(draw_count + 1):
                all_values.update(character_stats[i][draw].keys())
            all_values = sorted(list(all_values))
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                header = [''] + [f"The {j}th gacha" for j in range(draw_count + 1)]
                writer.writerow(header)
                
                # 写入数据行
                for value in all_values:
                    row = [f"aimming_level{value}"]
                    for draw in range(draw_count + 1):
                        count = character_stats[i][draw].get(value, 0)
                        ratio = count / rounds
                        row.append(f"{ratio:.4f}")
                    writer.writerow(row)



def main():
    """主函数"""
    simulator = Simulator()
    #simulator.simulate_attribute_value_ratio(draw_count=15, rounds=1000, threshold=7)
    #simulator.simulate_card_drawing(15)
    simulator.simulate_and_generate_csv(draw_count=15, rounds=1000)

if __name__ == "__main__":
    main()
