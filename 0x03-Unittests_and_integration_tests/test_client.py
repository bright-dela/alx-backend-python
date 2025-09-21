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

# Import the TEST_PAYLOAD directly instead of the whole fixtures module
TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/google/repos"},
        [
            {
                "id": 7697149,
                "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                "name": "episodes.dart",
                "full_name": "google/episodes.dart",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004,
                    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/1342004?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/google",
                    "html_url": "https://github.com/google",
                    "followers_url": "https://api.github.com/users/google/followers",
                    "following_url": "https://api.github.com/users/google/following{/other_user}",
                    "gists_url": "https://api.github.com/users/google/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/google/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/google/subscriptions",
                    "organizations_url": "https://api.github.com/users/google/orgs",
                    "repos_url": "https://api.github.com/users/google/repos",
                    "events_url": "https://api.github.com/users/google/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/google/received_events",
                    "type": "Organization",
                    "site_admin": False
                },
                "html_url": "https://github.com/google/episodes.dart",
                "description": "A framework for timing performance of web apps.",
                "fork": False,
                "url": "https://api.github.com/repos/google/episodes.dart",
                "forks_url": "https://api.github.com/repos/google/episodes.dart/forks",
                "keys_url": "https://api.github.com/repos/google/episodes.dart/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/google/episodes.dart/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/google/episodes.dart/teams",
                "hooks_url": "https://api.github.com/repos/google/episodes.dart/hooks",
                "issue_events_url": "https://api.github.com/repos/google/episodes.dart/issues/events{/number}",
                "events_url": "https://api.github.com/repos/google/episodes.dart/events",
                "assignees_url": "https://api.github.com/repos/google/episodes.dart/assignees{/user}",
                "branches_url": "https://api.github.com/repos/google/episodes.dart/branches{/branch}",
                "tags_url": "https://api.github.com/repos/google/episodes.dart/tags",
                "blobs_url": "https://api.github.com/repos/google/episodes.dart/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/google/episodes.dart/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/google/episodes.dart/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/google/episodes.dart/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/google/episodes.dart/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/google/episodes.dart/languages",
                "stargazers_url": "https://api.github.com/repos/google/episodes.dart/stargazers",
                "contributors_url": "https://api.github.com/repos/google/episodes.dart/contributors",
                "subscribers_url": "https://api.github.com/repos/google/episodes.dart/subscribers",
                "subscription_url": "https://api.github.com/repos/google/episodes.dart/subscription",
                "commits_url": "https://api.github.com/repos/google/episodes.dart/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/google/episodes.dart/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/google/episodes.dart/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/google/episodes.dart/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/google/episodes.dart/contents/{+path}",
                "compare_url": "https://api.github.com/repos/google/episodes.dart/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/google/episodes.dart/merges",
                "archive_url": "https://api.github.com/repos/google/episodes.dart/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/google/episodes.dart/downloads",
                "issues_url": "https://api.github.com/repos/google/episodes.dart/issues{/number}",
                "pulls_url": "https://api.github.com/repos/google/episodes.dart/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/google/episodes.dart/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/google/episodes.dart/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/google/episodes.dart/labels{/name}",
                "releases_url": "https://api.github.com/repos/google/episodes.dart/releases{/id}",
                "deployments_url": "https://api.github.com/repos/google/episodes.dart/deployments",
                "created_at": "2013-01-19T00:31:37Z",
                "updated_at": "2019-09-23T11:53:58Z",
                "pushed_at": "2014-10-09T21:39:33Z",
                "git_url": "git://github.com/google/episodes.dart.git",
                "ssh_url": "git@github.com:google/episodes.dart.git",
                "clone_url": "https://github.com/google/episodes.dart.git",
                "svn_url": "https://github.com/google/episodes.dart",
                "homepage": None,
                "size": 191,
                "stargazers_count": 12,
                "watchers_count": 12,
                "language": "Dart",
                "has_issues": True,
                "has_projects": True,
                "has_downloads": True,
                "has_wiki": True,
                "has_pages": False,
                "forks_count": 22,
                "mirror_url": None,
                "archived": False,
                "disabled": False,
                "open_issues_count": 0,
                "license": {
                    "key": "bsd-3-clause",
                    "name": "BSD 3-Clause \"New\" or \"Revised\" License",
                    "spdx_id": "BSD-3-Clause",
                    "url": "https://api.github.com/licenses/bsd-3-clause",
                    "node_id": "MDc6TGlc2Vuc2U1"
                },
                "forks": 22,
                "open_issues": 0,
                "watchers": 12,
                "default_branch": "master"
            }
        ],
        ['episodes.dart'],
        ['episodes.dart']
    )
]


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
        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos without license filter"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
