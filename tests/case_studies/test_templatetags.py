

from django.test import TestCase
from ictcg.case_studies.templatetags.case_studies_tags import get_latest_case_studies
from ictcg.case_studies.models import CaseStudyPage
from wagtail.images.models import Image


class TemplateTagsCaseStudiesTests(TestCase):
    fixtures = ['app.json']

    def test_get_latest_case_studies(self):
        # Get case studies based on the selected language from fixture data
        case_studies = get_latest_case_studies('en')
        self.assertEqual(len(case_studies), 3)

    def test_get_latest_case_studies_ordering_and_number_of_results(self):
        # Test the order is correct by creating a new case study with the latest publication_date.
        # Also test we still only get 3 results back.  Fixture data contains 3 case studies
        image = Image.objects.get(id=1)
        new_case_study = CaseStudyPage.objects.create(
            path='00010002000100030004',
            depth='5',
            title='New case study 4',
            header_image=image,
            header_image_description='Alt tag',
            publication_date='2020-06-05',
            introduction='Case study number 4',
            collaborator='Mexico City Government',
            read_time=5,
        )

        case_studies = get_latest_case_studies('en')

        self.assertEqual(len(case_studies), 3)
        self.assertEqual(case_studies[0].pk, new_case_study.pk)
