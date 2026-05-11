import aio_pika
import json
from utils.config_handler import rabbitmq_conf
from utils.logger_handler import logger


class RabbitMQService:
    """
    RabbitMQ 异步消息队列服务
    用于：文件上传 → 异步解析入库
    完全类封装，生产级标准
    """

    def __init__(self):
        self.url = f"amqp://{rabbitmq_conf['user']}:{rabbitmq_conf['password']}@{rabbitmq_conf['host']}:{rabbitmq_conf['port']}/"
        self.queue_name = rabbitmq_conf['file_parse_queue']
        self.connection = None
        self.channel = None

    async def init(self):
        """初始化连接 + 声明队列"""
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            # 声明队列持久化
            await self.channel.declare_queue(self.queue_name, durable=True)
            logger.info(f"✅ RabbitMQ 连接成功 | 队列：{self.queue_name}")
        except Exception as e:
            logger.error(f"❌ RabbitMQ 连接失败：{str(e)}", exc_info=True)

    async def send_parse_task(self, file_id: int, user_id: int, file_md5: str, file_path: str):
        """发送文件解析任务（生产者）"""
        try:
            message = {
                "file_id": file_id,
                "user_id": user_id,
                "file_md5": file_md5,
                "file_path": file_path
            }

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=self.queue_name
            )
            logger.info(f"📤 发送解析任务成功 | file_id={file_id}")
        except Exception as e:
            logger.error(f"📤 发送解析任务失败：{str(e)}", exc_info=True)

    async def start_consumer(self, handler):
        """启动消费者（后台监听）"""
        try:
            queue = await self.channel.declare_queue(self.queue_name, durable=True)
            logger.info(f"📥 RabbitMQ 消费者已启动，监听队列：{self.queue_name}")

            async with queue.iterator() as q:
                async for msg in q:
                    async with msg.process():
                        data = json.loads(msg.body)
                        await handler(data)
        except Exception as e:
            logger.error(f"📥 消费者异常：{str(e)}", exc_info=True)


# ====================== 全局单例 ======================
rabbit_service = RabbitMQService()