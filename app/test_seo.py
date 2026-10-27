import xml.etree.ElementTree as ET
from django.test import TestCase, Client
from django.urls import reverse


class TechnicalSEOTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt_status_and_content(self):
        """Verify /robots.txt returns HTTP 200, text/plain, and correct directives."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/plain'))

        content = response.content.decode('utf-8')

        # Check crawler directive
        self.assertIn('User-agent: *', content)

        # Check allowed resources
        self.assertIn('Allow: /', content)
        self.assertIn('Allow: /static/', content)
        self.assertIn('Allow: /media/', content)

        # Check sitemap declaration
        self.assertIn('Sitemap: https://sickbed.itegoss.in/sitemap.xml', content)

        # Check disallow rules for sensitive/private paths
        expected_disallows = [
            '/admin/',
            '/auth/',
            '/cart/',
            '/add-to-cart/',
            '/signin/',
            '/signup/',
            '/logout/',
            '/userdetail/',
            '/payment/',
            '/bookingsammry/',
            '/inventory/',
            '/request-blood/',
            '/notifications/',
            '/users/',
            '/roles/',
        ]
        for path in expected_disallows:
            self.assertIn(f'Disallow: {path}', content)

    def test_sitemap_xml_status_and_content(self):
        """Verify /sitemap.xml returns HTTP 200, application/xml, and valid XML with production HTTPS domain."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('application/xml'))

        content = response.content.decode('utf-8')

        # Validate that output is well-formed XML
        root = ET.fromstring(content)
        self.assertEqual(root.tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')

        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('ns:url', ns)
        self.assertGreater(len(urls), 0)

        locs = [u.find('ns:loc', ns).text for u in urls]

        # Verify all URLs strictly use the production domain and https
        for loc in locs:
            self.assertTrue(
                loc.startswith('https://sickbed.itegoss.in/'),
                f"URL does not use production HTTPS domain: {loc}"
            )

        # Verify key public pages are present
        expected_public_urls = [
            'https://sickbed.itegoss.in/',
            'https://sickbed.itegoss.in/items/',
            'https://sickbed.itegoss.in/about/',
            'https://sickbed.itegoss.in/terms/',
            'https://sickbed.itegoss.in/services/',
            'https://sickbed.itegoss.in/medical-services/',
            'https://sickbed.itegoss.in/organize-camp/',
            'https://sickbed.itegoss.in/be-donor/',
            'https://sickbed.itegoss.in/volunteer/',
        ]
        for expected in expected_public_urls:
            self.assertIn(expected, locs)

        # Verify private/sensitive URLs are NOT included in sitemap
        prohibited_fragments = [
            '/admin/',
            '/cart/',
            '/signin/',
            '/signup/',
            '/payment/',
            '/inventory/',
            '/userdetail/',
            '/bookingsammry/',
            '/request-blood/',
        ]
        for loc in locs:
            for frag in prohibited_fragments:
                self.assertNotIn(frag, loc)
