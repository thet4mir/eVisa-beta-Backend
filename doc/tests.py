from main.tests import BaseTestCase


class DocTest(BaseTestCase):

    def test_list(self):
        self.login_superuser()
        rsp = self.get('/api/doc/all/', doAssert=False)
        self.assertEqual(rsp.status_code, 200)
