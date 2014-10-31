"""
pyapi-gitlab tests
Covered:
Ssh keys
login
user
deploy keys
some list cases
"""

import unittest
import gitlab
import os
import time
import random
import string


user = os.environ.get('gitlab_user', 'root')
password = os.environ.get('gitlab_password', '5iveL!fe')
host = os.environ.get('gitlab_host', 'http://localhost:8080')

key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/" \
      "CdSKHzpkHWp6Bro20GtqTi7h+6+RRTwMatfPqKfuD" \
      "+lqMTzThs9DZWV5ys892UUoKM55xAEpNkan2Xp6Gj" \
      "+p+1vqdFkRGfItJUAlxOeW+3kPD83AIJ/F+uxyAZ5E" \
      "Rd9cdyBFr2efMDbgxOJKj4VmyXpO2UOsvil1wP4+CE" \
      "PxS95LgMqBAUOi7ypukQb3vr7R+MJ7G+vOpwZev8Wb" \
      "Q6aB9Hywu8GbUQk91pdkbvWOcJS783nI9TpZZm7m4O" \
      "NeLwd2XVpY7yBD7v1tL96i1CQRYaN/RosjxZU2ncHA" \
      "8DBC91BNsl9Gcztg6UGteuIClqfzvetwlB66KlL71Z" \
      "HZPmmV pyapi-gitlab@local.host"


class GitlabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.git = gitlab.Gitlab(host=host)
        cls.git.login(user=user, password=password)
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        cls.project = cls.git.createproject(name=name, visibility_level="private",
                                            import_url="https://github.com/Itxaka/pyapi-gitlab.git")
        # wait a bit for the project to be fully imported
        time.sleep(30)
        cls.project_id = cls.project['id']
        cls.user_id = cls.git.currentuser()['id']

    @classmethod
    def tearDownClass(cls):
        cls.git.deleteproject(cls.project_id)

    def test_user(self):
        assert isinstance(self.git.createuser(name="test", username="test",
                                              password="test1234", email="test@test.com",
                                              skype="this", linkedin="that"), dict)
        # get all users
        assert isinstance(self.git.getusers(), list)  # compatible with 2.6
        assert isinstance(self.git.currentuser(), dict)
        user = self.git.getusers(search="test")[0]
        self.assertTrue(self.git.deleteuser(user["id"]))
        # get X pages
        assert isinstance(self.git.getusers(page=2), list)  # compatible with 2.6
        assert isinstance(self.git.getusers(per_page=4), list)  # compatible with 2.6
        self.assertEqual(self.git.getusers(page=800), list(""))  # check against empty list
        self.assertTrue(self.git.getusers(per_page=43))  # check against false


    def test_project(self):
        # test project
        assert isinstance(self.git.getprojects(), list)
        assert isinstance(self.git.getprojects(page=5), list)
        assert isinstance(self.git.getprojects(per_page=7), list)
        assert isinstance(self.git.getproject(self.project_id), dict)
        self.assertFalse(self.git.getproject("wrong"))

        # test events
        assert isinstance(self.git.getprojectevents(self.project_id), list)
        assert isinstance(self.git.getprojectevents(self.project_id, page=3), list)
        assert isinstance(self.git.getprojectevents(self.project_id, per_page=4), list)

        # add-remove project members
        self.assertTrue(self.git.addprojectmember(id_=self.project_id, user_id=self.user_id, access_level="reporter", sudo=1))
        assert isinstance(self.git.listprojectmembers(id_=self.project_id), list)
        self.assertTrue(self.git.editprojectmember(id_=self.project_id, user_id=self.user_id, access_level="master", sudo=1))
        self.assertTrue(self.git.deleteprojectmember(id_=self.project_id, user_id=1))

        # Hooks testing
        self.assertTrue(self.git.addprojecthook(self.project_id, "http://web.com"))
        assert isinstance(self.git.getprojecthooks(self.project_id), list)
        assert isinstance(self.git.getprojecthook(self.project_id,
                                                  self.git.getprojecthooks(self.project_id)[0]['id']), dict)
        self.assertTrue(self.git.editprojecthook(self.project_id,
                                                 self.git.getprojecthooks(self.project_id)[0]['id'], "http://another.com"))
        self.assertTrue(self.git.deleteprojecthook(self.project_id,
                                                   self.git.getprojecthooks(self.project_id)[0]['id']))

    def test_branch(self):
        sha1 = self.git.listrepositorycommits(project_id=self.project_id)[0]["id"]
        self.assertTrue(self.git.createbranch(id_=self.project_id, branch="deleteme", ref=sha1))
        self.assertTrue(self.git.deletebranch(id_=self.project_id, branch="deleteme"))
        assert isinstance(self.git.listbranches(id_=self.project_id), list)
        assert isinstance(self.git.listbranch(id_=self.project_id, branch="develop"), dict)
        self.assertTrue(self.git.protectbranch(id_=self.project_id, branch="develop"))
        self.assertTrue(self.git.unprotectbranch(id_=self.project_id, branch="develop"))

    # def test_deploykeys(self):
    #     self.assertTrue(self.git.adddeploykey(id_=self.project_id, title="Pyapi-gitlab", key=key))
    #     assert isinstance(self.git.listdeploykey(id_=self.project_id, key_id=110), dict)
    #     assert isinstance(self.git.listdeploykeys(id_=self.project_id), list)
    #
    def test_snippets(self):
        self.assertTrue(self.git.createsnippet(self.project_id, "test", "test", "codeee"))
        assert isinstance(self.git.getsnippets(self.project_id), list)
        snippet = self.git.getsnippets(self.project_id)[0]
        assert isinstance(self.git.getsnippet(self.project_id, snippet["id"]), dict)
        self.assertTrue(self.git.deletesnippet(self.project_id, snippet["id"]))

    def test_repositories(self):
        assert isinstance(self.git.getrepositories(self.project_id), list)
        assert isinstance(self.git.getrepositorybranch(self.project_id, "develop"), dict)
        assert isinstance(self.git.protectrepositorybranch(self.project_id, "develop"), dict)
        assert isinstance(self.git.unprotectrepositorybranch(self.project_id, "develop"), dict)
        assert isinstance(self.git.listrepositorytags(self.project_id), list)
        assert isinstance(self.git.listrepositorycommits(self.project_id), list)
        assert isinstance(self.git.listrepositorycommits(self.project_id, page=1), list)
        assert isinstance(self.git.listrepositorycommits(self.project_id, per_page=7), list)
        commit = self.git.listrepositorycommits(self.project_id)[0]
        assert isinstance(self.git.listrepositorycommit(self.project_id, commit["id"]), dict)
        assert isinstance(self.git.listrepositorycommitdiff(self.project_id, commit["id"]), list)
        assert isinstance(self.git.listrepositorytree(self.project_id), list)
        assert isinstance(self.git.listrepositorytree(self.project_id, path="docs"), list)
        assert isinstance(self.git.listrepositorytree(self.project_id, ref_name="develop"), list)
        assert isinstance(str(self.git.getrawblob(self.project_id, commit['id'], "setup.py")), str)
    #
    # def test_search(self):
    #     assert isinstance(self.git.searchproject("gitlab"), list)
    #
    # def test_filearchive(self):
    #     # test it works
    #     self.assertTrue(self.git.getfilearchive(2))
    #     # test for failure
    #     self.failUnlessRaises(gitlab.exceptions.HttpError, self.git.getfilearchive, 999999)
    #
    def test_group(self):
        self.assertTrue(self.git.creategroup("test_group", "test_group"))
        assert isinstance(self.git.getgroups(), list)
        self.assertTrue(self.git.deletegroup(group_id=self.git.getgroups()[0]["id"]))
