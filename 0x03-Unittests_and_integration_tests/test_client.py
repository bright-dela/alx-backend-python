#!/usr/bin/env python3
"""
Unit tests for the client module.
This module contains test cases for the GithubOrgClient class
and its methods in the client module.
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org returns correct value without making HTTP calls"""
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(url)
        self.assertEqual(result, {"org": org_name})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct value
        based on mocked org
        """
        test_url = "https://api.github.com/orgs/test/repos"
        mock_org.return_value = {"repos_url": test_url}
        client = GithubOrgClient("test")
        result = client._public_repos_url
        self.assertEqual(result, test_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list of repos"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("test")
            result = client.public_repos()
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
            self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean value"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    def test_has_license_missing_key(self):
        """Test has_license handles repos without a license key"""
        repo = {"name": "repo-no-license"}
        result = GithubOrgClient.has_license(repo, "apache-2.0")
        self.assertFalse(result)


# Simplified test payload for integration tests
TEST_PAYLOAD = [(
    {"repos_url": "https://api.github.com/orgs/google/repos"},
    [{"name": "repo1", "license": {"key": "apache-2.0"}},
     {"name": "repo2", "license": {"key": "mit"}}],
    ["repo1", "repo2"],
    ["repo1"]
)]


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class with mocked requests.get"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Create mock responses
        cls.org_response = Mock()
        cls.org_response.json.return_value = cls.org_payload

        cls.repos_response = Mock()
        cls.repos_response.json.return_value = cls.repos_payload

        # Strict side effect based on full URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_response
            elif url == "https://api.github.com/orgs/google/repos":
                return cls.repos_response
            return Mock()

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_integration_public_repos(self):
        """Integration test for public_repos without license filter"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_integration_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
        self.assertEqual(self.mock_get.call_count, 2)


if __name__ == '__main__':
    unittest.main()
