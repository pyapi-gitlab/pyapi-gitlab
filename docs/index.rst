.. python-gitlab documentation master file, created by
   sphinx-quickstart on Sun Aug 04 20:46:27 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-gitlab's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Examples
==================

::
   import gitlab
   git = gitlab.Gitlab("gitlab", token="")
   git.login("", "")


   git.createUser("name", "username", "password", "email")
   git.deleteUser(7)
   print git.getUsers()
   print git.currentUser()


   print git.getSshKey(3)
   for key in git.getSshKeys():
       print key

   git.addSshKey("nesdfw key", "")
   addSshKeyUser()
   git.deleteSshKey()

   project = git.getProjects()
   for proj in project:
       print proj
       readme = git.getReadme(proj['web_url'])
       print readme

   git.getProject(2)
   git.getProjectEvents()
   git.createProject("test project number 1")
   git.listProjectMembers(3)
   git.addProjectMember(3, 6, "developer")
   git.deleteProjectMember(3, 5)

   git.getProjectHooks(1)
   git.getProjectHook(1,2)
   git.addProjectHook(1,"http://google.es")
   git.deleteProjectHook(1,7)

   git.listBranches(1)
   git.listBranch(1, "master")
   git.protectBranch(1, "master")
   git.unprotectBranch(1, "master")

   git.createForkRelation(1, 3)
   git.removeForkRelation(1)

   get.getIssues()
   git.getProjectIssues(1)
   git.getProjectIssue(1,1)
   git.createIssue(1, "pedsdfdwsdne")
   git.editIssue(1,1, title="Changing title")

   git.getMilestones(1)
   git.getMilestone(1,1)
   git.createMilestone(1,"New milestone")
   git.editMilestone(1,1,title="Change milestone title")
