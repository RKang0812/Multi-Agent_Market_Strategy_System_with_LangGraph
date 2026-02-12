"""
Logging configuration
日志配置
"""

import logging
import sys


def setup_logger(name: str = "marketing_strategy", level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with consistent formatting
    设置具有一致格式的日志记录器
    
    Args:
        name: Logger name / 日志记录器名称
        level: Logging level / 日志级别
        
    Returns:
        Configured logger / 配置的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers / 移除现有处理器
    logger.handlers = []
    
    # Create console handler / 创建控制台处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter / 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger / 将处理器添加到日志记录器
    logger.addHandler(handler)
    
    return logger
