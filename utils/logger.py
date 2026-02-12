"""
Logging configuration
"""

import logging
import sys


def setup_logger(name: str = "marketing_strategy", level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger / 将处理器添加到日志记录器
    logger.addHandler(handler)
    
    return logger
