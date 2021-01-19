import os
from common import logger

# 获取环境变量
env = os.getenv("ENV", "")
if env:
    # 如果有虚拟环境 则是 生产环境
    logger.info("----------生产环境启动------------")
    from .production_config import settings
else:
    # 没有则是开发环境
    logger.info("----------开发环境启动------------")
    from .development_config import settings
