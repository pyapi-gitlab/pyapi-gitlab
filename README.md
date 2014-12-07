# pyapi-gitlab

pyapi-gitlab is a python wrapper for the [Gitlab API](https://github.com/gitlabhq/gitlabhq/tree/master/doc/api).

[![Build Status](https://travis-ci.org/Itxaka/pyapi-gitlab.svg?branch=develop)](https://travis-ci.org/Itxaka/pyapi-gitlab)
[![PyPI version](https://badge.fury.io/py/pyapi-gitlab.png)](http://badge.fury.io/py/pyapi-gitlab)
[![Coverage Status](https://coveralls.io/repos/Itxaka/pyapi-gitlab/badge.png?branch=develop)](https://coveralls.io/r/Itxaka/pyapi-gitlab?branch=develop)
[![PyPi downloads](https://pypip.in/d/pyapi-gitlab/badge.png)](https://crate.io/packages/pyapi-gitlab/)
[![License](http://img.shields.io/pypi/l/pyapi-gitlab.svg)](http://www.gnu.org/copyleft/gpl.html)




## Requirements

- requests


## Naming convention

pyapi-gitlab has its own versioning in which the 2 first numbers indicates the Gitlab version that its supported for that library. a 7.5 version means that its compatible with the Gitlab 7.5 and lower API versions.

## Installation

pyapi-gitlab is now on Pypi!

Depending on the gitlab version you are using (check it on your help section on gitlab) you will need a different version.

Latest version

Gitlab 7.5.0:
```bash
pip install pyapi-gitlab=="7.5.0"
```


Old versions not maintained:

Gitlab 5.4:
```bash
pip install pyapi-gitlab==5.4-0
```

Gitlab 6.0 or 6.1:
```bash
pip install pyapi-gitlab==6.1.6
```

Gitlab 6.2:
```bash
pip install pyapi-gitlab==6.2.3
```

pyapi-gitlab supports python version 2.6, 2.7, 3.3 and 3.4


## Changes in the latest version

 - Support for the full Gitlab 7.5 API
 - All methods have documentation (Inside the library only, the docs are lagging a bit behind).
 - New fork api that allows to actually fork a project instead of doing fork relations
 - New label methods (getlabel, createlabel, editlabel, deletelabel)

 - BREAKING CHANGE: Some methods were returning True or False instead of the object created. Now all the methods in which there is something returning from the server is returned as a dictionary/list of dictionaries to the user
 - BREAKING CHANGE: Some methods now use kwargs for the optional parameters so the code is more easy. For example, createissue now will take as much optional named params as you want without making the code unreadable.
 - BREAKING CHANGE: Project wallnotes does not exist anymore, seems that they have been moved to project snippets (getsnippets, getsnippet, createsnippet, deletesnippet)
 - BREAKING CHANGE: Removed getreadme method as its not part of the gitlab api, nor was it ever.
 - BREAKING CHANGE: Old methods that started with list* are not get*. This is done in order to have a proper naming convention instead of having mixed listsomething and then getsomething. The actual

## Examples/Documentation

Check the docs at [readthedocs.org](http://pyapi-gitlab.readthedocs.org)

## License

pyapi-gitlab is licensed under the GPL3. Check the LICENSE file.
