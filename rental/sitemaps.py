from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.db.models import Max
from app.models import Inventory, SupportService


class BaseSitemap(Sitemap):
    """Base sitemap enforcing HTTPS protocol and production domain."""
    protocol = "https"

    def get_domain(self, site=None):
        return getattr(settings, "SITEMAP_DOMAIN", "sickbed.itegoss.in")


class StaticViewSitemap(BaseSitemap):
    """Sitemap for public, indexable informational and action landing pages."""

    PAGES = {
        "index": {"priority": 1.0, "changefreq": "daily"},
        "about": {"priority": 0.7, "changefreq": "monthly"},
        "terms": {"priority": 0.5, "changefreq": "yearly"},
        "organize_camp": {"priority": 0.7, "changefreq": "monthly"},
        "be_donor": {"priority": 0.7, "changefreq": "monthly"},
        "volunteer_event": {"priority": 0.7, "changefreq": "monthly"},
    }

    def items(self):
        return list(self.PAGES.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item]["priority"]

    def changefreq(self, item):
        return self.PAGES[item]["changefreq"]


class RentalItemsSitemap(BaseSitemap):
    """Sitemap for the rental equipment catalog."""
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ["items"]

    def location(self, item):
        return reverse("items")

    def lastmod(self, item):
        try:
            return Inventory.objects.aggregate(latest=Max("created_at"))["latest"]
        except Exception:
            return None


class ServicesSitemap(BaseSitemap):
    """Sitemap for medical and support service pages."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["services", "medical_services"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        try:
            return SupportService.objects.filter(is_active=True).aggregate(latest=Max("updated_at"))["latest"]
        except Exception:
            return None


sitemaps = {
    "static": StaticViewSitemap,
    "items": RentalItemsSitemap,
    "services": ServicesSitemap,
}
