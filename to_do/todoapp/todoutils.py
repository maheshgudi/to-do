class EmailManipulation(object):
    """Contains methods for manipulating email data."""

    @staticmethod
    def get_email_domain(email):
        """A very simple and flawed function to get domain names from a user 
           email"""
        return email.split('@')[1]
