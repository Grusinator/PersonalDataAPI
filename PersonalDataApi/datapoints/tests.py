"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import django
from django.test import TestCase

from PersonalDataApi.tests.GraphQLTestCase import GraphQLTestCase

# TODO: Configure your database in settings.py and sync before running tests.
Token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0IiwiZXhwIjoxNTM1MTE4NTA1LCJvcmlnX2lhdCI6MTUzNTExODIwNX0.Behbkb_R3OPuPubuoO0TIVl9jr-oPNgDTFBLvassKmU'


class DatapointTestCase(GraphQLTestCase):
    """Tests for the application views."""
    # Django requires an explicit setup() when running tests in PTVS
        
    @classmethod
    def setUpClass(cls):
        django.setup()

        



    def test_create_datapoint_audiodata(self):
        # User.objects.create(username='test', password='hunter2')
        
        self.login()

        input = {
            "datetime": None,
	        "category": "speech_audio",
	        "source_device": "insomnia",
	        "value": None,
	        "text_from_audio": None
        }


        output = {
            "datetime": None,
	        "category": "speech_audio",
	        "sourceDevice": "insomnia",
	        "value": None,
	        "textFromAudio": None
        }

        resp = self.query(
            # The mutation's graphql code
            '''
            mutation createDatapointMutation(
	            $datetime: DateTime, 
	            $category: CategoryTypes,
	            $source_device: String!,
	            $value: Float,
	            $text_from_audio: String
            ) {
              createDatapoint(
		            datetime:$datetime, 
		            category:$category,
		            sourceDevice:$source_device,
		            value:$value,
		            textFromAudio:$text_from_audio
	            ){
                    datetime
	                category
	                sourceDevice
	                value
	                textFromAudio
              }
            }
            ''',
            # The operation name (from the 1st line of the mutation)
            operation_name = 'createDatapointMutation',
            variables = input
        )


        self.assertResponseNoErrors(resp, {"createDatapoint" : output})



