from type import Style

class Character:
    def __init__(self, attribute, level=1, havetool=False):
        """
        初始化角色
        
        Args:
            attribute: 角色属性
            level: 角色等级，默认为1
            havetool: 是否拥有工具，默认为False
        """
        self.attribute = attribute
        self.level = level
        self.havetool = havetool
        
        # 创建流派实例
        self.style = Style("默认流派")
        
        # 根据等级确定可用的技能，并设置attribute_values
        self._initialize_attribute_values()
    
    def _initialize_attribute_values(self):
        """根据等级初始化属性值"""
        # 获取等级以下的所有流派
        available_styles = self.style.get_skills_below_level(self.level + 1)
        
        # 根据可用流派动态创建属性值字典
        # 每个流派对应一个属性，属性名为流派名
        self.attribute_values = {}
        for style in available_styles:
            # 如果havetool为True，且该流派是角色自身的属性，则设置为1，否则设置为0
            if self.havetool and style == self.attribute:
                self.attribute_values[style] = 1
            else:
                self.attribute_values[style] = 0
        
        # 计算流派拥有数量
        self._update_style_count()
    
    def _update_style_count(self):
        """更新流派拥有数量"""
        self.style_count = sum(1 for value in self.attribute_values.values() if value > 0)

    def get_attribute_value(self, attribute_name):
        """
        获取指定属性名称的数值
        
        Args:
            attribute_name: 属性名称（字符串）
            
        Returns:
            int: 属性数值，如果属性不存在返回0
        """
        return self.attribute_values.get(attribute_name, 0)
    
    def set_attribute_value(self, attribute_name, value):
        """
        设置指定属性名称的数值
        
        Args:
            attribute_name: 属性名称（字符串）
            value: 要设置的数值（整数）
        """
        if attribute_name in self.attribute_values:
            self.attribute_values[attribute_name] = value
            # 更新流派拥有数量
            self._update_style_count()
        else:
            raise ValueError(f"属性名称 '{attribute_name}' 不存在")
    
    def increase_attribute_value(self, attribute_name, increment=1):
        """
        增加指定属性名称的数值
        
        Args:
            attribute_name: 属性名称（字符串）
            increment: 增加的数值，默认为1
        """
        if attribute_name in self.attribute_values:
            self.attribute_values[attribute_name] += increment
            # 更新流派拥有数量
            self._update_style_count()
        else:
            raise ValueError(f"属性名称 '{attribute_name}' 不存在")
    
    def get_all_attribute_values(self):
        """
        获取所有属性数值的字典
        
        Returns:
            dict: 包含所有属性名称和数值的字典
        """
        return self.attribute_values.copy()
    
    def reset_all_attributes(self):
        """重置所有属性数值，结合havetool参数"""
        self._initialize_attribute_values()
    
    def set_level(self, new_level):
        """
        设置角色等级并重新计算属性值
        
        Args:
            new_level: 新的等级值
        """
        self.level = new_level
        self._initialize_attribute_values()
    
    def get_level(self):
        """
        获取角色等级
        
        Returns:
            int: 角色等级
        """
        return self.level
    
    def get_available_skills(self):
        """
        获取当前等级可用的技能
        
        Returns:
            list: 可用技能列表
        """
        return self.style.get_skills_below_level(self.level + 1)
    
    def get_probability_distribution(self, pro_distribution):
        """
        根据当前角色等级获取ProDistribution的概率分布
        
        Args:
            pro_distribution: ProDistribution实例
            
        Returns:
            dict: 当前等级对应的概率分布字典
        """
        return pro_distribution.get_current_weight(self)
    
    def get_style_count(self):
        """
        获取流派拥有数量
        
        Returns:
            int: 当前拥有数量大于0的流派数量
        """
        return self.style_count
    
    def get_havetool(self):
        """
        获取是否拥有工具
        
        Returns:
            bool: 是否拥有工具
        """
        return self.havetool
    
    def set_havetool(self, havetool):
        """
        设置是否拥有工具
        
        Args:
            havetool: 是否拥有工具（bool）
        """
        self.havetool = havetool
        # 重新初始化属性值
        self._initialize_attribute_values()
    
    def get_attribute_summary(self):
        """
        获取属性摘要信息
        
        Returns:
            str: 包含所有属性信息的字符串
        """
        summary = f"角色属性: {self.attribute}\n"
        summary += f"角色等级: {self.level}\n"
        summary += f"拥有工具: {self.havetool}\n"
        summary += f"流派拥有数量: {self.style_count}\n"
        summary += "属性数值:\n"
        for attr_name, value in self.attribute_values.items():
            summary += f"  {attr_name}: {value}\n"
        
        # 添加可用流派信息
        available_styles = self.get_available_skills()
        summary += f"可用流派数量: {len(available_styles)}\n"
        summary += f"可用流派: {available_styles}\n"
        
        return summary

    def __str__(self):
        return f"Character(attribute={self.attribute}, level={self.level}, havetool={self.havetool}, style_count={self.style_count}, values={self.attribute_values})"

    def __repr__(self):
        return f"Character(attribute={self.attribute}, level={self.level}, havetool={self.havetool}, style_count={self.style_count}, values={self.attribute_values})"

    def __eq__(self, other):
        return (self.attribute == other.attribute and 
                self.level == other.level and 
                self.havetool == other.havetool and
                self.style_count == other.style_count and
                self.attribute_values == other.attribute_values)