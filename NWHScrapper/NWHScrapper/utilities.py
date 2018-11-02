"""
Utility module containing all helper functions
to be used by spider.
"""


def prepare_search_request():
    """
    create form data and url for the POST request
    to get profile links of all doctors
    :return: dict containing url and form data
    """
    data = {
        '__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
        'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999',
    }

    url = 'https://www.nwh.org/find-a-doctor/find-a-doctor-home?type=1'
    return {
        'data': data,
        'url': url,
    }


def parse_name(response):
    """
    parse and return doctor's name
    :param response: response from hitting profile url
    :return: String: Doctor's name
    """
    full_name = "div.pnl-doctor-name>h1::text"
    return response.css(full_name).extract_first()


def parse_address(response):
    """
    parse and return doctor's residency address
    :param response: response from hitting profile url
    :return: String: doctor's residency
    """
    address = "div[id *= 'Residency']>ul>li::text"
    return response.css(address).extract()


def parse_speciality(response):
    """
    parse and return doctor's specialities
    :param response: response from hitting profile url
    :return: String: doctor's speciality
    """
    speciality = "div.pnl-doctor-specialty>h2::text"  # strip
    return response.css(speciality).extract_first().strip()


def parse_image_url(response):
    """
    parse and return doctor's profile image url
    :param response: response from hitting profile url
    :return: String: profile image url
    """
    image_url = "div.pnl-doctor-image>img::attr(src)"  # response.urljoin
    return response.css(image_url).extract_first()


def parse_affiliation(response):
    """
    parse and return affiliation of doctor
    :param response: response from hitting profile url
    :return: String: affiliation details
    """
    affiliation = "div[id *= 'Fellowship']>ul>li::text"
    return response.css(affiliation).extract_first()


def parse_medical_school(response):
    """
    parse and return medical school details of doctor
    :param response: response from hitting profile url
    :return: String: medical school name
    """
    medical_school = "div[id *= 'MedicalSchool']>ul>li::text"
    return response.css(medical_school).extract_first()


def parse_education(response):
    """
    parse and return graduate education information
    :param response: response from hitting profile url
    :return: String: graduate school information
    """
    graduate_education = "div[id *= 'Certifications']>ul>li::text"
    return response.css(graduate_education).extract_first()


def get_profile_ids(response):
    """
    parse and return ids of all profiles
    :param response: response from hitting POST request
    :return: list of profile ids
    """
    profile_ids = "div.search-results-physician>input::attr(value)"
    return response.css(profile_ids).extract()


def make_profile_urls(response):
    """
    parse and return profile urls of all doctors
    :param response: response from hitting POST request
    :return: list of profile urls of all doctors
    """
    profile_urls = []
    profile_ids = get_profile_ids(response)
    base_url = "https://www.nwh.org/find-a-doctor/find-a-doctor-profile"
    for profile_id in profile_ids:
        profile_url = base_url + "?id=" + str(profile_id)
        profile_urls.append(profile_url)
    return profile_urls
