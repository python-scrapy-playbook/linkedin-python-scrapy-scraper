import scrapy

class LinkedInPeopleProfileSpider(scrapy.Spider):
    name = "linkedin_people_profile"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.jsonl': { 'format': 'jsonlines',}}
        }

    def start_requests(self):
        profile_list = ['reidhoffman']
        for profile in profile_list:
            linkedin_people_url = f'https://www.linkedin.com/in/{profile}/' 
            yield scrapy.Request(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url})

    def parse_profile(self, response):
        item = {}
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']

        """
            SUMMARY SECTION
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        ## Location - now in profile-info-subheader
        try:
            location_text = response.css('div.profile-info-subheader span::text').get()
            item['location'] = location_text.strip() if location_text else ''
        except Exception as e:
            print('summary --> location', e)
            item['location'] = ''

        ## Followers and Connections - now in not-first-middot div
        item['followers'] = ''
        item['connections'] = ''

        for span_text in response.css('div.not-first-middot span::text').getall():
            span_text = span_text.strip()
            if 'followers' in span_text.lower():
                item['followers'] = span_text.replace(' followers', '').strip()
            if 'connections' in span_text.lower():
                item['connections'] = span_text.replace(' connections', '').strip()


        """
            ABOUT SECTION
        """
        item['about'] = response.css('section.summary div.core-section-container__content p::text').get()


        """
            EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_blocks = response.css('li.experience-item')
        for block in experience_blocks:
            experience = {}
            
            ## job title
            try:
                experience['title'] = block.css('span.experience-item__title::text').get().strip()
            except Exception as e:
                print('experience --> title', e)
                experience['title'] = ''

            ## company/organisation name
            try:
                experience['company'] = block.css('span.experience-item__subtitle::text').get().strip()
            except Exception as e:
                print('experience --> company', e)
                experience['company'] = ''

            ## organisation profile url
            try:
                experience['organisation_profile'] = block.css('a.profile-section-card__image-link::attr(href)').get().split('?')[0]
            except Exception as e:
                print('experience --> organisation_profile', e)
                experience['organisation_profile'] = ''

            ## location - second p.experience-item__meta-item (the one without date-range)
            try:
                meta_items = block.css('p.experience-item__meta-item')
                experience['location'] = ''
                for meta_item in meta_items:
                    # Skip the one that contains the date range
                    if not meta_item.css('span.date-range'):
                        location_text = meta_item.css('::text').get()
                        if location_text:
                            experience['location'] = location_text.strip()
                            break
            except Exception as e:
                print('experience --> location', e)
                experience['location'] = ''
                
            ## description
            try:
                experience['description'] = block.css('p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                print('experience --> description', e)
                try:
                    experience['description'] = block.css('p.show-more-less-text__text--less::text').get().strip()
                except Exception as e:
                    print('experience --> description', e)
                    experience['description'] = ''
                    
            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = 'present'
                else:
                    experience['start_time'] = ''
                    experience['end_time'] = ''
            except Exception as e:
                print('experience --> time ranges', e)
                experience['start_time'] = ''
                experience['end_time'] = ''

            ## duration
            try:
                duration_span = block.css('span.date-range span::text').get()
                experience['duration'] = duration_span.strip() if duration_span else ''
            except Exception as e:
                print('experience --> duration', e)
                experience['duration'] = ''
            
            item['experience'].append(experience)

        
        """
            EDUCATION SECTION
        """
        item['education'] = []
        education_blocks = response.css('li.education__list-item')

        for block in education_blocks:
            education = {}

            ## organisation - name is inside h3 > a > span
            try:
                education['organisation'] = block.css('h3 a span::text').get().strip()
            except Exception as e:
                print("education --> organisation", e)
                education['organisation'] = ''


            ## organisation profile url
            try:
                education['organisation_profile'] = block.css('a.profile-section-card__image-link::attr(href)').get().split('?')[0]
            except Exception as e:
                print("education --> organisation_profile", e)
                education['organisation_profile'] = ''

            ## course details - spans with class control-transition inside h4
            try:
                education['course_details'] = ''
                for text in block.css('h4 span.control-transition::text').getall():
                    education['course_details'] = education['course_details'] + text.strip() + ' '
                education['course_details'] = education['course_details'].strip()
            except Exception as e:
                print("education --> course_details", e)
                education['course_details'] = ''

            ## description - activities and societies in div.control-transition p
            try:
                education['description'] = block.css('div.control-transition p::text').get().strip()
            except Exception as e:
                print("education --> description", e)
                education['description'] = ''

         
            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = 'present'
            except Exception as e:
                print("education --> time_ranges", e)
                education['start_time'] = ''
                education['end_time'] = ''

            item['education'].append(education)
    

        """
            VOLUNTEERING SECTION
        """

        item['volunteering'] = []
        volunteering_blocks = response.css('section.volunteering li.profile-section-card')
        for block in volunteering_blocks:
            volunteering = {}
            
            ## role/title - direct text in h3
            try:
                volunteering['role'] = block.css('h3::text').get().strip()
            except Exception as e:
                print("volunteering --> role", e)
                volunteering['role'] = ''

            ## organisation name - text in h4 > a
            try:
                volunteering['organisation'] = block.css('h4 a::text').get().strip()
            except Exception as e:
                print("volunteering --> organisation", e)
                volunteering['organisation'] = ''

            ## organisation profile url
            try:
                volunteering['organisation_profile'] = block.css('a.profile-section-card__image-link::attr(href)').get().split('?')[0]
            except Exception as e:
                print("volunteering --> organisation_profile", e)
                volunteering['organisation_profile'] = ''

            ## cause - text in p.my-1.text-md (second p element typically)
            try:
                cause_text = block.css('p.my-1.text-md::text').get()
                volunteering['cause'] = cause_text.strip() if cause_text else ''
            except Exception as e:
                print("volunteering --> cause", e)
                volunteering['cause'] = ''

            ## description
            try:
                volunteering['description'] = block.css('p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                print("volunteering --> description", e)
                try:
                    volunteering['description'] = block.css('p.show-more-less-text__text--less::text').get().strip()
                except Exception as e:
                    print("volunteering --> description", e)
                    volunteering['description'] = ''

            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    volunteering['start_time'] = date_ranges[0]
                    volunteering['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    volunteering['start_time'] = date_ranges[0]
                    volunteering['end_time'] = 'present'
                else:
                    volunteering['start_time'] = ''
                    volunteering['end_time'] = ''
            except Exception as e:
                print("volunteering --> time_ranges", e)
                volunteering['start_time'] = ''
                volunteering['end_time'] = ''

            ## duration
            try:
                duration_text = block.css('span.date-range span::text').get()
                volunteering['duration'] = duration_text.strip() if duration_text else ''
            except Exception as e:
                print("volunteering --> duration", e)
                volunteering['duration'] = ''

            item['volunteering'].append(volunteering)


        """
            SKILLS SECTION
        """
        item['skills'] = []
        skill_items = response.css('section.skills li.skills__item a::text').getall()
        for skill in skill_items:
            item['skills'].append(skill.strip())


        """
            RECOMMENDATIONS SECTION
        """
        item['recommendations'] = []
        recommendation_blocks = response.css('section.recommendations div.endorsement-card')
        for block in recommendation_blocks:
            recommendation = {}

            ## recommender name
            try:
                recommendation['recommender_name'] = block.css('h3.base-main-card__title::text').get().strip()
            except Exception as e:
                print("recommendation --> recommender_name", e)
                recommendation['recommender_name'] = ''

            ## recommender profile url
            try:
                recommendation['recommender_profile'] = block.css('a.endorsement-card__entity::attr(href)').get().split('?')[0]
            except Exception as e:
                print("recommendation --> recommender_profile", e)
                recommendation['recommender_profile'] = ''

            ## recommendation content
            try:
                recommendation['content'] = block.css('p.endorsement-card__content::text').get().strip()
            except Exception as e:
                print("recommendation --> content", e)
                recommendation['content'] = ''

            item['recommendations'].append(recommendation)

        yield item