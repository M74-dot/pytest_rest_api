import requests
import uuid


# endpoint that we are going to test
ENDPOINT = "https://todo.pixegami.io"

response = requests.get(ENDPOINT)
# print(response)

data = response.json()
# print(data)

status_code = response.status_code
# print(status_code)


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["is_done"] == payload["is_done"]


def test_can_update_task():
    # create task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id, 
        "content": "my updated content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get task and validate
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    data = get_task_response.json()
    assert data["content"] == new_payload["content"]
    assert data["is_done"] == new_payload["is_done"]


def test_can_list_tasks():
    # create N tasks
    n = 3
    payload = new_task_payload()
    for i in range(n):
        response = create_task(payload)
        assert response.status_code == 200

    # list tasks and check that there an N items
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # get the task, and test that ast is not exists
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
