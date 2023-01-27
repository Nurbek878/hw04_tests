from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            id='100',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user_no_author = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_no_author)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_group_slug_url_exists_at_desired_location(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_location(self):
        """Страница /profile/<username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/HasNoName/')
        self.assertEqual(response.status_code, 200)

    def test_posts_id_url_exists_at_desired_location(self):
        """Страница /posts/<post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/100/')
        self.assertEqual(response.status_code, 200)

    def test_inexisting_page_url_exists_at_desired_location(self):
        """Страница /unexisting_page/ доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_posts_id_edit_url_exists_at_desired_location_authorized(self):
        """Страница /posts/<post_id>/edit/ доступна
        автору"""
        response = self.authorized_client_author.get('/posts/100/edit/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_exists_at_desired_location_authorized(self):
        """Страница /create/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_posts_id_edit_url_redirect_anonymous(self):
        """Страница /posts/<post_id>/edit/ перенаправляет
        анонимного пользователя."""
        response = self.guest_client.get('/posts/100/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/100/edit/')

    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного
        пользователя."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            '/posts/100/': 'posts/post_detail.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
