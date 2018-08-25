import json
from django.test import TestCase
from django.test import Client
from graphene.test import Client as GrapheneClient

# Inherit from this in your test cases
class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client()
        self.token = None

    def add_authorization(self, token):
        self._client.headers.update({'authorization': 'JWT '+token})

    def execute(self, query: str, operation_name: str = None, variables: dict = None, token: str = None):

        body = {'query': query}
        if operation_name:
            body['operation_name'] = operation_name
        if input:
            body['variables'] =  variables

        client = GrapheneClient()
        executed = client.execute(json.dumps(body), context_value={'authorization': 'JWT '+token})

        return executed


    def query(self, query: str, operation_name: str = None, variables: dict = None):
        '''
        Args:
            query (string) - GraphQL query to run
            op_name (string) - If the query is a mutation or named query, you must
                               supply the op_name.  For annon queries ("{ ... }"),
                               should be None (default).
            input (dict) - If provided, the $input variable in GraphQL will be set
                           to this value

        Returns:
            dict, response from graphql endpoint.  The response has the "data" key.
                  It will have the "error" key if any error happened.
        '''
        body = {'query': query}
        if operation_name:
            body['operation_name'] = operation_name
        if input:
            body['variables'] =  variables

        header = {"Authorization": "JWT " + self.token} if self.token else {}
        header["Content-Type"] = "application/json"

        resp = self._client.post('/graphql', json.dumps(body),
                                 content_type='application/json',
                                 **header)
        jresp = json.loads(resp.content.decode())
        return jresp

    def login(self, username:str = "guest", password:str = "test1234"):
        # User.objects.create(username='test', password='hunter2')
        resp = self.query(
            # The mutation's graphql code
            '''
            mutation LoginMutation($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                  token
                }
            }
            ''',
            # The operation name (from the 1st line of the mutation)
            operation_name = 'LoginMutation',
            variables = {'username': username, 'password': password}
        )
        self.assertResponseNoErrors(resp)

        self.token = resp["data"]["tokenAuth"]["token"]
        

    def assertResponseNoErrors(self, resp: dict, expected: dict = None):
        '''
        Assert that the resp (as retuened from query) has the data from
        expected
        '''
        self.assertNotIn('errors', resp, 'Response had errors')
        if expected is not None:
            self.assertEqual(resp['data'], expected, 'Response has correct data')

   