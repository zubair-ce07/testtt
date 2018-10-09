# -*- coding: utf-8 -*-
import json
import csv

import scrapy
from scrapy.item import Item, Field
from w3lib.url import add_or_replace_parameter


class OnBoardingItem(Item):
    company_name = Field()
    header_name = Field()
    joining_company = Field()
    meet_your_manager = Field()
    professional_development = Field()


class CultureItem(Item):
    company_name = Field()
    header_name = Field()
    company_culture_score = Field()
    compensation_score = Field()
    happiness_score = Field()
    retention_score = Field()
    meeting_score = Field()
    diversity_score = Field()
    gender_score = Field()
    executive_team_score = Field()
    ceo_rating_score = Field()
    leadership_score = Field()
    perks_and_benefits_score = Field()
    team_score = Field()
    outlook_score = Field()
    work_culture_score = Field()
    manager_score = Field()
    professional_development_score = Field()
    enps_score = Field()
    environment_score = Field()
    office_culture_score = Field()


class LeadershipItem(Item):
    company_name = Field()
    header_name = Field()
    ceo_score_by_gender = Field()
    ceo_score_by_department = Field()
    ceo_score_by_employee_tenure = Field()
    ceo_score_by_ethnicity = Field()
    manager_score_by_gender = Field()
    manager_score_by_department = Field()
    manager_score_by_employee_tenure = Field()
    manager_score_by_ethnicity = Field()


class WorkLifeBalanceItem(Item):
    company_name = Field()
    header_name = Field()
    work_life_balance_score = Field()
    happiness_score = Field()
    culture_score = Field()
    balance_by_department = Field()
    balance_by_experience = Field()
    questions = Field()
    highest_rank_work_life = Field()
    lowest_rank_work_life = Field()


class InterviewsItem(Item):
    company_name = Field()
    header_name = Field()
    interview_sentiment = Field()
    interview_experience = Field()
    culture_score = Field()
    questions = Field()
    highest_rank_interview = Field()
    lowest_rank_interview = Field()


class CareersItem(Item):
    company_name = Field()
    header_name = Field()
    happiness_by_gender = Field()
    happiness_by_ethnicity = Field()
    happiness_by_experience = Field()
    happiness_highest_score = Field()
    happiness_lowest_score = Field()
    environment_by_gender = Field()
    environment_by_ethnicity = Field()
    environment_by_experience = Field()
    environment_highest_score = Field()
    environment_lowest_score = Field()
    retention_by_gender = Field()
    retention_by_ethnicity = Field()
    retention_by_experience = Field()
    retention_highest_score = Field()
    retention_lowest_score = Field()


class EmployerBrandItem(Item):
    company_name = Field()
    header_name = Field()
    employer_brand_by_department = Field()
    company_employee_perception_questions = Field()
    office_culture_questions = Field()


class AwardItem(Item):
    company_name = Field()
    header_name = Field()
    awards_list = Field()


class ReviewItem(Item):
    company_name = Field()
    header_name = Field()
    sentiments = Field()
    reviews_list = Field()


class OfficeVibeItem(Item):
    company_name = Field()
    header_name = Field()
    office_vibe_letter_score = Field()
    environment_letter_score = Field()
    team_letter_score = Field()
    office_vibe_questions = Field()
    company_office_vibe_by_department = Field()


class MissionItem(Item):
    company_name = Field()
    header_name = Field()
    mission_statement = Field()
    vision_statement = Field()
    values = Field()
    questions = Field()


class PTOItem(Item):
    company_name = Field()
    header_name = Field()
    questions_by_tenure = Field()
    questions_by_age = Field()
    questions_by_years = Field()


class EmployeeItem(Item):
    company_name = Field()
    header_name = Field()
    overall_culture_score_by_gender = Field()
    overall_culture_score_by_ethnicity = Field()
    overall_culture_score_by_department = Field()
    overall_culture_score_by_tenure = Field()
    overall_culture_score_by_years = Field()
    company_employees_sentiment_questions = Field()


class InnovationItem(Item):
    company_name = Field()
    header_name = Field()
    questions = Field()


class ReputationItem(Item):
    company_name = Field()
    header_name = Field()
    customer_reputation = Field()
    employer_reputation = Field()
    recommend_working_at_company = Field()
    good_company_reputation_questions = Field()


class KPIandOKRItem(Item):
    company_name = Field()
    header_name = Field()
    questions = Field()


class GrowthItem(Item):
    company_name = Field()
    header_name = Field()
    growth_at_company_questions = Field()
    measuring_growth_questions = Field()
    employee_outlook_grade = Field()
    employee_outlook_questions = Field()


class EmployeeEngagementItem(Item):
    company_name = Field()
    header_name = Field()
    company_employee_engagement_questions = Field()
    company_values_questions = Field()


class OverviewItem(Item):
    company_name = Field()
    header_name = Field()
    employee_participants = Field()
    total_ratings = Field()
    ceo_name = Field()
    company_culture_score = Field()
    awards = Field()
    ceo_score = Field()
    gender_score = Field()
    diversity_score = Field()
    top_badges = Field()
    positive_reviews = Field()
    constructive_feedback = Field()
    enps = Field()
    overall_culture_score_by_department = Field()
    score_by_gender = Field()
    ceo_score_by_department = Field()
    ceo_score_by_tenure = Field()
    ceo_score_by_ethnicity = Field()
    leadership_score_questions = Field()
    compensation_score_questions = Field()
    team_score_questions = Field()
    environment_score_questions = Field()
    outlook_score_questions = Field()


class ComparablySpiderSpider(scrapy.Spider):

    name = 'comparably_spider'

    allowed_domains = ['www.comparably.com']

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "DOWNLOAD_DELAY": 1.25
    }

    def start_requests(self):
        #company_names = self.read_company_names()
        company_names = ["Microsoft", "Netflix"]

        for company_name in company_names:
            url = "https://www.comparably.com/search"
            url = add_or_replace_parameter(url, "q", company_name)

            yield scrapy.Request(url=url, headers={"control": "mixin"}, callback=self.parse,
                                 meta={"company": company_name})

    def parse(self, response):
        data = json.loads(response.text)
        r = scrapy.Selector(text=data["body"])

        results = r.xpath("//a[@class='result primary']")

        for res in results:
            res_company_name = res.xpath("descendant-or-self::div[@class='content']/text()").extract_first()
            if res_company_name == "{} Company Page".format(response.meta["company"]):
                url = res.xpath("@href").extract_first()
                yield scrapy.Request(url=url, callback=self.parse_company_page, meta=response.meta)

    def parse_company_page(self, response):
        headers = ["Culture", "Leadership", "Reviews", "Interviews", "Work/Life", "Careers", "Office Vibe",
                   "Awards", "Mission", "Employer Brand", "Employee Onboarding", "PTO", "Employees",
                   "Innovation", "Reputation", "KPIs & OKRs", "Growth", "Employee Engagement"]
        parser_map = {
            "Employee Onboarding": self.parse_onboarding,
            "Culture": self.parse_culture,
            "Leadership": self.parse_leadership,
            "Work/Life": self.parse_work_life,
            "Interviews": self.parse_interviews,
            "Careers": self.parse_careers,
            "Employer Brand": self.parse_employer_brand,
            "Awards": self.parse_award_pages,
            "Reviews": self.parse_reviews,
            "Office Vibe": self.parse_office_vibe,
            "Mission": self.parse_mission,
            "PTO": self.parse_pto,
            "Employees": self.parse_employee,
            "Innovation": self.parse_innovation,
            "Reputation": self.parse_reputation,
            "KPIs & OKRs": self.parse_kpiokr,
            "Growth": self.parse_growth,
            "Employee Engagement": self.parse_employee_engagement
        }

        all_headers = response.xpath("//*[@class='cppNav-list']//a")

        links = {}

        for header in all_headers:
            if header.xpath("text()").extract_first() in headers:
                links[header.xpath("text()").extract_first()] = header.xpath("@href").extract_first()

        response.meta["header_name"] = "Overview"
        yield from self.parse_overview(response)

        for header_name, link in links.items():
            response.meta["header_name"] = header_name
            yield scrapy.Request(url=link, callback=parser_map[header_name], meta=response.meta)

    def parse_leadership(self, response):
        leadership_item = LeadershipItem()
        leadership_item["company_name"] = response.meta["company"]
        leadership_item["header_name"] = response.meta["header_name"]

        leadership_item["ceo_score_by_gender"] = self.process_overview_graph(
            response.css(".ceo .gender .overview-graphs"))

        leadership_item["ceo_score_by_department"] = self.process_overview_graph(
            response.css(".ceo .departments .overview-graphs"))

        leadership_item["ceo_score_by_employee_tenure"] = self.process_overview_graph(
            response.css(".ceo .tenure .overview-graphs"))

        leadership_item["ceo_score_by_ethnicity"] = self.process_overview_graph(
            response.css(".ceo .ethnicity .overview-graphs"))

        leadership_item["manager_score_by_gender"] = self.process_overview_graph(
            response.css(".manager .gender .overview-graphs"))

        leadership_item["manager_score_by_department"] = self.process_overview_graph(
            response.css(".manager .departments .overview-graphs"))

        leadership_item["manager_score_by_employee_tenure"] = self.process_overview_graph(
            response.css(".manager .tenure .overview-graphs"))

        leadership_item["manager_score_by_ethnicity"] = self.process_overview_graph(
            response.css(".manager .ethnicity .overview-graphs"))

        yield leadership_item

    def parse_employee_engagement(self, response):
        employee_engagement_item = EmployeeEngagementItem()
        employee_engagement_item["company_name"] = response.meta["company"]
        employee_engagement_item["header_name"] = response.meta["header_name"]

        questions_map = {
            "How frequently does your company participate in community outreach?":
                "//*[@data-question-id='202'][@class='result user-answered answered']/div[1]"
        }
        employee_engagement_item["company_employee_engagement_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "Which of the following set of Company Values is most meaningful to you?":
                "//*[@data-question-id='138'][@class='result user-answered answered']/div[1]",
            "Are you proud to be a part of your company?":
                "//*[@data-question-id='139']/div[1]"
        }
        employee_engagement_item["company_values_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield employee_engagement_item

    def parse_growth(self, response):
        growth_item = GrowthItem()
        growth_item["company_name"] = response.meta["company"]
        growth_item["header_name"] = response.meta["header_name"]

        questions_map = {
            "Do you approve of the job your executive team is doing at your company?":
                "//*[@data-question-id='104']/div[1]",
            "How would you rate your company's growth rate?":
                "//*[@data-question-id='197']/div[1]"
        }
        growth_item["growth_at_company_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "How would you rate the effectiveness of your CEO to drive business results?":
                "//*[@data-question-id='152'][@class='result user-answered answered']/div[1]",
            "How much has your company's revenue grown in the last year?":
                "//*[@data-question-id='145'][@class='result user-answered answered']/div[1]"
        }
        growth_item["measuring_growth_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        growth_item["employee_outlook_grade"] = self.process_letter_grade(
            response.xpath("//*[contains(text(), 'Employee Outlook at')]/..//div[contains(@class, 'letterGrade')]"))

        questions_map = {
            "How do your customers perceive your company?":
                "//*[@data-question-id='69'][@class='result user-answered answered']/div[1]",
            "How confident are you about the future success of your company?":
                "//*[@data-question-id='68']/div[1]"
        }
        growth_item["employee_outlook_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield growth_item

    def parse_kpiokr(self, response):
        kpiokr_item = KPIandOKRItem()
        kpiokr_item["company_name"] = response.meta["company"]
        kpiokr_item["header_name"] = response.meta["header_name"]

        questions_map = {
            "Are the KPIs/OKRs for your department clear?":
                "//*[@data-question-id='200']/div[1]",
            "Are you typically recognized for the impact and accomplishments you make for your current company?":
                "//*[@data-question-id='153']/div[1]",
            "How often do you receive valuable feedback from your Manager?":
                "//*[@data-question-id='76'][@class='result user-answered answered']/div[1]",
        }
        kpiokr_item["questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield kpiokr_item

    def parse_reputation(self, response):
        reputation_item = ReputationItem()
        reputation_item["company_name"] = response.meta["company"]
        reputation_item["header_name"] = response.meta["header_name"]
        common_xpath_rep = "//*[text()='{}']/../p/text()"
        reputation_item["customer_reputation"] = response.xpath(common_xpath_rep.format('Customer Reputation'))\
            .extract_first()
        reputation_item["employer_reputation"] = response.xpath(common_xpath_rep.format('Employer Reputation'))\
            .extract_first()
        common_xpath_recommendation = "//*[contains(text(),'Do employees recommend')]/" \
                                      "following::div//div[text()='{}']/../div[@class='percent']/text()"
        reputation_item["recommend_working_at_company"] = {
            "yes": response.xpath(common_xpath_recommendation.format("Yes")).extract_first(),
            "neutral": response.xpath(common_xpath_recommendation.format("Neutral")).extract_first(),
            "no": response.xpath(common_xpath_recommendation.format("No")).extract_first(),
        }

        questions_map = {
            "Is your current company transparent about the financial status and well being of your company?":
                "//*[@data-question-id='188']/div[1]",
            "Does your current employer focus on improving your company culture?":
                "//*[@data-question-id='149']/div[1]",
            "Are you typically recognized for the impact and accomplishments you make for your current company?":
                "//*[@data-question-id='153']/div[1]"
        }
        reputation_item["good_company_reputation_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield reputation_item

    def parse_innovation(self, response):
        innovation_item = EmployeeItem()
        innovation_item["company_name"] = response.meta["company"]
        innovation_item["header_name"] = response.meta["header_name"]

        questions_map = {
            "How innovative is your company?":
                "//*[@data-question-id='198'][@class='result user-answered answered']/div[1]",
            "How often do you receive valuable feedback from your Manager?":
                "//*[@data-question-id='76'][@class='result user-answered answered']/div[1]"
        }
        innovation_item["company_employees_sentiment_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield innovation_item

    def parse_employee(self, response):
        employee_item = EmployeeItem()
        employee_item["company_name"] = response.meta["company"]
        employee_item["header_name"] = response.meta["header_name"]

        common_xpath = ('//*[@class="cppExtras-demographic-title"][text()='
                        '"{}"]/following::*[@class="cppExtras-demographic-content"][1]')

        employee_item["overall_culture_score_by_ethnicity"] = self.process_graded_horizontal_graph(
            response.xpath(common_xpath.format("Ethnicity")))
        employee_item["overall_culture_score_by_gender"] = self.process_graded_horizontal_graph(
            response.xpath(common_xpath.format("Gender")))
        employee_item["overall_culture_score_by_department"] = self.process_graded_horizontal_graph(
            response.xpath(common_xpath.format("Department")))
        employee_item["overall_culture_score_by_tenure"] = self.process_graded_horizontal_graph(
            response.xpath(common_xpath.format("Tenure")))
        employee_item["overall_culture_score_by_years"] = self.process_graded_horizontal_graph(
            response.xpath(common_xpath.format("Years of Experience")))

        questions_map = {
            "Are you typically excited about going to work each day?":
                "//*[@data-question-id='70']/div[1]",
            "What percent of your potential do you think you are using?":
                "//*[@data-question-id='25'][@class='result user-answered answered']/div[1]"
        }
        employee_item["company_employees_sentiment_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield employee_item

    def parse_pto(self, response):
        pto_item = PTOItem()
        pto_item["company_name"] = response.meta["company"]
        pto_item["header_name"] = response.meta["header_name"]
        pto_item["questions_by_tenure"] = {
            "question_text": "How much paid vacation and sick days can you take a year?",
            "graph": self.process_layered_horizontal_graph(
                response.xpath('//*[@class="cppPTO-demo-nav-title"][text()="Tenure"]/..'))
        }
        pto_item["questions_by_age"] = {
            "question_text": "How much paid vacation and sick days can you take a year?",
            "graph": self.process_layered_horizontal_graph(
                response.xpath('//*[@class="cppPTO-demo-nav-title"][text()="Age"]/..'))
        }
        pto_item["questions_by_years"] = {
            "question_text": "How much paid vacation and sick days can you take a year?",
            "graph": self.process_layered_horizontal_graph(
                response.xpath('//*[@class="cppPTO-demo-nav-title"][text()="Years of Experience"]/..'))
        }

        yield pto_item

    def parse_mission(self, response):
        mission_item = MissionItem()
        mission_item["company_name"] = response.meta["company"]
        mission_item["header_name"] = response.meta["header_name"]
        mission_item["mission_statement"] = \
            response.xpath("//*[text()='Mission Statement']/../p/text()").extract_first()
        mission_item["vision_statement"] = \
            response.xpath("//*[text()='Vision Statement']/../p/text()").extract_first()
        mission_item["values"] = \
            response.xpath("//*[text()='Values']/../p/text()").extract_first()

        questions_map = {
            "Are you proud to be apart of your company?":
                "//*[@data-question-id='139']/div[1]",
            "Are you motivated by your company's mission, vision, & values?":
                "//*[@data-question-id='182']/div[1]",
            "How important was your Company's mission while job searching?":
                "//*[@data-question-id='183'][@class='result user-answered answered']/div[1]",
            "Are your company goals clear, and are you invested in them?":
                "//*[@data-question-id='47']/div[1]",
            "Besides your Salary, what’s most important to you about work?":
                "//*[@data-question-id='100'][@class='result user-answered answered']/div[1]",
            "To whom do you feel loyal at work?":
                "//*[@data-question-id='128'][@class='result user-answered answered']/div[1]",
            "What’s the main reason you stay at your current company?":
                "//*[@data-question-id='79'][@class='result user-answered answered']/div[1]",
            "Which of the following set of company values is most meaningful to you?":
                "//*[@data-question-id='138'][@class='result user-answered answered']/div[1]"
        }
        mission_item["questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield mission_item

    def parse_overview(self, response):
        overview_item = OverviewItem()
        overview_item["company_name"] = response.meta["company"]
        overview_item["header_name"] = response.meta["header_name"]
        overview_item["employee_participants"] = response.css('.js-participantsCount::text').extract_first()
        overview_item["total_ratings"] = response.css('.js-ratingsCount::text').extract_first()
        overview_item["ceo_name"] = (' '.join(response.css('.ceoName span::text').extract())).strip()
        overview_item["company_culture_score"] = response.css('.cppOverview-summary .letterGrade::text').extract_first()
        overview_item["awards"] = self.process_awards(response.css('.cppOverview-awards'))
        overview_item["ceo_score"] = '{}/100'.format(response.css('.ceoScore .grade-text::text').extract_first())
        overview_item["gender_score"] = self.process_sparkline(response.css('.cppOverview-gender'))
        overview_item["diversity_score"] = self.process_sparkline(response.css('.cppOverview-diversity'))
        overview_item["top_badges"] = self.process_top_badges(response.css('.cppOverview-summary-rankings'))
        overview_item["positive_reviews"] = self.process_reviews(
            response.css('.cppReviewsPositiveNegative-colPositive'))
        overview_item["constructive_feedback"] = self.process_reviews(
            response.css('.cppReviewsPositiveNegative-colNegative'))
        overview_item["enps"] = self.process_enps(response.css('.cppOverview-enps'))
        overview_item["overall_culture_score_by_department"] = self.process_vertical_graph(
            response.css('.cppOverview-ratingsByDepartment'))

        overview_item["score_by_gender"] = self.process_overview_graph(
            response.css(".ceo .gender .overview-graphs"))

        overview_item["ceo_score_by_department"] = self.process_overview_graph(
            response.css(".ceo .departments .overview-graphs"))

        overview_item["ceo_score_by_tenure"] = self.process_overview_graph(
            response.css(".ceo .tenure .overview-graphs"))

        overview_item["ceo_score_by_ethnicity"] = self.process_overview_graph(
            response.css(".ceo .ethnicity .overview-graphs"))

        questions_map = {
            "Executive rating?":
                "//*[@data-question-id='62']/div[1]",
            "CEO rating?":
                "//*[@data-question-id='71']/div[1]",
            "Manager rating?":
                "//*[@data-question-id='72']/div[1]",
        }
        overview_item["leadership_score_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "Paid fairly?":
                "//*[@data-question-id='16']/div[1]",
            "Satisfied with benefits?":
                "//*[@data-question-id='63']/div[1]",
        }
        overview_item["compensation_score_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "Meeting effective?":
                "//*[@data-question-id='52']/div[1]",
            "Coworker interaction?":
                "//*[@data-question-id='64']/div[1]",
            "Quality of coworkers?":
                "//*[@data-question-id='65']/div[1]",
        }
        overview_item["team_score_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "Work hours per day?":
                "//*[@data-question-id='55'][@class='result user-answered answered']/div[1]",
            "Pace at work?":
                "//*[@data-question-id='66'][@class='result user-answered answered']/div[1]",
            "Positive/Negative":
                "//*[@data-question-id='67'][@class='result user-answered answered']/div[1]",
        }
        overview_item["environment_score_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "Future outlook?":
                "//*[@data-question-id='68']/div[1]",
            "Customer perception?":
                "//*[@data-question-id='69'][@class='result user-answered answered']/div[1]",
            "Excited going to work?":
                "//*[@data-question-id='70']/div[1]",
        }
        overview_item["outlook_score_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        yield overview_item

    def parse_office_vibe(self, response):
        office_vibe_item = OfficeVibeItem()
        office_vibe_item["company_name"] = response.meta["company"]
        office_vibe_item["header_name"] = response.meta["header_name"]
        common_xpath = '//*[text()="{}"][@class="section-subtitle"]/following::div[contains(@class, "letterGrade")][1]'
        field_names = ["office_vibe_letter_score", "environment_letter_score", "team_letter_score"]
        xpath_names = ["Office Vibe", "Environment", "Team"]

        for field, xpath_name in zip(field_names, xpath_names):
            office_vibe_item[field] = self.process_letter_grade(response.xpath(common_xpath.format(xpath_name)))

        questions_map = {
            "How would you describe the Office vibe at your company?":
                "//*[@data-question-id='177'][@class='result user-answered answered']/div[1]",
            "Does your current company have a great office vibe?":
                "//*[@data-question-id='176']/div[1]"
        }
        office_vibe_item["office_vibe_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        office_vibe_item["company_office_vibe_by_department"] = self.process_table_wrapper(
            response.xpath('//*[contains(text(), "Office Vibe by Department")]'
                           '/following::div[@class="tableWrapper"]'))

        yield office_vibe_item

    def parse_reviews(self, response):
        if response.meta.get("item"):
            review_item = response.meta["item"]
            review_item["reviews_list"].extend(self.process_reviews(response.css('.pager_container')))
        else:
            review_item = ReviewItem()
            review_item["company_name"] = response.meta["company"]
            review_item["header_name"] = response.meta["header_name"]
            review_item["sentiments"] = self.process_review_sentiment(response.xpath(
                '//*[@class="section-subtitle"][contains(text(), "Review Sentiment")]/..'))
            review_item["reviews_list"] = self.process_reviews(response.css('.pager_container'))

        if not response.css('.pager_next.disabled'):
            link = response.css('.pager_next::attr(href)').extract_first()
            yield scrapy.Request(link, callback=self.parse_reviews, meta={"item": review_item})
        else:
            yield review_item

    def parse_award_pages(self, response):
        award_years_links = response.css(".yearSelector a::attr(href)").extract()
        for link in award_years_links:
            yield scrapy.Request(link, callback=self.parse_awards, meta=response.meta)

    def parse_awards(self, response):
        award_item = AwardItem()
        award_item["company_name"] = response.meta["company"]
        award_item["header_name"] = response.meta["header_name"]
        award_item["awards_list"] = self.process_awards(response.css('.comparablyAwards'))

        yield award_item

    def parse_employer_brand(self, response):
        employer_brand_item = EmployerBrandItem()
        employer_brand_item["company_name"] = response.meta["company"]
        employer_brand_item["header_name"] = response.meta["header_name"]

        employer_brand_item["employer_brand_by_department"] = self.process_table_wrapper(
            response.xpath('//*[contains(text(), "Employer Brand by Department")]'
                           '/following::div[@class="tableWrapper"]'))

        questions_map = {
            "Do you believe you're paid fairly?":
                "//*[@data-question-id='16']/div[1]",
            "Would you leave your current job for a 20% raise at a different company?":
                "//*[@data-question-id='102']/div[1]",
            "Are you challenged at work?":
                "//*[@data-question-id='21']/div[1]",
            "How would you rate the quality of your coworkers?":
                "//*[@data-question-id='65']/div[1]",
        }
        employer_brand_item["company_employee_perception_questions"] = [
            self.process_question(response.xpath(q_xpath), question) for question, q_xpath in questions_map.items()]

        questions_map = {
            "What's your opinion of what the overall business climate will be like in 2018?":
                "//*[@data-question-id='155'][@class='result user-answered answered']/div[1]",
            "How would you describe the Office vibe at your company?":
                "//*[@data-question-id='177'][@class='result user-answered answered']/div[1]",
            "How often do you socialize with team members outside of work?":
                "//*[@data-question-id='60'][@class='result user-answered answered']/div[1]",
            "Is your work environment positive or negative?":
                "//*[@data-question-id='67'][@class='result user-answered answered']/div[1]"
        }
        employer_brand_item["office_culture_questions"] = [self.process_question(response.xpath(q_xpath), question)
                                                           for question, q_xpath in questions_map.items()]

        yield employer_brand_item

    def parse_careers(self, response):
        career_item = CareersItem()
        career_item["company_name"] = response.meta["company"]
        career_item["header_name"] = response.meta["header_name"]

        common_xpath_gender = '//*[contains(text(), "{} at")][@class="section-subtitle"]/..' \
                              '//div[@class="genderLabel"][text()="{}"]/..//div[contains(@class,"letterGrade")]'
        common_xpath_ethnicity = '//*[@class="section-subtitle"][contains(text(), "{}")]//..//' \
                                 '*[contains(@class, "segment")]//*[@class="section-subtitle"][text()="Ethnicity"]' \
                                 '//ancestor-or-self::div[contains(@class, "segment")][1]'
        common_xpath_experience = '//*[@class="section-subtitle"][contains(text(), "{}")]//..//' \
                                  '*[contains(@class, "segment")]//*[@class="section-subtitle"][text()="Experience"]' \
                                  '//ancestor-or-self::div[contains(@class, "segment")][1]'
        career_item["happiness_by_gender"] = {
            "male": self.process_letter_grade(response.xpath(common_xpath_gender.format("Happiness", "Male"))),
            "female": self.process_letter_grade(response.xpath(common_xpath_gender.format("Happiness", "Female"))),
        }

        career_item["happiness_by_ethnicity"] = self.process_segment_table(
            response.xpath(common_xpath_ethnicity.format("Happiness")))
        career_item["happiness_by_experience"] = self.process_segment_table(
            response.xpath(common_xpath_experience.format("Happiness")))

        career_item["happiness_highest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Happiness the highest?")]/..'))
        career_item["happiness_lowest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Happiness the lowest?")]/..'))

        career_item["environment_by_gender"] = {
            "male": self.process_letter_grade(response.xpath(common_xpath_gender.format("Environment", "Male"))),
            "female": self.process_letter_grade(response.xpath(common_xpath_gender.format("Environment", "Female"))),
        }

        career_item["environment_by_ethnicity"] = self.process_segment_table(
            response.xpath(common_xpath_ethnicity.format("Environment")))
        career_item["environment_by_experience"] = self.process_segment_table(
            response.xpath(common_xpath_experience.format("Environment")))

        career_item["environment_highest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Environment the highest?")]/..'))
        career_item["environment_lowest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Environment the lowest?")]/..'))

        career_item["retention_by_gender"] = {
            "male": self.process_letter_grade(response.xpath(common_xpath_gender.format("Retention", "Male"))),
            "female": self.process_letter_grade(response.xpath(common_xpath_gender.format("Retention", "Female"))),
        }

        career_item["retention_highest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Retention the highest?")]/..'))
        career_item["retention_lowest_score"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who ranks Retention the lowest?")]/..'))

        career_item["retention_by_ethnicity"] = self.process_segment_table(
            response.xpath(common_xpath_ethnicity.format("Retention")))
        career_item["retention_by_experience"] = self.process_segment_table(
            response.xpath(common_xpath_experience.format("Retention")))

        yield career_item

    def parse_interviews(self, response):
        interview_item = InterviewsItem()
        interview_item["company_name"] = response.meta["company"]
        interview_item["header_name"] = response.meta["header_name"]
        interview_item["interview_sentiment"] = self.process_question(
            response.xpath("//*[@data-question-id='166']/div[1]"), "Interview Sentiment")

        common_xpath = '//*[text()="{}"][@class="section-subtitle"]/following::div[contains(@class, "letterGrade")][1]'
        field_names = ["interview_experience", "culture_score"]
        xpath_names = ["Interview Experience", "Culture Score"]

        for field, xpath_name in zip(field_names, xpath_names):
            interview_item[field] = self.process_letter_grade(response.xpath(common_xpath.format(xpath_name)))

        questions_map = {
            "How would you rate the interview process at your company?":
                "//*[@data-question-id='167']/div[1]",
            "How did you get your first interview at your current company?":
                "//*[@data-question-id='168'][@class='result user-answered answered']/div[1]",
            "How many phone/in person interviews did you have before you were hired at your current company?":
                "//*[@data-question-id='172'][@class='result user-answered answered']/div[1]"
        }
        interview_item["questions"] = [self.process_question(response.xpath(q_xpath), question)
                                       for question, q_xpath in questions_map.items()]

        interview_item["highest_rank_interview"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who Ranks the Interview Process the Highest")]/..'))
        interview_item["lowest_rank_interview"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who Ranks the Interview Process the Lowest")]/..'))

        yield interview_item

    def parse_work_life(self, response):
        work_life_item = WorkLifeBalanceItem()
        work_life_item["company_name"] = response.meta["company"]
        work_life_item["header_name"] = response.meta["header_name"]
        common_xpath = '//*[text()="{}"][@class="section-subtitle"]/following::div[contains(@class, "letterGrade")][1]'
        field_names = ["work_life_balance_score", "happiness_score", "culture_score"]
        xpath_names = ["Work Life Balance", "Happiness", "Culture Score"]

        for field, xpath_name in zip(field_names, xpath_names):
            work_life_item[field] = self.process_letter_grade(response.xpath(common_xpath.format(xpath_name)))

        work_life_item["balance_by_department"] = self.process_table_wrapper(
            response.xpath('//*[contains(text(), "Work Life Balance by Department")]'
                           '/following-sibling::div[@class="tableWrapper"][1]'))
        work_life_item["balance_by_experience"] = self.process_table_wrapper(
            response.xpath('//*[contains(text(), "Work Life Balance by Experience")]'
                           '/following-sibling::div[@class="tableWrapper"][1]'))

        questions_map = {
            "Are you satisfied with your work/life balance?":
                "//*[@data-question-id='54']/div[1]",
            "On average, how many hours do you work a day?":
                "//*[@data-question-id='55'][@class='result user-answered answered']/div[1]",
            "How long do you take for lunch breaks?":
                "//*[@data-question-id='57'][@class='result user-answered answered']/div[1]",
            "Do you feel burnt out at work?":
                "//*[@data-question-id='107']/div[1]",
            "How’s the work life balance at your company?":
                "//*[@data-question-id='173'][@class='result user-answered answered']/div[1]"

        }
        work_life_item["questions"] = [self.process_question(response.xpath(q_xpath), question)
                                       for question, q_xpath in questions_map.items()]

        work_life_item["highest_rank_work_life"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who Ranks the Work Life Balance highest at")]/..'))
        work_life_item["lowest_rank_work_life"] = self.process_horizontal_graph(
            response.xpath('//*[contains(text(), "Who Ranks the Work Life Balance lowest at")]/..'))

        yield work_life_item

    def parse_culture(self, response):
        culture_item = CultureItem()

        common_xpath = '//*[text()="{}"][@class="section-subtitle"]/following::div[contains(@class, "letterGrade")][1]'

        culture_item["company_name"] = response.meta["company"]
        culture_item["header_name"] = response.meta["header_name"]
        culture_item['company_culture_score'] = self.process_rainbow_graph(response.css(".rainbowGraph"))

        field_names = ["compensation_score", "happiness_score", "retention_score", "meeting_score",
                       "diversity_score", "gender_score", "executive_team_score", "ceo_rating_score",
                       "leadership_score", "perks_and_benefits_score", "team_score", "outlook_score",
                       "work_culture_score", "manager_score", "professional_development_score", "enps_score",
                       "environment_score", "office_culture_score"]
        xpath_names = ["Compensation", "Happiness", "Retention", "Meetings", "Diversity", "Gender",
                       "Executive Team", "CEO Rating", "Leadership", "Perks And Benefits", "Team", "Outlook",
                       "Work Culture", "Manager", "Professional Development", "eNPS", "Environment",
                       "Office Culture"]

        for field, xpath_name in zip(field_names, xpath_names):
            culture_item[field] = self.process_letter_grade(response.xpath(common_xpath.format(xpath_name)))

        yield culture_item

    def parse_onboarding(self, response):
        onboarding_item = OnBoardingItem()
        onboarding_item["company_name"] = response.meta["company"]
        onboarding_item["header_name"] = response.meta["header_name"]

        joining_questions_map = {
            "Did you have a positive onboarding experience when you were hired at your current company? ":
                "//*[@data-question-id='185']/div[1]",
            "How prepared was your company on your first day of onboarding?":
                "//*[@data-question-id='185']/div[1]",
            "Was your direct manager helpful with your onboarding during your first 90 days?":
                "//*[@data-question-id='186']/div[1]"
        }
        onboarding_item["joining_company"] = [self.process_question(response.xpath(q_xpath), question)
                                              for question, q_xpath in joining_questions_map.items()]

        meet_question_map = {
            "How often do you receive valuable feedback from your Manager?":
                "//*[@data-question-id='76'][@class='result user-answered answered']/div[1]",
            "Does your boss expect you to work when you're on vacation?":
                "//*[@data-question-id='133']/div[1]",
            "Do you feel comfortable giving your boss negative feedback?":
                "//*[@data-question-id='119']/div[1]"
        }

        onboarding_item["meet_your_manager"] = [self.process_question(response.xpath(q_xpath), question)
                                                for question, q_xpath in meet_question_map.items()]

        pro_dev_question_map = {
            "Do you have a mentor at work?":
                "//*[@data-question-id='24']/div[1]",
            "Does your current company provide you meaningful opportunities or career advancement?":
                "//*[@data-question-id='129']/div[1]"
        }

        onboarding_item["professional_development"] = [self.process_question(response.xpath(q_xpath), question)
                                                       for question, q_xpath in pro_dev_question_map.items()]

        yield onboarding_item

    def process_overview_graph(self, raw_overview_graph):
        graph = []
        for row in raw_overview_graph.css('.barLabel'):
            if not row.css('.barLabel-name::text'):
                continue

            graph.append({
                'name': row.css('.barLabel-name::text').extract_first(),
                'value': row.css('.barLabel-value::text').extract_first()
            })

        for col in raw_overview_graph.css('.gs-col'):
            if not col.css('.verticalBar-label::text'):
                continue

            graph.append({
                'name': col.css('.verticalBar-label::text').extract_first(),
                'value': col.css('.cap span::text').extract_first()
            })

        return graph

    def process_letter_grade(self, letter_grade_selector):
        lg = {'grade': letter_grade_selector.css('.letterGrade::text').extract_first()}
        score = ''.join(letter_grade_selector.css('.letterGrade + .numberGrade span::text').extract())
        if score:
            lg["score"] = score
        return lg

    def process_question(self, question_selector, question):
        if question_selector.xpath("@class").extract_first() == 'insightsPie':
            return {
                "question_text": question,
                "percentage": question_selector.xpath("@data-percentage").extract_first()
            }
        if question_selector.xpath("@class").extract_first() == 'insightsYesNo':
            return {
                "question_text": question,
                "yes": question_selector.xpath("@data-yes").extract_first(),
                "no": question_selector.xpath("@data-no").extract_first()
            }
        if question_selector.xpath("@class").extract_first() == 'result-inner user-answered answered':
            return {
                "question_text": question,
                "options": self.user_options(question_selector)
            }

    def user_options(self, question_selector):
        options = []
        for ans in question_selector.css('.answer'):
            options.append({
                'title': ans.css('.answer-text::text').extract_first(),
                'percentage': ans.css('[data-percentage]::attr(data-percentage)').extract_first()
            })

        return options

    def process_table_wrapper(self, raw_table):
        table = {}
        headers = raw_table.css('th::text').extract()

        for row in raw_table.css('tbody tr'):
            label = row.css('.label::text').extract_first()
            grades = row.css('.groupGradeLetter::text').extract()

            table[label] = {}

            for i in range(0, len(grades)):
                table[label][headers[i]] = grades[i]

        return table

    def process_rainbow_graph(self, raw_rainbow_graph):
        return {
            'grade': raw_rainbow_graph.css('.rainbowGraph-text .letterGrade::text').extract_first(),
            'score': ''.join(raw_rainbow_graph.css('.rainbowGraph-text .numberGrade span::text').extract())
        }

    def process_horizontal_graph(self, raw_horizontal_graph):
        graph = []

        for row in raw_horizontal_graph.css('.horizontal-bar'):
            graph.append({
                'name': row.css('.horizontal-bar-legend-label::text').extract_first(),
                'score': ''.join(row.css(
                    '.horizontal-bar-legend-percent::text, .horizontal-bar-legend-percent span::text').extract())
            })

        return graph

    def process_segment_table(self, raw_segment_table):
        table = {}
        for row in raw_segment_table.css('.segmentRow'):
            table[row.css('.segmentLabel::text').extract_first()] = row.css('.segmentGradeLetter::text').extract_first()

        return table

    def process_awards(self, raw_awards):
        return raw_awards.css('.cmToolTip-container::text').extract()

    def process_review_sentiment(self, raw_sentiment):
        return {
            'positive': raw_sentiment.css('.positive .horizontal-bar-legend-percent::text').extract_first(),
            'negative': raw_sentiment.css('.negative .horizontal-bar-legend-percent::text').extract_first()
        }

    def process_reviews(self, raw_reviews):
        reviews = []

        for review in raw_reviews.css('.cppReviewHighlight-review'):
            question = review.css('.cppReviewHighlight-review-subtitle::text').extract_first()
            answers = []

            for answer in review.css('[itemprop="review"]'):
                answers.append(
                    ''.join(answer.css('[itemprop="reviewBody"]::text, [itemprop="reviewBody"] *::text').extract()))

            reviews.append({
                'question': question,
                'answers': answers
            })

        return reviews

    def process_layered_horizontal_graph(self, raw_graph):
        graph = {}
        selectors = zip(raw_graph.css('a::attr(href)').extract(), raw_graph.css('a::text').extract())
        for id, text in selectors:
            graph[text] = self.process_horizontal_graph(raw_graph.css(id))

        return graph

    def process_graded_horizontal_graph(self, raw_graph):
        graph = {}
        for row in raw_graph.css('.cppExtras-demographic-content > .offset'):
            graph[row.css('.grade-label::text').extract_first()] = {
                'grade': row.css('.grade-text::text').extract_first(),
                'percentage': ''.join(row.css(
                    '.horizontal-bar-legend-percent::text, .horizontal-bar-legend-percent span::text').extract())
            }

        return graph

    def process_vertical_graph(self, raw_vertical_graph):
        graph = {}
        for bar in raw_vertical_graph.css('.verticalBar'):
            graph[bar.css('.verticalBar-label::text').extract_first()] = bar.css('.capScore::text').extract_first()

        return graph

    def process_enps(self, raw_enps):
        return {
            'score': raw_enps.css('.numberGrade-score::text').extract_first(),
            'callout': raw_enps.css('.cmToolTip-container::text').extract_first()
        }

    def process_top_badges(self, raw_badges):
        badges = []
        for badge in raw_badges.css('p'):
            badges.append(''.join(badge.css('p::text, p *::text').extract()))

        return badges

    def process_sparkline(self, raw_sparkline):
        return {
            'score': ''.join(raw_sparkline.css('.numberGrade span::text').extract()),
            'award': raw_sparkline.css('.award .hide-me::text').extract_first()
        }

    def read_company_names(self):
        names = []

        with open("Limeade TAM List 10 2018.csv") as f:
            reader = csv.DictReader(f)
            for a in reader:
                names.append(a["Company Name"])
        return names
