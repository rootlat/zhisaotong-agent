"""
为整个项目生成日志的工具
"""
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.config_handler import prompt_conf


def load_prompt(prompt_file_path: str, prompt_def_name: str) -> str:
    """
    通用的提示词加载函数
    :param prompt_file_path: 配置文件中的键名，例如 "main_prompt_path"
    :param prompt_def_name: 用于日志显示的提示词名称，例如 "system_prompts"
    :return: 文件内容字符串
    """
    try:
        file_path = get_abs_path(prompt_file_path)
    except KeyError as e:
        logger.error(f"[{prompt_def_name}] 在yaml配置中未找到路径：{prompt_file_path}")
        raise e

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            logger.info(f"[{prompt_def_name}] 提示词加载成功 | 路径：{file_path}")
            return content
    except Exception as e:
        logger.error(f"[{prompt_def_name}] 读取失败：{str(e)}")
        raise e


def load_system_prompts() -> str:
    return load_prompt(prompt_conf["main_prompt_path"], "system_prompts")

def load_rag_prompts() -> str:
    return load_prompt(prompt_conf["rag_summarize_prompt_path"], "rag_prompts")

def load_report_prompts() -> str:
    return load_prompt(prompt_conf["report_prompt_path"], "report_prompts")