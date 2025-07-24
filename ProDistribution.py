class ProDistribution:
    """概率分布类 - 基于动态技能名称"""
    
    def __init__(self, initial_value=500, ratio=0.6):
        """
        初始化概率分布
        
        Args:
            initial_value: 基础权重值，默认为500
            ratio: 递减比例，默认为0.8
        """
        self.initial_value = initial_value
        self.ratio = ratio
    
    def get_current_weight(self, character):
        """
        返回每个流派在当前卡牌投放时的概率字典
        
        Args:
            character: Character类实例，包含attribute_values字典
            
        Returns:
            dict: 包含每个流派当前概率的字典 {str: float}
        """
        attribute_values = character.attribute_values
        style_count = character.get_style_count()
        
        # 创建结果字典，用于存储每个流派的当前权重
        current_weights = {}
        
        # 遍历角色的所有流派
        for style_name, style_value in attribute_values.items():
            # 如果流派拥有数量>=3，只保留角色拥有的流派（value>0）
            if style_count >= 3 and style_value == 0:
                continue  # 跳过未拥有的流派
            
            # 为每个流派创建一个简单的分布（这里使用默认分布）
            # 可以根据需要扩展为更复杂的分布逻辑
            if style_value == 0:
                current_weight = self.initial_value  # 基础权重
            else:
                current_weight = self.initial_value * (self.ratio ** style_value)  # 按流派值递减
            
            # 将权重存储到字典中
            current_weights[style_name] = current_weight
        
        # 计算所有权重之和
        total_weight = sum(current_weights.values())
        
        # 将权重转换为概率（每一项/所有项之和）
        current_probabilities = {}
        if total_weight > 0:
            for style_name, weight in current_weights.items():
                probability = weight / total_weight
                current_probabilities[style_name] = probability
        else:
            # 如果总权重为0，则所有概率相等
            num_styles = len(current_weights)
            equal_probability = 1.0 / num_styles if num_styles > 0 else 0.0
            for style_name in current_weights.keys():
                current_probabilities[style_name] = equal_probability
        
        return current_probabilities
    
    def get_style_weight(self, style_name, style_value):
        """
        获取单个流派的权重值
        
        Args:
            style_name: 流派名称
            style_value: 流派值
            
        Returns:
            float: 流派权重值
        """
        if style_value == 0:
            return self.initial_value
        else:
            return self.initial_value * (self.ratio ** style_value)
    
    def get_summary(self):
        """
        获取概率分布摘要信息
        
        Returns:
            str: 摘要信息字符串
        """
        summary = f"概率分布配置:\n"
        summary += f"  基础权重值: {self.initial_value}\n"
        summary += f"  递减比例: {self.ratio}\n"
        return summary
    
    def print_summary(self):
        """打印概率分布摘要信息"""
        print(self.get_summary())
    
    def __str__(self):
        return f"ProDistribution(initial_value={self.initial_value}, ratio={self.ratio})"
    
    def __repr__(self):
        return f"ProDistribution(initial_value={self.initial_value}, ratio={self.ratio})"


# 示例用法
if __name__ == "__main__":
    from character import Character
    from type import Style
    
    print("=== ProDistribution 测试 ===")
    
    # 创建概率分布实例
    pro_dist = ProDistribution(initial_value=100, ratio=0.8)
    print(f"创建概率分布: {pro_dist}")
    
    # 打印配置信息
    pro_dist.print_summary()
    
    # 创建角色实例
    character = Character("测试角色", 10)
    print(f"\n角色信息:")
    print(f"  等级: {character.get_level()}")
    print(f"  技能: {character.attribute_values}")
    
    # 获取概率分布
    probabilities = pro_dist.get_current_weight(character)
    print(f"\n概率分布:")
    for skill, prob in probabilities.items():
        print(f"  {skill}: {prob:.4f}")
    
    # 验证概率总和
    total_prob = sum(probabilities.values())
    print(f"概率总和: {total_prob:.6f}")
    
    print("\n测试完成！") 