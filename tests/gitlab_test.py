import unittest
import gitlab

user = "test@test.com"
password = "123456"
host = "http://demo.gitlabhq.com"
key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD0WZg/LJenhWSm1toLLhMVplLd4tUthdEc7G2MafER91gLqZaGVfp2FcohDR9I7hU+9g52RtyoGzNbeLF1L7jVULe/OG1Ta8snxqpZ8Lgdgj2SYCsHjAebSozHzoxxz/TIBvZix4yMervMESLH1uBzkmdw1cT4LCFsrd+n/uhX6uMwjVggu1m+VPJfq2CE+mzbE/kUWua+h7F7Kf5+sNeTio26thUjxDx/10W3e119EeNO3JObi/dvmKGZ5IlSPfbnZ+Q0IKe6VwmHwRfc649MW9JZJJjgRISxUgN70g0TsfAF7+Yv8QketOSXfv0mwtixiUQXuf+TDGm6ilOufHhP network@base"
git = gitlab.Gitlab(host=host, user=user)

class GitlabTest(unittest.TestCase):
    def testlogin(self):
        """
        Test to see if login works with proper credentials
        """
        self.assertTrue(git.login(user=user, password=password))

    def testbadlogin(self):
        """
        Test to see if login fails with no credentials
        """
        self.assertFalse(git.login("", ""))

class UsersTest(unittest.TestCase):
    git.login(user=user, password=password)

    def testgetusers(self):
        # get all users
        assert isinstance(git.getusers(), list)  # compatible with 2.6
        self.assertIsNot(git.getusers(), False)
        # get X pages
        assert isinstance(git.getusers(page=2), list)  # compatible with 2.6
        assert isinstance(git.getusers(per_page=4), list)  # compatible with 2.6
        self.assertIsNot(git.getusers(page=7), False)  # check against false
        self.assertIsNot(git.getusers(per_page=43), False)  # check against false

    def testcurrentuser(self):
        assert isinstance(git.currentuser(), dict)  # compatible with 2.6
        self.assertIsNot(git.currentuser(), False)


class SshTest(unittest.TestCase):
    def testsshkeys(self):
        git.addsshkey(title="test key", key=key)
        assert isinstance(git.getsshkeys(), list)  # compatible with 2.6
        self.assertIsNot(git.getsshkeys(), False)
        # pass the id of the first key
        assert isinstance(git.getsshkey(id_=git.getsshkeys()[0]['id']), dict)  # compatible with 2.6
        self.assertIsNot(git.getsshkey(id_=git.getsshkeys()[0]['id']), False)
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        self.assertTrue(git.addsshkey(title="test key", key=key))
        self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
        # on the demo gitlab there is no way to add a key for another user if you are not an admin
        #self.assertTrue(git.addsshkeyuser(id_=git.currentuser()['id'], title="tests key", key=key))
        #self.assertTrue(git.deletesshkey(id_=git.getsshkeys()[0]['id']))
