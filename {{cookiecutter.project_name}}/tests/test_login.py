"""
需要安装 pytest
pip install pytest

"""

from fastapi.testclient import TestClient

from api import create_app

app = create_app()

client = TestClient(app)


def test_login():
    """
    测试登录
    自行使用 /app/create_user.py 创建任意测试用户
    test@test.com
    test
    :return:
    """
    response = client.post("/admin/auth/login/access-token", json={
        "username": "test@test.com",
        "password": "test"
    })
    assert response.status_code == 200
    assert response.json().code == 200

