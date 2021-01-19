"""

版本路由区分

# 可以在这里添加所需要的依赖
https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-fastapi

"""

from fastapi import APIRouter, Depends

from common.deps import check_jwt_token

from .auth.endpoints import router as auth_router
from .items.endpoints import router as items_router
from .items.sys_scheduler import router as scheduler_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router, prefix="/admin/auth", tags=["用户"])
api_v1_router.include_router(items_router, tags=["测试API"], dependencies=[Depends(check_jwt_token)])
api_v1_router.include_router(scheduler_router, tags=["任务调度"])  # 可以添加验证token dependencies=[Depends(check_jwt_token)]
