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
host = "http://gitlab.garciaperez.net/"
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
        self.git = gitlab.Gitlab(host=host)

    def test_login(self):
        """
        Test to see if login works with proper credentials
        """
        self.assertTrue(self.git.login(user=user, password=password))

    def test_badlogin(self):
        """
        Test to see if login fails with no credentials
        """
        self.assertFalse(self.git.login("", ""))

    def test_getusers(self):
        self.git.login(user=user, password=password)
        # get all users
        assert isinstance(self.git.getusers(), list)  # compatible with 2.6
        self.assertTrue(self.git.getusers())
        # get X pages
        assert isinstance(self.git.getusers(page=2), list)  # compatible with 2.6
        assert isinstance(self.git.getusers(per_page=4), list)  # compatible with 2.6
        self.assertEqual(self.git.getusers(page=800), list(""))  # check against empty list
        self.assertTrue(self.git.getusers(per_page=43))  # check against false

    def test_currentuser(self):
        self.git.login(user=user, password=password)
        assert isinstance(self.git.currentuser(), dict)  # compatible with 2.6
        self.assertTrue(self.git.currentuser())

    def test_addremoveusers(self):
        self.git.login(user=user, password=password)
        newuser = self.git.createuser("Test", "test", "123456",
                                      "test@test.com", "skype",
                                      "linkedin", "twitter", "25",
                                      bio="bio")
        assert isinstance(newuser, dict)
        # this below doesn't really matter. Gilab always answers a 404
        #self.assertTrue(self.git.edituser(newuser['id'], twitter="tweeeeet", skype="Microsoft", username="Changed"))
        self.assertTrue(self.git.deleteuser(newuser['id']))

#    def test_sshkeys(self):
#        self.git.login(user=user, password=password)
#        self.git.addsshkey(title="testkey", key=key)
#        assert isinstance(self.git.getsshkeys(), list)  # compatible with 2.6
        # pass the id of the first key
#        assert isinstance(self.git.getsshkey(id_=self.git.getsshkeys()[0]['id']), dict)  # compatible with 2.6
#        self.assertTrue(self.git.getsshkey(id_=self.git.getsshkeys()[0]['id']))
#        self.assertTrue(self.git.deletesshkey(id_=self.git.getsshkeys()[0]['id']))
#        self.assertTrue(self.git.addsshkey(title="test key", key=key))
#        self.assertTrue(self.git.deletesshkey(id_=self.git.getsshkeys()[0]['id']))
#        self.assertTrue(self.git.addsshkeyuser(id_=self.git.currentuser()['id'], title="testkey", key=key))
#        self.assertTrue(self.git.deletesshkey(id_=self.git.getsshkeys()[0]['id']))

    def test_project(self):
        self.git.login(user=user, password=password)
        # we won't test the creation of the project as there is no way of deleting it trougth the api
        # so we would end with a million test projects. Next Gitlab version allows to delete projects
        #self.assertTrue(self.git.createproject("Test-pyapy-gitlab"))
        assert isinstance(self.git.getprojects(), list)
        assert isinstance(self.git.getprojects(page=5), list)
        assert isinstance(self.git.getprojects(per_page=7), list)
        assert isinstance(self.git.getproject(self.git.getprojects()[0]['id']), dict)
        self.assertFalse(self.git.getproject("wrong"))
        assert isinstance(self.git.getprojectevents(self.git.getprojects()[0]['id']), list)
        assert isinstance(self.git.getprojectevents(self.git.getprojects()[0]['id'], page=3), list)
        assert isinstance(self.git.getprojectevents(self.git.getprojects()[0]['id'], per_page=4), list)
        self.assertTrue(self.git.addprojectmember(id_=2, user_id=3, access_level="reporter", sudo=1))
        assert isinstance(self.git.listprojectmembers(id_=2), list)
        self.assertTrue(self.git.editprojectmember(id_=2, user_id=3, access_level="master", sudo=2))
        self.assertTrue(self.git.deleteprojectmember(id_=2, user_id=3))
        self.assertTrue(self.git.addprojecthook(id_=2, url="http://test.com"))
        assert isinstance(self.git.getprojecthooks(id_=2), list)
        assert isinstance(self.git.getprojecthook(id_=2, hook_id=self.git.getprojecthooks(id_=2)[0]['id']), dict)
        self.assertTrue(self.git.editprojecthook(id_=2, hook_id=self.git.getprojecthooks(id_=2)[0]['id'],
                                                 url="http://anothest.com"))
        self.assertTrue(self.git.deleteprojecthook(id_=2, hook_id=self.git.getprojecthooks(id_=2)[0]['id']))

    def test_branch(self):
        self.git.login(user=user, password=password)
        assert isinstance(self.git.listbranches(id_=2), list)
        assert isinstance(self.git.listbranch(id_=2, branch="master"), dict)
        self.assertTrue(self.git.protectbranch(id_=2, branch="master"))
        self.assertTrue(self.git.unprotectbranch(id_=2, branch="master"))

    def test_deploykeys(self):
        self.git.login(user=user, password=password)
        self.assertTrue(self.git.adddeploykey(id_=2, title="test", key=key))
        assert isinstance(self.git.listdeploykey(id_=2, key_id=110), dict)
        assert isinstance(self.git.listdeploykeys(id_=2), list)

    def test_snippets(self):
        self.git.login(user=user, password=password)
        self.assertTrue(self.git.createsnippet(1, "test", "test", "codeee"))
        assert isinstance(self.git.getsnippets(1), list)
        assert isinstance(self.git.getsnippet(1, self.git.getsnippets(1)[0]['id']), dict)
        self.assertTrue(self.git.deletesnippet(1, self.git.getsnippets(1)[0]['id']))

    def test_repositories(self):
        self.git.login(user=user, password=password)
        assert isinstance(self.git.getrepositories(2), list)
        assert isinstance(self.git.getrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.protectrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.unprotectrepositorybranch(2, "master"), dict)
        assert isinstance(self.git.listrepositorytags(2), list)
        assert isinstance(self.git.listrepositorycommits(2), list)
        assert isinstance(self.git.listrepositorycommit(2, self.git.listrepositorycommits(2)[0]['id']), dict)
        assert isinstance(self.git.listrepositorycommitdiff(2, self.git.listrepositorycommits(2)[0]['id']), dict)
        assert isinstance(self.git.listrepositorytree(2), list)
        assert isinstance(self.git.listrepositorytree(2, path="docs"), list)
        assert isinstance(self.git.listrepositorytree(2, ref_name="master"), list)
        assert isinstance(str(self.git.getrawblob(2, self.git.listrepositorycommits(2)[0]['id'], "setup.py")), str)