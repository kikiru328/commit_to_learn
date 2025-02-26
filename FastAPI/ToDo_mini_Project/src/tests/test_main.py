from database.orm import ToDo

def test_health_check(client):
    response = client.get("/") # ping: pong
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

def test_get_todos(client, mocker):
    # mocking before functions work
    mocker.patch("main.get_todos", return_value=[
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    # order=ASC
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }

def test_get_todo(client, mocker):
    # 200
    #mocking
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    response = client.get("/todos/1") #path, test
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

    #404
    #mocking
    mocker.patch("main.get_todo_by_todo_id", return_value=None,)
    response = client.get("/todos/1") #path, test
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not Found"}

def test_create_todo(client, mocker):
    #spy: tracking object
    create_spy = mocker.spy(ToDo, "create")

    #mocking
    mocker.patch(
        "main.create_todo",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    body = {
        "contents": "test",
        "is_done": False
    }
    response = client.post("/todos", json=body)
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

def test_update_todo(client, mocker):
    #200
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )

    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch(
        "main.update_todo",
        return_value=ToDo(id=1, contents="todo", is_done=False),
    )
    response = client.patch("/todos/1", json={"is_done": False}) #path, test

    undone.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": False}

    #404
    #mocking
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.patch("/todos/1", json={"is_done": True}) #path, test
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not Found"}

def test_delete_todo(client, mocker):
    # # 204
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    mocker.patch("main.delete_todo", return_value=None)
    response = client.delete("/todos/1") #path, test
    assert response.status_code == 204

    #404
    #mocking
    mocker.patch("main.get_todo_by_todo_id", return_value=None,)
    response = client.delete("/todos/1") #path, test
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not Found"}