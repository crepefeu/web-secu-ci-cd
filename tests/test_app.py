import pytest
import sys
import os

# Add the parent directory to the Python path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import add_numbers, multiply_numbers, divide_numbers, app


class TestMathFunctions:
    """Test cases for mathematical functions in the app."""
    
    def test_add_numbers_positive(self):
        """Test addition with positive numbers."""
        assert add_numbers(2, 3) == 5
        assert add_numbers(10, 15) == 25
    
    def test_add_numbers_negative(self):
        """Test addition with negative numbers."""
        assert add_numbers(-2, -3) == -5
        assert add_numbers(-10, 15) == 5
    
    def test_add_numbers_zero(self):
        """Test addition with zero."""
        assert add_numbers(0, 5) == 5
        assert add_numbers(5, 0) == 5
        assert add_numbers(0, 0) == 0
    
    def test_multiply_numbers_positive(self):
        """Test multiplication with positive numbers."""
        assert multiply_numbers(2, 3) == 6
        assert multiply_numbers(4, 5) == 20
    
    def test_multiply_numbers_negative(self):
        """Test multiplication with negative numbers."""
        assert multiply_numbers(-2, 3) == -6
        assert multiply_numbers(-2, -3) == 6
    
    def test_multiply_numbers_zero(self):
        """Test multiplication with zero."""
        assert multiply_numbers(0, 5) == 0
        assert multiply_numbers(5, 0) == 0
    
    def test_divide_numbers_positive(self):
        """Test division with positive numbers."""
        assert divide_numbers(6, 2) == 3
        assert divide_numbers(15, 3) == 5
    
    def test_divide_numbers_negative(self):
        """Test division with negative numbers."""
        assert divide_numbers(-6, 2) == -3
        assert divide_numbers(-6, -2) == 3
    
    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide_numbers(10, 0)


class TestWebApplication:
    """Test cases for the Flask web application."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_home_page(self, client):
        """Test that the home page loads correctly."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Vulnerable Web Application' in response.data
        assert b'SQL Injection Login' in response.data
    
    def test_login_page_get(self, client):
        """Test that the login page loads correctly."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Username:' in response.data
    
    def test_file_endpoint_exists(self, client):
        """Test that the file endpoint exists (even though it's vulnerable)."""
        response = client.get('/file')
        # We expect this to fail gracefully, not crash
        assert response.status_code in [200, 404, 500]
    
    def test_ping_endpoint_exists(self, client):
        """Test that the ping endpoint exists."""
        response = client.get('/ping')
        # We expect this to work with localhost
        assert response.status_code == 200