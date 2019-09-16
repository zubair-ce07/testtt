def profile_info_incomplete(user_profile):
    return (not user_profile.location or
            not user_profile.bio or
            not user_profile.birth_date)
