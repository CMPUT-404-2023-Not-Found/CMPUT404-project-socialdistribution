from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from author.models import Author

# This code is modified from a video tutorial from Bobby Stearman on 2022-11-28 retrieved on 2023-02-15, to Youtube freeCodeCamp.org
# video here:
# https://www.youtube.com/watch?v=tujhGdn1EMI
# Module 4: Write unit tests 44:50

# Used ideas from below website resources: 
# Password validation and strength tests:
# Tutorialspoint: https://www.tutorialspoint.com/strong-password-checker-in-python 
# OWASP: https://owasp.org/www-community/password-special-characters
# Username validation tests:
# ConstantContact: https://knowledgebase.constantcontact.com/articles/KnowledgeBase/5890-characters-that-are-allowed-for-user-names?lang=en_US

class AuthorTestCase(APITestCase):
    '''
    Test suite for Author model
    '''
    def setUp(self):
        self.client = APIClient()
        self.data = { 
            'username': 'testme01',
            'password': 'P*ssw0rd!',
        }
        self.url = '/api/authors/'
    
    def test_create_author(self):
        '''
        AuthorView: test legit create
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().username, data['username'])

    def test_create_author_without_username(self):
        '''
        AuthorView: test when username is not present in data
        '''
        data = self.data
        data.pop("username")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_without_password(self):
        """
        AuthorView: test when password is not present in data
        """
        data = self.data
        data.pop("password")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_author_without_username_and_password(self):
        """
        AuthorView: test when both username and password are not present in data
        """
        data = self.data
        data.pop("username")
        data.pop("password")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_when_username_equals_blank(self):
        """
        AuthorView: test when username is blank
        """
        data = self.data
        data["username"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_when_password_equals_blank(self):
        """
        AuthorView: test when password is blank
        """
        data = self.data
        data["password"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_author_when_both_username_and_passowrd_equal_blank(self):
        """
        AuthorView: test when both username and password are blank
        """
        data = self.data
        data["username"] = ""
        data["password"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_shorter_password_length(self):
        """
        AuthorView: test when password length is not at least 6-character long
        """
        data = self.data
        data["password"] = "P*ssw"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_longer_password_length(self):
        """
        AuthorView: test when password length is more than at most 20-character long
        """
        data = self.data
        data["password"] = "P*ssw0rd!P*ssw0rd!P*ssw0rd!"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_author_with_numeric_only_password(self):
        """
        AuthorView: test when password are only numeric characters
        """
        data = self.data
        data["password"] = "1234567890"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_author_with_alphabetical_only_password(self):
        """
        AuthorView: test when password are only letters
        """
        data = self.data
        data["password"] = "aBcDeFgH"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_author_with_lower_case_letter_only_password(self):
        """
        AuthorView: test when password are only lower case letters
        """
        data = self.data
        data["password"] = "password"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_author_with_upper_case_letter_only_password(self):
        """
        AuthorView: test when password is made of only upper case letters
        """
        data = self.data
        data["password"] = "PASSWORD"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_author_with_triple_same_letter_in_a_row_password(self):
        """
        AuthorView: test when password contains three repeating characters in a row
        """
        data = self.data
        data["password"] = "aa26bbb"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_special_character_password(self):
        """
        AuthorView: test when password contains special characters
        """
        data = self.data
        data["password"] = " \"!#$%&'()*+-./:;<=>?@[\]^_`{|}~"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_author_with_lower_case_letter_username(self):
        """
        AuthorView: test when username is made of only lower case letters
        """
        data = self.data
        data["username"] = "testme"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_upper_case_letter_username(self):
        """
        AuthorView: test when username is made of only upper case letters
        """
        data = self.data
        data["username"] = "TESTME"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_author_with_numeric_username(self):
        """
        AuthorView: test when username is made of only numeric characters
        """
        data = self.data
        data["username"] = "0123456789"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_author_with_allowed_special_characters_username(self):
        """
        AuthorView: test when username is made of only allowed special characters
        """
        data = self.data
        data["username"] = "testme01@-.+_"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_invalid_special_characters_username(self):
        """
        AuthorView: test when username is made of only special characters
        """
        data = self.data
        data["username"] = " \"!#$%&'()*/:;<=>?[\]^`{|}~"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_author_with_same_username_and_password(self):
        # ! HEADS UP !
        data = self.data
        data["password"] = "testme01"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_author_with_shorter_length_username(self):
        """
        AuthorView: test when username length is smaller than 6 (minimum standard)
        """
        data = self.data
        data["username"] = "test"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)