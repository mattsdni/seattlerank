something = "AQSUclIZWfLdDzCxyoDUGATEb7_Z63sGN5zJfHNbTCFg0szIolOD9BwdqOSx9sqlPQ-31VgQbx3bHQxA1h4DnP5oHjNlMDCylN47BkMKDVsf3TK23No"


from linkedin import linkedin

CONSUMER_KEY
CONSUMER_SECRET 
USER_TOKEN
USER_SECRET


# Instantiate the developer authentication class

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                                          USER_TOKEN, USER_SECRET, 
                                                          RETURN_URL, linkedin.PERMISSIONS.enums.values())

# Pass it in to the app...

application = linkedin.LinkedInApplication(authentication)

# Use the app....

application.get_profile()


