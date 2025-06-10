import pytest
from src.app import app # 假设你的Flask应用实例在 src/app.py 中名为 app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_and_delete_server(client):
    # 1. 创建服务器所需的数据
    server_data = {
        "network_segment_id": 1,
        "service_tag": "test_service_tag_12345",
        "name": "test_server",
        "primary_ip": "192.168.1.100"
    }

    # 2. 发送POST请求创建服务器
    response = client.post("/api/server/", json=server_data)
    assert response.status_code == 201
    created_server = response.get_json()['data']
    server_id = created_server['id']
    assert server_id is not None

    # 3. 发送DELETE请求删除服务器
    delete_response = client.delete(f"/api/server/{server_id}")
    assert delete_response.status_code == 200

    # 4. 尝试使用GET请求获取已删除的服务器
    get_response = client.get(f"/api/server/{server_id}")
    assert get_response.status_code == 404 