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

user = "pyapi-gitlab"
password = "pyapi-gitlab"
host = "http://gitlab.garciaperez.net/"
key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDlH8WnTTdkK/dHA" \
      "hxma4zlw0t8OHEqeAcLFPg4uYMGEZK8K/m0O4zj4mXU5iFgabQKWz" \
      "ax8J42/7ht45kv/pajRH4kmuFag7tqcvVa2sshZ8SaVs1TbEiUJwU4" \
      "hQsDG1WSIaZAEi45PSxIvFu1ev+TDjFHqyrWhQ8CQOIo1ECMJ6WFTd" \
      "Ot/MfOPRT+2Wq0KCBz9a1EzZk0v0U9n2ee2mpiJPweOh8X0wkc/Wmst" \
      "IQ4+rJYNI39wsvcwdztiOvQuAgI35L2EfSAkmUyel2+K1U0WP6bDDbyE" \
      "+3Bexaw1sT6RgQaAI4qAyorWt2LN+/ah3gXCLqwzLsWU5TQlb6YEGkH" \
      " itxaka@MacBook-Air-de-Itxaka.local"

git = gitlab.Gitlab(host=host, user=user)


class GitlabTest(unittest.TestCase):
    def test_login(self):
        """
        Test to see if login works with proper credentials
        """
        self.assertTrue(git.login(user=user, password=password))

    def test_badlogin(self):
        """
        Test to see if login fails with no credentials
        """
        self.assertFalse(git.login("", ""))

    def test_getusers(self):
        git.login(user=user, password=password)
        # get all users
        assert isinstance(git.getusers(), list)  # compatible with 2.6
        self.assertTrue(git.getusers())
        # get X pages
        assert isinstance(git.getusers(page=2), list)  # compatible with 2.6
        assert isinstance(git.getusers(per_page=4), list)  # compatible with 2.6
        self.assertEqual(git.getusers(page=800), list(""))  # check against empty list
        self.assertTrue(git.getusers(per_page=43))  # check against false

    def test_currentuser(self):
        git.login(user=user, password=password)
        assert isinstance(git.currentuser(), dict)  # compatible with 2.6
        self.assertTrue(git.currentuser())

    def test_addremoveusers(self):
        git.login(user=user, password=password)
        newuser = git.createuser("Test", "test", "123456",
                                 "test@test.com", "skype",
                                 "linkedin", "twitter", "25",
                                 bio="bio")
        assert isinstance(newuser, dict)
        # this below doesn't really matter. Gilab always answers a 404
        #self.assertTrue(git.edituser(newuser['id'], twitter="tweeeeet", skype="Microsoft", username="Changed"))
        self.assertTrue(git.deleteuser(newuser['id']))

    def test_sshkeys(self):
        git.login(user=user, password=password)
        git.addsshkey(title="testkey", key=key)
        assert isinstance(git.getsshkeys(), list)  # compatible with 2.6
        # pass the id of the first key
        assert isinstance(git.getsshkey(id_=git.getsshkeys()[0]['id']), dict)  # compatible with 2.6
        self.assertTrue(git.getsshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.addsshkey(title="test key", key=key))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.addsshkeyuser(id_=git.currentuser()['id'], title="testkey", key=key))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))

    def test_project(self):
        git.login(user=user, password=password)
        # we won't test the creation of the project as there is no way of deleting it trougth the api
        # so we would end with a million test projects. Next Gitlab version allows to delete projects
        #self.assertTrue(git.createproject("Test-pyapy-gitlab"))
        assert isinstance(git.getprojects(), list)
        assert isinstance(git.getprojects(page=5), list)
        assert isinstance(git.getprojects(per_page=7), list)
        assert isinstance(git.getproject(git.getprojects()[0]['id']), dict)
        self.assertFalse(git.getproject("wrong"))
        assert isinstance(git.getprojectevents(git.getprojects()[0]['id']), list)
        assert isinstance(git.getprojectevents(git.getprojects()[0]['id'], page=3), list)
        assert isinstance(git.getprojectevents(git.getprojects()[0]['id'], per_page=4), list)
        self.assertTrue(git.addprojectmember(id_=2, user_id=3, access_level="reporter", sudo=1))
        assert isinstance(git.listprojectmembers(id_=2), list)
        self.assertTrue(git.editprojectmember(id_=2, user_id=3, access_level="master", sudo=2))
        self.assertTrue(git.deleteprojectmember(id_=2, user_id=3))
        self.assertTrue(git.addprojecthook(id_=2, url="http://test.com"))
        assert isinstance(git.getprojecthooks(id_=2), list)
        assert isinstance(git.getprojecthook(id_=2, hook_id=git.getprojecthooks(id_=2)[0]['id']), dict)
        self.assertTrue(git.editprojecthook(id_=2, hook_id=git.getprojecthooks(id_=2)[0]['id'], url="http://anothest.com"))
        self.assertTrue(git.deleteprojecthook(id_=2, hook_id=git.getprojecthooks(id_=2)[0]['id']))

    def test_branch(self):
        git.login(user=user, password=password)
        assert isinstance(git.listbranches(id_=2), list)
        assert isinstance(git.listbranch(id_=2,branch="master"), dict)
        self.assertTrue(git.protectbranch(id_=2, branch="master"))
        self.assertTrue(git.unprotectbranch(id_=2, branch="master"))

    def test_deploykeys(self):
        git.login(user=user, password=password)
        self.assertTrue(git.adddeploykey(id_=2, title="test", key=key))
        assert isinstance(git.listdeploykey(id_=2, key_id=110), dict)
        assert isinstance(git.listdeploykeys(id_=2), list)
