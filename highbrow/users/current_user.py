class CurrentUser():
    def __init__(self, fullname, username, email, password, remember_me,
                 profile_picture, num_followers, num_following, short_bio):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = password
        self.remember_me = remember_me
        self.profile_picture = profile_picture
        self.num_followers = num_followers
        self.num_following = num_following
        self.short_bio = short_bio
