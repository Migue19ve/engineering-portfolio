import unittest
from scripts.check_public_content import inspect_text


class PublicationGuardTests(unittest.TestCase):
    def test_classic_and_fine_grained_shapes_are_detected(self):
        # Construct intentionally fake strings; never place real credentials here.
        self.assertIn('access token', inspect_text('ghp_' + 'A' * 36))
        self.assertIn('fine-grained token', inspect_text('github_pat_' + 'A' * 70))

    def test_normal_public_link_is_allowed(self):
        self.assertEqual(inspect_text('https://github.com/Migue19ve/engineering-portfolio'), [])
