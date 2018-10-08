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


class ComparablySpiderSpider(scrapy.Spider):
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
        test_header = ["Interviews"]

        parser_map = {
            "Employee Onboarding": self.parse_onboarding,
            "Culture": self.parse_culture,
            "Leadership": self.parse_leadership,
            "Work/Life": self.parse_work_life,
            "Interviews": self.parse_interviews
        }

        all_headers = response.xpath("//*[@class='cppNav-list']//a")

        links = {}

        for header in all_headers:
            if header.xpath("text()").extract_first() in test_header:
                links[header.xpath("text()").extract_first()] = header.xpath("@href").extract_first()

        #response.meta["header_name"] = "Overview"
        #yield from self.parse_raw_html(response)

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

    def read_company_names(self):
        names = []

        with open("Limeade TAM List 10 2018.csv") as f:
            reader = csv.DictReader(f)
            for a in reader:
                names.append(a["Company Name"])
        return names
