"""
yaml
k: v
"""
import yaml
from utils.path_tool import get_abs_path

# 通用配置加载函数
def load_config(filename: str) -> dict:
    path = get_abs_path(f"config/{filename}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载所有配置
mysql_conf = load_config("mysql.yml")
redis_conf = load_config("redis.yml")
milvus_conf = load_config("milvus.yml")
rabbitmq_conf = load_config("rabbitmq.yml")
jwt_conf = load_config("jwt.yml")
prompt_conf = load_config("prompt.yml")
path_conf = load_config("path.yml")
rag_conf = load_config("rag.yml")
agent_conf = load_config("agent.yml")