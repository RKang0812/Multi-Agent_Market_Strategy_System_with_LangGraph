"""
Helper utility functions
辅助工具函数
"""

from typing import Dict, Any
import json


def format_json_output(data: Any, indent: int = 2) -> str:
    """
    Format data as pretty JSON
    将数据格式化为美观的 JSON
    
    Args:
        data: Data to format / 要格式化的数据
        indent: Indentation spaces / 缩进空格数
        
    Returns:
        Formatted JSON string / 格式化的 JSON 字符串
    """
    if hasattr(data, 'dict'):
        # Pydantic model / Pydantic 模型
        data = data.dict()
    return json.dumps(data, indent=indent, ensure_ascii=False)


def safe_get(dictionary: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary value
    安全地获取嵌套字典值
    
    Args:
        dictionary: Dictionary to access / 要访问的字典
        *keys: Nested keys / 嵌套键
        default: Default value if key not found / 如果未找到键的默认值
        
    Returns:
        Value or default / 值或默认值
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        else:
            return default
    return result


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    将文本截断到最大长度
    
    Args:
        text: Text to truncate / 要截断的文本
        max_length: Maximum length / 最大长度
        suffix: Suffix to add if truncated / 如果截断则添加的后缀
        
    Returns:
        Truncated text / 截断的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_input(company_domain: str, industry: str, project_description: str) -> tuple[bool, str]:
    """
    Validate user input
    验证用户输入
    
    Args:
        company_domain: Company domain / 公司域名
        industry: Industry / 行业
        project_description: Project description / 项目描述
        
    Returns:
        Tuple of (is_valid, error_message) / (是否有效, 错误消息) 元组
    """
    if not company_domain or not company_domain.strip():
        return False, "Company domain is required / 公司域名为必填项"
    
    if not industry or not industry.strip():
        return False, "Industry is required / 行业为必填项"
    
    if not project_description or not project_description.strip():
        return False, "Project description is required / 项目描述为必填项"
    
    if len(project_description) < 50:
        return False, "Project description should be at least 50 characters / 项目描述至少需要 50 个字符"
    
    return True, ""
