from gitlab.base import Base


class Keys(Base):
    def keys(self, id):
        """
        Get SSH key with user by ID of an SSH key. Note only administrators can lookup SSH key with user by ID of an
        SSH key.

        >>> gitlab = Gitlab(host='http://localhost:10080', verify_ssl=False)
        >>> gitlab.login(user='root', password='5iveL!fe')
        >>> gitlab.keys(1)

        :param id: The ID of an SSH key
        :return: Dictionary containing Key data
        """
        return self.get('/keys/{id}'.format(id=id), default_response={})
