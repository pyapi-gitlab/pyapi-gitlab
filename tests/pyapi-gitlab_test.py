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


user = os.environ['gitlab_user']
password = os.environ['gitlab_password']

host = os.environ['gitlab_host']
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
    def setUp(self):
        # set up the connection
        self.git = gitlab.Gitlab(host=host)

        # test the failure first
        self.failUnlessRaises(gitlab.exceptions.HttpError, self.git.login, user="caca", password="caca")

        # now test login and leave it set up for the rest of the tests
        self.assertTrue(self.git.login(user, password))

        # create a project to use on the testing
        self.project = self.git.createproject("Pyapi-gitlab")
        self.project_id = self.project['id']
        assert isinstance(self.project, dict)

        # create a user to use in the testing
        self.user = self.git.createuser("caca", "test", "testpass", "test@test.com")
        self.user_id = self.user['id']
        assert isinstance(self.user, dict)

    def tearDown(self):
        # remove projects and users
        self.assertTrue(self.git.deleteuser(self.user_id))
        self.assertTrue(self.git.deleteproject(self.project_id))

    def test_getusers(self):
        # get all users
        assert isinstance(self.git.getusers(), list)  # compatible with 2.6
        self.assertTrue(self.git.getusers())

        # get X pages
        assert isinstance(self.git.getusers(page=2), list)  # compatible with 2.6
        assert isinstance(self.git.getusers(per_page=4), list)  # compatible with 2.6
        self.assertEqual(self.git.getusers(page=800), list(""))  # check against empty list
        self.assertTrue(self.git.getusers(per_page=43))  # check against false

    def test_currentuser(self):
        assert isinstance(self.git.currentuser(), dict)  # compatible with 2.6
        self.assertTrue(self.git.currentuser())

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
        self.assertTrue(self.git.addprojectmember(id_=self.project_id, user_id=1, access_level="reporter", sudo=1))
        assert isinstance(self.git.listprojectmembers(id_=self.project_id), list)
        self.assertTrue(self.git.editprojectmember(id_=self.project_id, user_id=1, access_level="master", sudo=2))
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

        # Delete the created project
        self.assertTrue(self.git.deleteproject(self.project_id))

    def test_branch(self):
        assert isinstance(self.git.listbranches(id_=self.project_id), list)
        assert isinstance(self.git.listbranch(id_=self.project_id, branch="master"), dict)
        self.assertTrue(self.git.protectbranch(id_=self.project_id, branch="master"))
        self.assertTrue(self.git.unprotectbranch(id_=self.project_id, branch="master"))

    def test_deploykeys(self):
        self.assertTrue(self.git.adddeploykey(id_=2, title="test", key=key))
        assert isinstance(self.git.listdeploykey(id_=2, key_id=110), dict)
        assert isinstance(self.git.listdeploykeys(id_=2), list)

    def test_snippets(self):
        self.assertTrue(self.git.createsnippet(1, "test", "test", "codeee"))
        assert isinstance(self.git.getsnippets(1), list)
        assert isinstance(self.git.getsnippet(1, self.git.getsnippets(1)[0]['id']), dict)
        self.assertTrue(self.git.deletesnippet(1, self.git.getsnippets(1)[0]['id']))

    def test_repositories(self):
        assert isinstance(self.git.getrepositories(2), list)
        assert isinstance(self.git.getrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.protectrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.unprotectrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.listrepositorytags(2), list)
        assert isinstance(self.git.listrepositorycommits(2), list)
        assert isinstance(self.git.listrepositorycommits(2, page=1), list)
        assert isinstance(self.git.listrepositorycommits(2, per_page=7), list)
        assert isinstance(self.git.listrepositorycommit(2, self.git.listrepositorycommits(2)[0]['id']), dict)
        assert isinstance(self.git.listrepositorycommitdiff(2, self.git.listrepositorycommits(2)[0]['id']), dict)
        assert isinstance(self.git.listrepositorytree(2), list)
        assert isinstance(self.git.listrepositorytree(2, path="docs"), list)
        assert isinstance(self.git.listrepositorytree(2, ref_name="master"), list)
        assert isinstance(str(self.git.getrawblob(2, self.git.listrepositorycommits(2)[0]['id'], "setup.py")), str)

    def test_search(self):
        assert isinstance(self.git.searchproject("gitlab"), list)

    def test_filearchive(self):
        # test it works
        self.assertTrue(self.git.getfilearchive(2))
        # test for failure
        self.failUnlessRaises(gitlab.exceptions.HttpError, self.git.getfilearchive, 999999)

    def test_group(self):
        self.assertTrue(self.git.creategroup("test_group", "test"))
        assert isinstance(self.git.getgroups(), list)
        print(self.git.getgroups())
        #self.assertTrue(self.git.deletegroup(self.git.getgroups()[:-1]))
