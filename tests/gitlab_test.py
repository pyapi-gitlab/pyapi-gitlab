import unittest
import gitlab

user = "pyapi-gitlab"
password = "pyapi-gitlab"
host = "http://gitlab.garciaperez.net/"
key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD0WZg/LJenhWSm1toLLhMVplLd4tUthdEc7G2MafER91gLqZaGVfp2FcohDR9I7hU+9g52RtyoGzNbeLF1L7jVULe/OG1Ta8snxqpZ8Lgdgj2SYCsHjAebSozHzoxxz/TIBvZix4yMervMESLH1uBzkmdw1cT4LCFsrd+n/uhX6uMwjVggu1m+VPJfq2CE+mzbE/kUWua+h7F7Kf5+sNeTio26thUjxDx/10W3e119EeNO3JObi/dvmKGZ5IlSPfbnZ+Q0IKe6VwmHwRfc649MW9JZJJjgRISxUgN70g0TsfAF7+Yv8QketOSXfv0mwtixiUQXuf+TDGm6ilOufHhP network@base"
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
        git.addsshkey(title="test key", key=key)
        assert isinstance(git.getsshkeys(), list)  # compatible with 2.6
        # pass the id of the first key
        assert isinstance(git.getsshkey(id_=git.getsshkeys()[0]['id']), dict)  # compatible with 2.6
        self.assertTrue(git.getsshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.addsshkey(title="test key", key=key))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.addsshkeyuser(id_=git.currentuser()['id'], title="tests key", key=key))
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
