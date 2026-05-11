"""
为整个项目提供文件绝对路径的工具
"""

import os


def get_project_root(root_name: str = "zhisaotong-agent") -> str:
    """
    获取项目根目录绝对路径
    :root_name: 指定项目根目录文件名称
    :return: 绝对路径
    """
    # 当前文件所在目录
    current = os.path.dirname(os.path.abspath(__file__))
    # 无限向上找，直到匹配根目录名
    while True:
        if os.path.basename(current) == root_name:
            return current
        # 到系统根目录还没找到，退出
        parent = os.path.dirname(current)
        if parent == current:
            raise FileNotFoundError(f"未找到项目根目录: {root_name}")
        current = parent


def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径，得到绝对路径
    :param relative_path: 相对领
    :return: 绝对路径
    """
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)