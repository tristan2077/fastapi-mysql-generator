from datetime import datetime

from fastapi import APIRouter, Request, Query, Body

from common import response_code
from utils.cron_task import demo_task

router = APIRouter()


@router.get("/jobs/all", summary="获取所有job信息")
async def get_scheduled_syncs(request: Request):
    """
    获取所有job
    :return:
    """
    schedules = []
    for job in request.app.state.schedule.get_jobs():
        schedules.append(
            {"job_id": job.id, "func_name": job.func_ref, "func_args": job.args, "cron_model": str(job.trigger),
             "next_run": str(job.next_run_time)}
        )

    return response_code.resp_200(data=schedules)


@router.get("/jobs/once", summary="获取指定的job信息")
async def get_target_sync(
        request: Request,
        job_id: str = Query(..., title="任务id")
):
    job = request.app.state.schedule.get_job(job_id=job_id)

    if not job:
        return response_code.resp_4001(message=f"not found job {job_id}")

    return response_code.resp_200(
        data={"job_id": job.id, "func_name": job.func_ref, "func_args": job.args, "cron_model": str(job.trigger),
              "next_run": str(job.next_run_time)})


@router.post("/job/schedule/", summary="开始job调度")
async def add_job_to_scheduler(
        request: Request,
        *,
        seconds: int = Body(120, title="循环间隔时间/秒,默认120s", embed=True),
        job_id: str = Body(..., title="任务id", embed=True),
):
    """
    简易的任务调度演示 可自行参考文档 https://apscheduler.readthedocs.io/en/stable/
    三种模式
    date: use when you want to run the job just once at a certain point of time
    interval: use when you want to run the job at fixed intervals of time
    cron: use when you want to run the job periodically at certain time(s) of day
    :param request:
    :param seconds:
    :param job_id:
    :return:
    """
    res = request.app.state.schedule.get_job(job_id=job_id)
    if res:
        return response_code.resp_4001(message=f"{job_id} job already exists")

    schedule_job = request.app.state.schedule.add_job(demo_task,
                                                      'interval',
                                                      args=(job_id,),
                                                      seconds=seconds,  # 循环间隔时间 秒
                                                      id=job_id,  # job ID
                                                      next_run_time=datetime.now()  # 立即执行
                                                      )
    return response_code.resp_200(data={"id": schedule_job.id})


@router.post("/job/del", summary="移除任务")
async def remove_schedule(
        request: Request,
        job_id: str = Body(..., title="job_id", embed=True)
):
    res = request.app.state.schedule.get_job(job_id=job_id)
    if not res:
        return response_code.resp_4001(message=f"not found job {job_id}")

    request.app.state.schedule.remove_job(job_id)

    return response_code.resp_200()
