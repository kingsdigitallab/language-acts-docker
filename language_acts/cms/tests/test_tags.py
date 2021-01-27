from datetime import date

from language_acts.cms.models.pages import (
    IndexPage, HomePage
)
from language_acts.cms.templatetags import cms_tags
from language_acts.cms.tests.factories import (
    IndexPageFactory, BlogIndexPageFactory, BlogPostFactory,
    BlogAuthorFactory, HomePageFactory, EventFactory, EventIndexPageFactory,
    NewsIndexPageFactory, NewsPostFactory
)
from language_acts.cms.models.snippets import (
    GlossaryTerm
)
from django.test import RequestFactory, TestCase
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText


class CMSTagsTestCase(TestCase):
    """Helper class to store wagtail content creation for easier tag
    testing"""
    test_page_title = 'Parent Test Page'

    def setUp(self) -> None:
        site_root, created = Page.objects.get_or_create(id=2)
        self.home_page = HomePageFactory.build()
        site_root.add_child(instance=self.home_page)
        self.top_page = IndexPageFactory.build(
            title='Index Test',
            live=True
        )
        self.top_page.show_in_menus = True
        self.home_page.add_child(
            instance=self.top_page
        )

        self.top_page.add_child(
            instance=IndexPageFactory.build(
                title=self.test_page_title,
                live=True
            )
        )
        self.page_1 = IndexPageFactory.build(live=True)
        self.page_1.show_in_menus = True
        self.top_page.add_child(
            instance=self.page_1
        )
        self.top_page.add_child(
            instance=IndexPageFactory.build(live=True),
        )


class TestGetSection(CMSTagsTestCase):

    def test_get_section(self):
        page = IndexPage.objects.get(title=self.test_page_title)
        # pass bad params make sure it handles it
        homepage = HomePage.objects.first()
        current_section = Page.objects.ancestor_of(page,
                                                   inclusive=True) \
            .child_of(homepage).first()
        self.assertTrue(cms_tags.get_section(page), current_section.pk)


class TestBreadcrumbs(CMSTagsTestCase):

    def test_breadcrumbs(self):
        page = IndexPage.objects.get(title=self.test_page_title)
        # pass bad params make sure it handles it
        homepage = HomePage.objects.first()
        context = {'request': []}
        breadcrumbs = cms_tags.breadcrumbs(context, homepage, page)
        self.assertIn('root', breadcrumbs)
        self.assertIn('current_page', breadcrumbs)
        self.assertIn('pages', breadcrumbs)
        self.assertEqual(2, breadcrumbs['pages'].count())
        self.assertEqual(page.pk, breadcrumbs['pages'][1].pk)


class TestFooterMenu(CMSTagsTestCase):

    def test_footer_menu(self):
        # pass bad params make sure it handles it
        context = {'request': []}
        #
        self.event_index = EventIndexPageFactory.build(
            title='Event Index Test',
            show_in_menus=True
        )
        self.home_page.add_child(
            instance=self.event_index
        )
        # make sure only 4 come back
        self.event_1 = EventFactory.build(show_in_menus=True)
        self.event_index.add_child(instance=self.event_1)
        self.event_index.add_child(
            instance=EventFactory.build(show_in_menus=True))
        self.event_index.add_child(
            instance=EventFactory.build(show_in_menus=True))
        footer = cms_tags.footer_menu(context, self.event_index, self.event_1)
        self.assertIn('root', footer)
        self.assertIn('current_page', footer)
        self.assertIn('menu_pages', footer)
        self.assertEqual(3, footer['menu_pages'].count())


class TestGetHomepageEvents(CMSTagsTestCase):

    def test_get_homepage_events(self) -> None:
        self.event_2 = EventFactory.build(
            title='Event Today',
            date_from=date.today()
        )
        self.event_index = EventIndexPageFactory.build(
            title='Event Index Test'
        )
        self.home_page.add_child(
            instance=self.event_index
        )
        self.event_index.add_child(instance=self.event_2)
        events = cms_tags.get_homepage_events()
        self.assertTrue(events.count(), 1)
        # make sure only 4 come back
        self.event_index.add_child(instance=EventFactory.build())
        self.event_index.add_child(instance=EventFactory.build())
        self.event_index.add_child(instance=EventFactory.build())
        self.event_index.add_child(instance=EventFactory.build())
        self.event_index.add_child(instance=EventFactory.build())
        self.event_index.add_child(instance=EventFactory.build())
        events = cms_tags.get_homepage_events()
        self.assertTrue(cms_tags.get_homepage_events().count(), 4)


class TestLines(TestCase):

    def test_lines(self) -> None:
        self.assertTrue(cms_tags.lines('A\r\nB')[0] == 'A')
        self.assertTrue(cms_tags.lines('A\nB')[0] == 'A')


class TestQuerify(TestCase):

    def test_querify(self) -> None:
        self.assertTrue(cms_tags.querify('?q='), '?q=')
        self.assertTrue(cms_tags.querify('test'), 'test?q=')


class TestNewsPreview(TestCase):

    def test_news_preview(self) -> None:
        site_root, created = Page.objects.get_or_create(id=2)
        self.home_page = HomePageFactory.build()
        site_root.add_child(instance=self.home_page)
        self.news_index = NewsIndexPageFactory.build()
        self.home_page.add_child(instance=self.news_index)
        self.news_post_1 = NewsPostFactory.build()
        self.news_index.add_child(instance=self.news_post_1)
        self.assertEqual(
            cms_tags.get_news_preview()[0].pk, self.news_post_1.pk)
        self.news_index.add_child(instance=NewsPostFactory.build())
        self.news_index.add_child(instance=NewsPostFactory.build())
        self.news_index.add_child(instance=NewsPostFactory.build())
        self.news_index.add_child(instance=NewsPostFactory.build())
        self.assertEqual(cms_tags.get_news_preview().count(), 3)


class TestBlogPostsPreview(TestCase):

    def test_get_blog_posts_preview(self) -> None:
        site_root, created = Page.objects.get_or_create(id=2)
        self.home_page = HomePageFactory.build()
        site_root.add_child(instance=self.home_page)
        blog_index = BlogIndexPageFactory.build()
        self.home_page.add_child(instance=blog_index)
        author_1 = BlogAuthorFactory()
        post_1 = BlogPostFactory.build(author=author_1)
        blog_index.add_child(instance=post_1)
        self.assertEqual(
            cms_tags.get_blog_posts_preview()[0].pk, post_1.pk)
        blog_index.add_child(instance=BlogPostFactory.build(author=author_1))
        blog_index.add_child(instance=BlogPostFactory.build(author=author_1))
        blog_index.add_child(instance=BlogPostFactory.build(author=author_1))
        blog_index.add_child(instance=BlogPostFactory.build(author=author_1))
        self.assertEqual(
            cms_tags.get_blog_posts_preview().count(), 4)


class TestPageInSubmenu(CMSTagsTestCase):

    def test_page_in_submenu(self) -> None:
        page = IndexPage.objects.get(title=self.test_page_title)
        # pass bad params make sure it handles it
        self.assertFalse(cms_tags.page_in_submenu(page, None))
        self.assertFalse(cms_tags.page_in_submenu(None, self.top_page))
        # Find page in submenu only if it's toggled in menu
        # nope
        self.assertFalse(cms_tags.page_in_submenu(page, self.top_page))
        # now
        page.show_in_menus = True
        page.save()
        self.assertTrue(cms_tags.page_in_submenu(page, self.top_page))


class TestGetTogglerStatusPageInSubmenu(CMSTagsTestCase):

    def test_get_toggler_status(self) -> None:
        page = IndexPage.objects.get(title=self.test_page_title)
        request = RequestFactory().get('test')
        self.assertFalse(
            cms_tags.get_toggler_status({'request': request}, page))
        request = RequestFactory().get('test?toggler_open={}'.format(page.pk))
        self.assertTrue(cms_tags.get_toggler_status(
            {'request': request}, page))


class TestGetRequestParameters(TestCase):

    def test_get_request_parameters(self) -> None:
        factory = RequestFactory()
        get_string = "page=1&stuff=1"
        request = factory.get('/test?' + get_string)
        context = {'request': request}
        new_get_string = cms_tags.get_request_parameters(context)
        self.assertTrue('stuff=1' in new_get_string)
        self.assertTrue('page=1' in new_get_string)
        self.assertEqual(
            cms_tags.get_request_parameters(context, 'page'), '&stuff=1')


class TestShowChildrenInMenu(CMSTagsTestCase):

    def setUp(self) -> None:
        super().setUp()
        # Add a blog whose children we shouldn't see
        self.blog_index = BlogIndexPageFactory.build(
            title=self.test_page_title,
            live=True
        )
        self.top_page.add_child(
            instance=self.blog_index
        )
        self.blog_1 = BlogPostFactory.build(
            author=BlogAuthorFactory(),
            live=True
        )
        self.blog_index.add_child(
            instance=self.blog_1,
        )

    def test_show_children_show_in_menus(self):
        self.top_page.show_in_menus = True
        self.top_page.save()
        self.page_1.show_in_menus = True
        self.page_1.save()
        tag_dict = cms_tags.show_children_in_menu(self.top_page)
        self.assertIn('show_children', tag_dict)
        self.assertIn('children', tag_dict)
        self.assertTrue(tag_dict['show_children'])
        self.assertGreater(tag_dict['children'].count(), 0)
        tag_dict = cms_tags.show_children_in_menu(self.blog_index)
        # children for blogs shouldn't be displayed
        self.assertFalse(tag_dict['show_children'])
        self.assertTemplateUsed('cms/tags/show_children_show_in_menus.html')


class AddReferencesTestCase(TestCase):
    def test_add_references(self):
        term = GlossaryTerm(
            term='term', description='term description'
        )
        term.save()
        # nothing should be found
        test_text = RichText("not here")
        value = cms_tags.add_references(test_text)
        self.assertTrue(value.source, test_text.source)
        # term should be found here
        test_text = RichText("term here")
        value = cms_tags.add_references(test_text)
        self.assertTrue(value.source,
                        '<a title="term description" href="#">term</a> here')
