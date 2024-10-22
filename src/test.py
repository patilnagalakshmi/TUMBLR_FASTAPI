'''Test for FastAPI Application'''
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_index():
    '''Test the index route'''
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Text": "Tumblr app management using fastapi"}

def test_create_post(mocker):
    '''Test the create post route'''
    mock_post = mocker.patch('requests.post')
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value ={
        "meta": {
            "status": 201,
            "msg": "Created"
            },
            "response": {
                "id": 123456789,
                "id_string": "123456789",
                "state": "published",
                "display_text": "Posted to test_blog"
                }
                }
    mock_post.return_value = mock_response
    response = client.post("/create",
                           params={"type":"text","title": "Test Title", "body": "Test Body"})
    assert response.status_code == 200
def test_get_posts(mocker):
    '''Test get posts route'''
    mock_response = {
        "response": {
            "posts": [
                {
                    "id": 1,
                    "id_string": "1",
                    "type": "text",
                    "summary": "Test summary",
                    "post_url": "https://example.com/test",
                }
            ]
        }
    }
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    response = client.get("/display")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["post_id"] == 1
    assert posts[0]["post_summary"] == "Test summary"
def test_search_post(mocker):
    '''Test search post route'''
    mock_response = {
        "response": [
            {
                "blog_name": "test_blog",
                "type": "text",
                "summary": "This is a test post",
                "post_url": "https://example.com/test",
            }
        ]
    }
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    response = client.get("/search", params={"tag": "test_tag"})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["blog_name"] == "test_blog"
def test_delete_post(mocker):
    '''Test delete post route'''
    mock_post = mocker.patch('requests.post')
    mock_post.return_value.status_code = 200
    response = client.delete("/delete/12345")
    assert response.status_code == 200
    assert response.json() == {"detail": "The post deleted successfully"}
