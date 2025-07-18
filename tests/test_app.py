import unittest
import os

os.environ['TESTING'] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Portfolio Home</title>" in html
        assert "<h1>Our Group Portfolio</h1>" in html
        assert "<li><strong>Timeline</strong> - Share your thoughts and see what others have posted</li>" in html
        

        
    def test_timeline(self):
        # Get empty timeline posts
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        

        # Make a post to timeline posts
        # Testing timeline post
        test_post_response = self.client.post('/api/timeline_post',
                    data={"name": "John Doe", "email": "john@example.com", "content": "Hello World, I'm John!"})
        assert test_post_response.status_code == 200
        assert test_post_response.is_json
        test_json= test_post_response.get_json()
        
        
        assert test_json["name"] == "John Doe"
        assert test_json["email"] == "john@example.com"
        assert test_json["content"] == "Hello World, I'm John!"
        
        # Make get request to newly added timeline post
        get_response = self.client.get('/api/timeline_post')
        assert get_response.status_code == 200
        assert get_response.is_json
        get_json = get_response.get_json()
        # Make sure that there is one post in the timleine_posts array
        assert len(get_json["timeline_posts"]) == 1
        
        
        # Test timeline page 
        timeline_response = self.client.get('/timeline')
        assert timeline_response.status_code == 200
        timeline_html = timeline_response.get_data(as_text=True)    
        assert "<h2>Timeline</h2>" in timeline_html
        

        
    
    # testing edge cases
    def test_malformed_timline_post(self):
        # POST request missing name
       response = self.client.post('/api/timeline_post', data={ 'name': '', 'email': 'john@example.com', 'content': "Hello World, I'm john!" })
       assert response.status_code == 400
       html = response.get_data(as_text=True)
       assert 'Invalid name' in html
       
       # POST request missing content
       response = self.client.post('/api/timeline_post', data={ 'email': 'john@example.com', 'name': "John Doe", 'content': '' })
       assert response.status_code == 400
       html = response.get_data(as_text=True)
       assert 'Invalid content' in html
       
       # POST request missing or invalid email
       response = self.client.post('/api/timeline_post', data={ 'email': 'notanemail', 'content': "Hello World, I'm john!", 'name': 'John Doe' })
       assert response.status_code == 400
       html = response.get_data(as_text=True)
       assert 'Invalid email' in html
    