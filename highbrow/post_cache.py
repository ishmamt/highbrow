from datetime import datetime


class Pagination():
    def __init__(self):
        self.number_of_posts_in_a_page = 2

        self.current_newsfeed_page = 1
        self.current_own_profile_page = 1
        self.current_saved_posts_page = 1
        self.current_topic_posts_page = 1

        self.previous_newsfeed_first_post_time = datetime.now()
        self.previous_own_profile_first_post_time = datetime.now()
        self.previous_saved_posts_first_post_time = datetime.now()
        self.previous_topic_posts_first_post_time = datetime.now()

        self.previous_newsfeed_last_post_time = datetime.now()
        self.previous_own_profile_last_post_time = datetime.now()
        self.previous_saved_posts_last_post_time = datetime.now()
        self.previous_topic_posts_last_post_time = datetime.now()

        self.newsfeed_last_post_time = datetime.now()
        self.own_profile_last_post_time = datetime.now()
        self.saved_posts_last_post_time = datetime.now()
        self.topic_posts_last_post_time = datetime.now()

        self.newsfeed_first_post_time = datetime.now()
        self.own_profile_first_post_time = datetime.now()
        self.saved_posts_first_post_time = datetime.now()
        self.topic_posts_first_post_time = datetime.now()
