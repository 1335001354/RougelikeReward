class Style:
    """流派类"""
    
    # 类变量：流派技能字典 {技能名称: 技能等级}
    style_skills = {
        "熔岩球": 1,
        "寒冰彗星": 1,
        "电球": 2,
        "黑洞": 5,
        "闪电核心": 7,
        "冰刺": 10,
        "风刃": 13,
        "岩崩": 18,
        "火雨": 22,
        "气流屏障": 27,
        "岩壳共鸣": 32,
        "暗影之爪": 35
    }
    
    def __init__(self, name="默认流派"):
        """
        初始化流派
        
        Args:
            name: 流派名称，默认为"默认流派"
        """
        self.name = name
        self.skills = self.style_skills.copy()  # 复制类变量到实例变量
    
    
    def get_all_skills(self):
        """
        获取所有技能信息
        
        Returns:
            dict: 包含所有技能名称和等级的字典
        """
        return self.skills.copy()
    
    def get_skills_by_level_range(self, min_level, max_level):
        """
        获取指定等级范围内的技能
        
        Args:
            min_level: 最小等级（包含）
            max_level: 最大等级（包含）
            
        Returns:
            dict: 符合条件的技能字典
        """
        return {skill: level for skill, level in self.skills.items() 
                if min_level <= level <= max_level}
    
    
    def get_skills_below_level(self, max_level):
        """
        获取等级小于指定值的所有技能
        
        Args:
            max_level: 最大等级（不包含）
            
        Returns:
            list: 等级小于max_level的技能名称列表
        """
        return [skill for skill, skill_level in self.skills.items() if skill_level < max_level]
    
    
    
    def get_skill_count(self):
        """
        获取技能总数
        
        Returns:
            int: 技能数量
        """
        return len(self.skills)
    
    def print_skills(self, sort_by_level=True):
        """
        打印所有技能信息
        
        Args:
            sort_by_level: 是否按等级排序，默认为True
        """
        print(f"流派: {self.name}")
        print("技能列表:")
        print("-" * 30)
        
        if sort_by_level:
            # 按等级排序
            sorted_skills = sorted(self.skills.items(), key=lambda x: x[1])
        else:
            # 按名称排序
            sorted_skills = sorted(self.skills.items())
        
        for skill_name, level in sorted_skills:
            print(f"  {skill_name}: 等级 {level}")
    
    def get_skill_summary(self):
        """
        获取技能摘要信息
        
        Returns:
            str: 包含技能摘要信息的字符串
        """
        summary = f"流派: {self.name}\n"
        summary += f"技能总数: {self.get_skill_count()}\n"
        
        
        return summary
    
    def __str__(self):
        return f"Style(name='{self.name}', skills_count={self.get_skill_count()})"
    
    def __repr__(self):
        return f"Style(name='{self.name}', skills={self.skills})"
    
    def __eq__(self, other):
        return self.name == other.name and self.skills == other.skills


# 示例用法
if __name__ == "__main__":
    # 创建流派实例
    style = Style("元素流派")
    
    # 打印所有技能
    style.print_skills()
    
    # 打印摘要
    print("\n" + "=" * 40)
    print(style.get_skill_summary())
    
    # 测试各种方法
    print("\n" + "=" * 40)
    print("测试各种方法:")
    
    
    # 测试新方法：获取等级小于指定值的技能
    below_5_skills = style.get_skills_below_level(5)
    print(f"等级小于5的技能: {below_5_skills}")
    
    below_10_skills = style.get_skills_below_level(10)
    print(f"等级小于10的技能: {below_10_skills}")
    
    below_20_skills = style.get_skills_below_level(20)
    print(f"等级小于20的技能: {below_20_skills}")
