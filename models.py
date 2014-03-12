
from django.db import models
from django.template import RequestContext, Template, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import Orderable, SiteRelated
from mezzanine.core.request import current_request
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to


DEFAULT_COPYRIGHT = '&copy {% now "Y" %} {{ settings.SITE_TITLE }}'


class SiteConfiguration(SiteRelated):
    '''
    A model to edit sitewide content
    '''
    col1_heading = models.CharField(max_length=200, default="Contact us")
    col1_content = RichTextField()
    col2_heading = models.CharField(max_length=200, default="Go social")
    col2_content = RichTextField(blank=True, 
                                 help_text="If present will override the "
                                           "social network icons.")
    col3_heading = models.CharField(max_length=200, default="Subscribe")
    col3_content = RichTextField()
    twitter_link = models.CharField(max_length=2000, blank=True)
    facebook_link = models.CharField(max_length=2000, blank=True)
    pinterest_link = models.CharField(max_length=2000, blank=True)
    youtube_link = models.CharField(max_length=2000, blank=True)
    github_link = models.CharField(max_length=2000, blank=True)
    linkedin_link = models.CharField(max_length=2000, blank=True)
    vk_link = models.CharField(max_length=2000, blank=True)
    gplus_link = models.CharField(max_length=2000, blank=True)
    has_social_network_links = models.BooleanField(default=False, blank=True)
    copyright = models.TextField(default=DEFAULT_COPYRIGHT)

    class Meta:
        verbose_name = _('Site Configuration')
        verbose_name_plural = _('Site Configuration')

    def save(self, *args, **kwargs):
        '''
        Set has_social_network_links
        '''
        if (self.twitter_link or self.facebook_link or self.pinterest_link or
            self.youtube_link or self.github_link or self.linkedin_link or
            self.vk_link or self.gplus_link):
            self.has_social_network_links = True
        else:
            self.has_social_network_links = False
        super(SiteConfiguration, self).save(*args, **kwargs)

    
    def render_copyright(self):
        '''
        Render the footer
        '''
        c = RequestContext(current_request())
        try:
            t = Template(self.copyright)
        except TemplateSyntaxError:
            return ''
        return t.render(c)


class HomePage(Page):
    '''
    A home page page type
    '''
    heading = models.CharField(max_length=100)
    slide_in_one_icon = models.CharField(max_length=50, blank=True)
    slide_in_one = models.CharField(max_length=200, blank=True)
    slide_in_two_icon = models.CharField(max_length=50, blank=True)
    slide_in_two = models.CharField(max_length=200, blank=True)
    slide_in_three_icon = models.CharField(max_length=50, blank=True)
    slide_in_three = models.CharField(max_length=200, blank=True)
    header_background = FileField(verbose_name=_("Header Background"),
        upload_to=upload_to("theme.HomePage.header_background", "homepage"),
        format="Image", max_length=255, blank=True)
    header_image = FileField(verbose_name=_("Header Image (optional)"),
        upload_to=upload_to("theme.HomePage.header_image", "homepage"),
        format="Image", max_length=255, blank=True, null=True)
    welcome_heading = models.CharField(max_length=100, default="Welcome")
    content = RichTextField()
    recent_blog_heading = models.CharField(max_length=100,
        default="Latest blog posts")
    number_recent_posts = models.PositiveIntegerField(default=3,
        help_text="Number of recent blog posts to show")

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class IconBox(Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="boxes")
    icon = models.CharField(max_length=50,
        help_text="Enter the name of a font awesome icon, i.e. "
                  "fa-eye. A list is available here "
                  "http://fontawesome.io/")
    title = models.CharField(max_length=200)
    link_text = models.CharField(max_length=100)
    link = models.CharField(max_length=2000, blank=True,
        help_text="Optional, if provided clicking the box will go here.")
