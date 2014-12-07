.. pyapi-gitlab documentation master file, created by
   sphinx-quickstart on Sun Aug 04 20:46:27 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyapi-gitlab's documentation!
=========================================

pyapi-gitlab is a wrapper to access all the functions of Gitlab from our python scripts.


How to use it
==================

There are several optional parameters in a lot of the commands, you should check the command documentation or the
command string, for example adding an user accepts up to 7 extra parameters.

First we import our library::

   import gitlab

Then we need to authenticate to our Gitlab instance. There is 2 ways of doing this.

Authenticating via user/password
==================================

First create the instance passing the gitlab server as parameter::

   git = gitlab.Gitlab("our_gitlab_host")

Then call the login() method::

   git.login("user", "password")


That's it, now your gitlab instance is using the private token in all the calls. You can see it in the token variable

Authenticating via private_token
====================================

You can also authenticate via the private_token that you can get from your gitlab profile and it's easier than using user/password

Just call the instance with the parameter token::

    git = gitlab.Gitlab("our_gitlab_host", token="mytoken")


Using sudo on the functions
=============================

All API calls support using sudo (e.g. calling the API as a different user)
This is accomplished by using the setsudo() method to temporarily make all requests as another user, then calling it with no args to go back to the original user::


    >>> git = gitlab.Gitlab(host=host)
    >>> git.login(user=user, password=password)
    True
    >>> git.currentuser()["username"]
    u'root'
    >>> [[u["id"], u["username"]] for u in git.getusers()]
    [[1, u'root'], [9, u'sudo_user'], [10, u'NMFUQ85Y']]
    >>> # lets try with sudo_user
    >>> git.setsudo(9)
    >>> git.currentuser()["username"]
    u'sudo_user'
    >>> # lets change back to the original user
    >>> git.setsudo(1)
    >>> git.currentuser()["username"]
    u'root'



Pagination
===========

All get* functions now accept a page and per_page parameter::

    git.getissues(page=1, per_page=40)


The default is to get page 1 and 20 results per page. The max value for per_page is 100.

API doc
==================

Every method now has the documentation as a docstring.
The best way of checking what the API entails is to go to the Gitlab API page directly as this library is a 1:1 translation of it.
http://doc.gitlab.com/ce/api/README.html


.. toctree::

.. automodule:: Gitlab
   :members: