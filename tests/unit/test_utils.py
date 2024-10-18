import unittest
import bcrypt
import jwt
from datetime import datetime, timedelta

from core.utils import utils
from config.settings import settings

class TestUtils(unittest.TestCase):

    def test_generate_token(self):
        """
        Tests the generate_token function, verifying that it produces a valid JWT token.
        """
        user_id = 123
        token = utils.generate_token(user_id)
        self.assertIsNotNone(token)
        self.assertNotEqual(token, "")

        # Verify token structure and payload
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded_token["user_id"], user_id)
        self.assertGreater(decoded_token["exp"], datetime.utcnow())

    def test_verify_token(self):
        """
        Tests the verify_token function, verifying token validation and handling expired tokens.
        """
        user_id = 456
        # Generate a valid token
        token = utils.generate_token(user_id)
        payload = utils.verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["user_id"], user_id)

        # Generate an expired token
        expired_token = jwt.encode({"user_id": 789, "exp": datetime.utcnow() - timedelta(minutes=1)}, settings.JWT_SECRET, algorithm="HS256").decode("utf-8")
        payload = utils.verify_token(expired_token)
        self.assertIsNone(payload)

    def test_hash_password(self):
        """
        Tests the hash_password function, verifying that it generates a bcrypt hash.
        """
        password = "testpassword"
        hashed_password = utils.hash_password(password)
        self.assertIsNotNone(hashed_password)
        self.assertNotEqual(hashed_password, password)

    def test_check_password(self):
        """
        Tests the check_password function, verifying that it correctly compares a password against a bcrypt hash.
        """
        password = "testpassword"
        hashed_password = utils.hash_password(password)

        # Correct password
        self.assertTrue(utils.check_password(password, hashed_password))

        # Incorrect password
        self.assertFalse(utils.check_password("wrongpassword", hashed_password))

    def test_cache_response(self):
        """
        Tests the cache_response function, simulating Redis caching behavior.
        """
        query_id = "12345"
        response = "This is a test response"
        utils.cache_response(query_id, response)

        # Mock retrieval from Redis
        self.assertEqual(utils.get_cached_response(query_id), response)

    def test_get_cached_response(self):
        """
        Tests the get_cached_response function, simulating Redis retrieval.
        """
        query_id = "67890"
        # Mock Redis data
        utils.cache_response(query_id, "Cached response")

        cached_response = utils.get_cached_response(query_id)
        self.assertEqual(cached_response, "Cached response")

        # Missing cache
        non_existent_query_id = "11111"
        cached_response = utils.get_cached_response(non_existent_query_id)
        self.assertIsNone(cached_response)


if __name__ == "__main__":
    unittest.main()