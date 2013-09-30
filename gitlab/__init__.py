# -*- coding: utf-8 -*-
"""
python-gitlab, a gitlab python wrapper for the gitlab API
by Itxaka Serrano Garcia <itxakaserrano@gmail.com>
"""

import requests
import json
import markdown


class Gitlab(object):
    def __init__(self, host, token=""):
        """
        on init we setup the token used for all the api calls and all the urls
        :param host: host of gitlab
        :param user: user
        :param token: token
        """
        if token != "":
            self.token = token
            self.headers = {"PRIVATE-TOKEN": self.token}
        if host[-1] == '/':
            self.host = host[:-1]
        else:
            self.host = host
        self.projects_url = self.host + "/api/v3/projects"
        self.users_url = self.host + "/api/v3/users"
        self.keys_url = self.host + "/api/v3/user/keys"
        self.groups_url = self.host + "/api/v3/groups"

    def login(self, email, password):
        """
        Logs the user in and setups the header with the private token
        :param user: gitlab user
        :param password: gitlab password
        :return: True if login successfull
        """
        data = {"email": email, "password": password}
        request = requests.post(self.host + "/api/v3/session", data=data)
        if request.status_code == 201:
            self.token = json.loads(request.content)['private_token']
            self.headers = {"PRIVATE-TOKEN": self.token}
            return True
        else:
            print request
            return False

    def getusers(self, id_=0, page=1, per_page=20):
        """
        Return a user list
        :param id_: the id of the user to get instead of getting all users,
         return all users if 0
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        return: returs a dictionary of the users, false if there is an error
        """
        params = {'page': page, 'per_page': per_page}
        if id_ != 0:
            request = requests.get(self.host + "/api/v3/users/" + str(id_),
                             params=params, headers=self.headers)
            user = json.loads(request.content)
            return [user['id'], user['username'], user['name'], user['email'],
                    user['state'], user['created_at']]
        else:
            request = requests.get(self.users_url, params=params, headers=self.headers)
            if request.status_code == 200:
                return json.loads(request.content)
            else:
                return False

    def createuser(self, name, username, password, email, skype="", linkedin="",
                   twitter="",
                   projects_limit="", extern_uid="", provider="", bio=""):
        """
        Create a user
        :param name: Obligatory
        :param username: Obligatory
        :param password: Obligatory
        :param email: Obligatory
        :return: TRue if the user was created,false if it wasn't(already exists)
        """
        data = {"name": name, "username": username, "password": password,
                "email": email, "skype": skype,
                "twitter": twitter, "linkedin": linkedin,
                "projects_limit": projects_limit, "extern_uid": extern_uid,
                "provider": provider, "bio": bio}
        request = requests.post(self.users_url, headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        elif request.status_code == 404:
            print request
            return False

    def deleteuser(self, id_):
        """
        Deletes an user by ID
        :param id_: id of the user to delete
        :return: True if it deleted, False if it couldn't. False could happen
        for several reasons, but there isn't a
        good way of differenting them
        """
        request = requests.delete(self.users_url + "/" + str(id_),
                            headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def currentuser(self):
        """
        Returns the current user parameters. The current user is linked
        to the secret token
        :return: a list with the current user properties
        """
        request = requests.get(self.host + "/api/v3/user",
                         headers=self.headers)
        return json.loads(request.content)

    def edituser(self, id_, name="", username="", password="", email="",
                 skype="", linkedin="", twitter="",
                 projects_limit="", extern_uid="", provider="", bio=""):
        """
        Edits an user data. Unfortunately we have to check ALL the params,
        as they can't be empty or the user will get all their data empty,
        so we only send the filled params
        :param id_: id of the user to change
        :param name: name
        :param username: username
        :param password: pass
        :param email: email
        :param skype: skype
        :param linkedin: linkedin
        :param twitter: twitter
        :param projects_limit: the limits project, default is 10
        :param extern_uid: no idea
        :param provider: google login for example
        :param bio: bio
        :param sudo: do the task as the user provided
        :return: alway true as gitlab answers with a 404
        """
        data = {}
        if name != "":
            data["name"] = name
        if username != "":
            data["username"] = username
        if password != "":
            data["password"] = password
        if email != "":
            data["email"] = email
        if skype != "":
            data["skype"] = skype
        if linkedin != "":
            data["linkedin"] = linkedin
        if twitter != "":
            data["twitter"] = twitter
        if projects_limit != "":
            data["projects_limit"] = projects_limit
        if extern_uid != "":
            data["extern_uid"] = extern_uid
        if provider != "":
            data["provider"] = provider
        if bio != "":
            data["bio"] = bio
        request = requests.put(self.users_url + "/" + str(id_),
                               headers=self.headers, data=data)
        if request.status_code == 404:
            return True
        # There is a problem here and that is that the api always return 404,
        #  doesn't matter what heappened with the request,
        # so now way of knowing what happened
        else:
            return False

    def getsshkeys(self):
        """
        Gets all the ssh keys for the current user
        :return: a dictionary with the lists
        """
        request = requests.get(self.keys_url, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getsshkey(self, id_):
        """
        Get a single ssh key identified by id_
        :param id_: the id of the key
        :return: the key itself
        """
        request = requests.get(self.keys_url + "/" + str(id_),
                               headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def addsshkey(self, title, key):
        """
        Add a new ssh key for the current user
        :param title: title of the new key
        :param key: the key itself
        :return: true if added, false if it didn't add it
        (it could be because the name or key already exists)
        """
        data = {"title": title, "key": key}
        request = requests.post(self.keys_url, headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def addsshkeyuser(self, id_, title, key):
        """
        Add a new ssh key for the user identified by id
        :param id_: id of the user to add the key to
        :param title: title of the new key
        :param key: the key itself
        :return: true if added, false if it didn't add it
        (it could be because the name or key already exists)
        """
        data = {"title": title, "key": key}
        request = requests.post(self.keys_url + "/" + str(id_) + "/keys",
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def deletesshkey(self, id_):
        """
        Deletes an sshkey for the current user identified by id
        :param id_: the id of the key
        :return: False if it didn't delete it, True if it was deleted
        """
        request = requests.delete(self.keys_url + "/" + str(id_),
                            headers=self.headers)
        if request.content == "null":
            print request
            return False
        else:
            return True

    def getprojects(self, page=1, per_page=20):
        """
        Returns a dictionary of all the projects
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        :return: list with the repo name, description, last activity,
         web url, ssh url, owner and if its public
        """
        params = {'page': page, 'per_page': per_page}
        request = requests.get(self.projects_url, params=params, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getproject(self, id_):
        """
        Get info for a project identified by id
        :param id_: id of the project
        :return: False if not found, a dictionary if found
        """
        request = requests.get(self.projects_url + "/" + str(id_),
                         headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getprojectevents(self, id_, page=1, per_page=20):
        """
        Get the project identified by id, events(commits)
        :param id_: id of the project
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        :return: False if no project with that id, a dictionary
         with the events if found
        """
        params = {'page': page, 'per_page': per_page}
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/events", params=params, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def createproject(self, name, description="", default_branch="",
                      issues_enabled=0, wall_enabled=0,
                      merge_requests_enabled=0, wiki_enabled=0,
                      snippets_enabled=0, public=0):
        """
        Create a project
        :param name: Obligatory
        :return: Dict of information on the newly created project if successful,
         False otherwise
        """
        data = {"name": name, "description": description,
                "default_branch": default_branch,
                "issues_enabled": issues_enabled, "wall_enabled": wall_enabled,
                "merge_requests_enabled": merge_requests_enabled,
                "wiki_enabled": wiki_enabled,
                "snippets_enabled": snippets_enabled}

        # if gitlab is the new 6th version, there is a public option for the
        # project creation
        if type(public) != int:
            raise TypeError
        if public != 0:
            data['public'] = public
        #request now works with both GitLab 5 and GitLab 6.
        request = requests.post(self.projects_url, headers=self.headers,
                                data=data)
        if request.status_code == 201:
            return json.loads(request.content)
        else:
            print request
            return False

    def createprojectuser(self, id_, name, description="", default_branch="",
                          issues_enabled=0, wall_enabled=0,
                          merge_requests_enabled=0, wiki_enabled=0,
                          snippets_enabled=0):
        """
        Create a project for the given user identified by id
        :param id_: id of the user to crete the project for
        :param name: Obligatory
        :return: True if it created the project, False otherwise
        """
        data = {"name": name, "description": description,
                "default_branch": default_branch,
                "issues_enabled": issues_enabled, "wall_enabled": wall_enabled,
                "merge_requests_enabled": merge_requests_enabled,
                "wiki_enabled": wiki_enabled,
                "snippets_enabled": snippets_enabled}
        request = requests.post(self.projects_url + "/user/" + str(id_),
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def listprojectmembers(self, id_):
        """
        lists the members of a given project id
        :param id_: the project id
        :return: the projects memebers
        """
        request = requests.get(self.projects_url + "/" + str(id_) + "/members",
                         headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def addprojectmember(self, id_, user_id, access_level):
        """
        adds a project member to a project
        :param id_: project id
        :param user_id: user id
        :param access_level: access level, see gitlab help to know more
        :param sudo: do the request with another user
        :return: True if success
        """
        # check the access level and put into a number
        if access_level.lower() == "master":
            access_level = 40
        elif access_level.lower() == "developer":
            access_level = 30
        elif access_level.lower() == "reporter":
            access_level = 20
        else:
            access_level = 10
        data = {"id": id_, "user_id": user_id, "access_level": access_level}
        request = requests.post(self.projects_url + "/" + str(id_) + "/members",
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def editprojectmember(self, id_, user_id, access_level):
        """
        edit a project member
        :param id_: project id
        :param user_id: user id
        :param access_level: access level
        :param sudo: do the request as another user
        :return: True if success
        """
        if access_level.lower() == "master":
            access_level = 40
        elif access_level.lower() == "developer":
            access_level = 30
        elif access_level.lower() == "reporter":
            access_level = 20
        else:
            access_level = 10
        data = {"id": id_, "user_id": user_id, "access_level": access_level}
        request = requests.put(self.projects_url + "/" + str(id_) + "/members/"
                               + str(user_id), headers=self.headers, data=data)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def deleteprojectmember(self, id_, user_id):
        """
        Delete a project member
        :param id_: project id
        :param user_id: user id
        :return: always true
        """
        request = requests.delete(self.projects_url + "/" + str(id_)
                                  + "/members/" + str(user_id),
                                  headers=self.headers)
        if request.status_code == 200:
            return True  # It always returns true

    def getprojecthooks(self, id_):
        """
        get all the hooks from a project
        :param id_: project id
        :return: the hooks
        """
        request = requests.get(self.projects_url + "/" + str(id_) + "/hooks",
                         headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getprojecthook(self, id_, hook_id):
        """
        get a particular hook from a project
        :param id_: project id
        :param hook_id: hook id
        :return: the hook
        """
        request = requests.get(self.projects_url + "/" + str(id_) + "/hooks/" +
                         str(hook_id), headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def addprojecthook(self, id_, url):
        """
        add a hook to a project
        :param id_: project id
        :param url: url of the hook
        :return: True if success
        """
        data = {"id": id_, "url": url}
        request = requests.post(self.projects_url + "/" + str(id_) + "/hooks",
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def editprojecthook(self, id_, hook_id, url):
        """
        edit an existing hook from a project
        :param id_: project id
        :param hook_id: hook id
        :param url: the new url
        :param sudo: do the request as another user
        :return: True if success
        """
        data = {"id": id_, "hook_id": hook_id, "url": url}
        request = requests.put(self.projects_url + "/" + str(id_) + "/hooks/" +
                         str(hook_id), headers=self.headers,
                         data=data)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def deleteprojecthook(self, id_, hook_id):
        """
        delete a project hook
        :param id_: project id
        :param hook_id: hook id
        :return: True if success
        """
        request = requests.delete(self.projects_url + "/" + str(id_)
                                  + "/hooks/"
                                  + str(hook_id), headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def listbranches(self, id_):
        """
        list all the branches from a project
        :param id_: project id
        :return: the branches
        """
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/repository/branches", headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def listbranch(self, id_, branch):
        """
        list one branch from a project
        :param id_: project id
        :param branch: branch id
        :return: the branch
        """
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/repository/branches/" + str(branch),
                         headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def protectbranch(self, id_, branch):
        """
        protect a branch from changes
        :param id_: project id
        :param branch: branch id
        :return: True if success
        """
        request = requests.put(self.projects_url + "/" + str(id_) +
                         "/repository/branches/" + str(branch) + "/protect",
                         headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def unprotectbranch(self, id_, branch):
        """
        stop protecting a branch
        :param id_: project id
        :param branch: branch id
        :return: true if success
        """
        request = requests.put(self.projects_url + "/" + str(id_) +
                         "/repository/branches/" + str(branch) + "/unprotect",
                         headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def createforkrelation(self, id_, from_):
        """
        create a fork relation. This DO NOT create a fork but only adds
        the relation between 2 repositories
        :param id_: project id
        :param from_: from id
        :return: true if success
        """
        data = {"id": id_, "forked_from_id": from_}
        request = requests.post(self.projects_url + "/" + str(id_) +
                          "/fork/" + str(from_), headers=self.headers,
                          data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def removeforkrelation(self, id_):
        """
        remove an existing fork relation. this DO NOT remove the fork,
        only the relation between them
        :param id_: project id
        :return: true if success
        """
        request = requests.delete(self.projects_url + "/" + str(id_) +
                            "/fork", headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def getissues(self, page=1, per_page=20):
        """
        Return a global list of issues for your user.
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        """
        params = {'page': page, 'per_page': per_page}
        request = requests.get(self.host + "/api/v3/issues",
                               params=params, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getprojectissues(self, id_, page=1, per_page=20):
        """
        Return a list of issues for project id_.
        :param id_: The id for the project.
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        """
        params = {'page': page, 'per_page': per_page}
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/issues", params=params, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getprojectissue(self, id_, issue_id):
        """
        Return a list of issues for project id_.
        :param id_: The id for the project.
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        """
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/issues/" + str(issue_id), headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def createissue(self, id_, title, description="", assignee_id="",
                    milestone_id="", labels=""):
        """
        create a new issue
        :param id_: project id
        :param title: title of the issue
        :param description: description
        :param assignee_id: assignee for the issue
        :param milestone_id: milestone
        :param labels: label
        :param sudo: do the request as another user
        :return: true if success
        """
        data = {"id": id, "title": title, "description": description,
                "assignee_id": assignee_id,
                "milestone_id": milestone_id, "labels": labels}
        request = requests.post(self.projects_url + "/" + str(id_) + "/issues",
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def editissue(self, id_, issue_id, title="", description="",
                  assignee_id="", milestone_id="", labels="",
                  state_event=""):
        """
        edit an existing issue data
        :param id_: project id
        :param issue_id: issue id
        :param title: title
        :param description: description
        :param assignee_id: asignee
        :param milestone_id: milestone
        :param labels: label
        :param state_event: state
        :param sudo: do the request as another user
        :return: true if success
        """
        data = {"id": id, "issue_id": issue_id, "title": title,
                "description": description, "assignee_id": assignee_id,
                "milestone_id": milestone_id, "labels": labels,
                "state_event": state_event}
        request = requests.put(self.projects_url + "/" + str(id_) + "/issues/" +
                         str(issue_id), headers=self.headers,
                         data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def getmilestones(self, id_):
        """
        get the milestones for a project
        :param id_: project id
        :return: the milestones
        """
        request = requests.get(self.projects_url + "/" + str(id_) +
                         "/milestones", headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getmilestone(self, id_, milestone_id):
        """
        get an specific milestone
        :param id_: project id
        :param milestone_id: milestone id
        :return: the milestone
        """
        request = requests.get(self.projects_url + "/" + str(id_)
                               + "/milestones/"
                               + str(milestone_id), headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def createmilestone(self, id_, title, description="", due_date=""):
        """
        create a new milestone
        :param id_: project id
        :param title: title
        :param description: description
        :param due_date: due date
        :param sudo: do the request as another user
        :return: true if success
        """
        data = {"id": id_, "title": title, "description": description,
                "due_date": due_date}
        request = requests.post(self.projects_url + "/" + str(id_) +
                          "/milestones", headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def editmilestone(self, id_, milestone_id, title="", description="",
                      due_date="", state_event=""):
        """
        edit an existing milestone
        :param id_: project id
        :param milestone_id: milestone id
        :param title: title
        :param description: description
        :param due_date: due date
        :param state_event: state
        :param sudo: do the request as another user
        :return: true if success
        """
        data = {"id": id_, "milestone_id": milestone_id, "title": title,
                "description": description,
                "due_date": due_date, "state_event": state_event}
        request = requests.put(self.projects_url + "/" + str(id_)
                               + "/milestones/"
                               + str(milestone_id), headers=self.headers,
                         data=data)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def listdeploykeys(self, id_):
        """
        Get a list of a project's deploy keys.
        :param id_: project id
        :return: the keys in a dictionary if success, false if not
        """
        request = requests.get(self.projects_url + "/" + str(id_) + "/keys",
                         headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def listdeploykey(self, id_, key_id):
        """
        Get a single key.
        :param id_: project id
        :param key_id: key id
        :return: the key in a dict if success, false if not
        """
        request = requests.get(self.projects_url + "/" + str(id_) + "/keys/" +
                         str(key_id), headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def adddeploykey(self, id_, title, key):
        """
        Creates a new deploy key for a project.
        If deploy key already exists in another project - it will be joined
        to project but only if original one was is accessible by same user
        :param id_: project id
        :param title: title of the key
        :param key: the key itself
        :return: true if sucess, false if not
        """
        data = {"id": id_, "title": title, "key": key}
        request = requests.post(self.projects_url + "/" + str(id_) + "/keys",
                          headers=self.headers, data=data)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def deletedeploykey(self, id_, key_id):
        """
        Delete a deploy key from a project
        :param id_: project id
        :param key_id: key id to delete
        :return: true if success, false if not
        """
        request = requests.delete(self.projects_url + "/" + str(id_) + "/keys/"
                                  + str(key_id), headers=self.headers)
        if request.status_code == 200:
            return True
        else:
            print request
            return False

    def getreadme(self, repo, md=False):
        """
        returns the readme
        :param md: If false returns the raw readme,
        else returns the readme parsed by markdown
        :param repo: the web url to the project
        """
        request = requests.get(repo + "/raw/master/README.md?private_token=" +
                         self.token)  # setting the headers doesn't work
        if "<!DOCTYPE html>" in request.content:  # having HTML means a 404
            if md:
                return "<p>There isn't a README.md for that project</p>"
            else:
                return "There isn't a README.md for that project"
        else:
            if md:
                return markdown.markdown(request.content)
            else:
                return request.content

    def creategroup(self, name, path):
        """
        Creates a new group
        :param name: The name of the group
        :param path: The path for the group
        """
        request = requests.post(self.groups_url,
                                data={'name': name, 'path': path},
                                headers=self.headers)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def getgroups(self, id_=None, page=1, per_page=20):
        """
        Retrieve group information
        :param id_: Specify a group. Otherwise, all groups are returned
        :param page: Which page to return (default is 1)
        :param per_page: Number of items to return per page (default is 20)
        """
        params = {'page': page, 'per_page': per_page}
        request = requests.get("{0}/{1}".format(self.groups_url,
                                                id_ if id_ else ""),
                               params=params, headers=self.headers)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def moveproject(self, groupID, projectID):
        """
        Move a given project into a given group
        :param groupID: ID of the destination group
        :param projectID: ID of the project to be moved
        """
        request = requests.post("{0}/{1}/projects/{2}".format(self.groups_url,
                                                        groupID, projectID),
                          headers=self.headers)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def getmergerequests(self, projectID, page=None, per_page=None):
        """
        Get all the merge requests for a project.
        :param projectID: ID of the project to retrieve merge requests for
        :param page: If pagination is set, which page to return
        :param per_page: Number of merge requests to return per page
        """
        params = {'page': page, 'per_page': per_page}
        url_str = '{0}/{1}/merge_requests'.format(self.projects_url, projectID)
        request = requests.get(url_str, params=params, headers=self.headers)

        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False

    def getmergerequest(self, projectID, mergeRequestID):
        """
        Get information about a specific merge request.
        :param projectID: ID of the project
        :param mergeRequestID: ID of the merge request
        """
        url_str = '{0}/{1}/merge_request/{2}'.format(self.projects_url,
                                                     projectID, mergeRequestID)
        request = requests.get(url_str, headers=self.headers)

        if request.status_code == 200:
            return json.loads(request.content)
        else:
            print request
            return False
            
    def createmergerequest(self, projectID, sourceBranch, targetBranch,
                           title, assigneeID=None):
        """
        Create a new merge request.
        :param projectID: ID of the project originating the merge request
        :param sourceBranch: name of the branch to merge from
        :param targetBranch: name of the branch to merge to
        :param title: Title of the merge request
        :param assigneeID: Assignee user ID
        """
        url_str = '{0}/{1}/merge_requests'.format(self.projects_url, projectID)
        params = {'source_branch': sourceBranch,
                  'target_branch': targetBranch,
                  'title': title,
                  'assignee_id': assigneeID}

        request = requests.post(url_str, data=params, headers=self.headers)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def updatemergerequest(self, projectID, mergeRequestID, sourceBranch=None,
                           targetBranch=None, title=None,
                           assigneeID=None, closed=None):
        """
        Update an existing merge request.
        :param projectID: ID of the project originating the merge request
        :param mergeRequestID: ID of the merge request to update
        :param sourceBranch: name of the branch to merge from
        :param targetBranch: name of the branch to merge to
        :param title: Title of the merge request
        :param assigneeID: Assignee user ID
        :param closed: MR status.  True = closed
        """
        url_str = '{0}/{1}/merge_request/{2}'.format(self.projects_url,
                                                     projectID, mergeRequestID)
        params = {'source_branch': sourceBranch,
                  'target_branch': targetBranch,
                  'title': title,
                  'assignee_id': assigneeID,
                  'closed': closed}

        request = requests.post(url_str, data=params, headers=self.headers)
        if request.status_code == 201:
            return True
        else:
            print request
            return False

    def addcommenttomergerequest(self, projectID, mergeRequestID, note):
        """
        Add a comment to a merge request.
        :param projectID: ID of the project originating the merge request
        :param mergeRequestID: ID of the merge request to comment on
        :param note: Text of comment
        """
        url_str = '{0}/{1}/merge_request/{2}/comments'.format(self.projects_url,
                                                              projectID,
                                                              mergeRequestID)
        request = requests.post(url_str, data={'note': note},
                                headers=self.headers)

        if request.status_code == 201:
            return True
        else:
            print request
            return False
