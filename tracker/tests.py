from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404
from unittest.mock import patch

from tracker.models import Profile, MediaItem, UserMedia, Note, MediaType
from tracker.forms import CustomUserCreationForm, NoteForm

User = get_user_model()


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_registration_view_post_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_view_post_invalid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'pass',
            'password2': 'different'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())


class UserLibraryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.url = reverse('tracker:index')

        self.media1 = MediaItem.objects.create(
            title='Test Movie 1',
            type=MediaType.MOVIE
        )
        self.media2 = MediaItem.objects.create(
            title='Test Book 1',
            type=MediaType.BOOK
        )
        self.user_media1 = UserMedia.objects.create(user=self.user, item=self.media1)
        self.user_media2 = UserMedia.objects.create(user=self.user, item=self.media2)

    def test_library_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_library_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie 1')
        self.assertContains(response, 'Test Book 1')
        self.assertEqual(len(response.context['user_media_list']), 2)

    def test_library_view_shows_only_user_media(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        other_media = MediaItem.objects.create(title='Other Media', type=MediaType.GAME)
        UserMedia.objects.create(user=other_user, item=other_media)

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        self.assertNotContains(response, 'Other Media')
        self.assertEqual(len(response.context['user_media_list']), 2)


# class ProfileDetailViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.profile = self.user.profile
#         self.profile.bio = "Test bio"
#         self.profile.save()
#         self.media = MediaItem.objects.create(title='Test Media', type=MediaType.MOVIE)
#         self.user_media = UserMedia.objects.create(user=self.user, item=self.media)
#
#     def test_profile_detail_with_pk(self):
#         url = reverse('tracker:profile-detail', kwargs={'pk': self.profile.pk})
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['profile'], self.profile)
#
#     def test_profile_detail_without_pk_authenticated(self):
#         self.client.login(username='testuser', password='testpass')
#         url = reverse('tracker:profile-detail')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['profile'], self.user)
#
#     def test_profile_context_data(self):
#         url = reverse('tracker:profile-detail', kwargs={'pk': self.profile.pk})
#         response = self.client.get(url)
#
#         self.assertIn('user_media', response.context)
#         self.assertIn('media_titles', response.context)
#         self.assertEqual(response.context['media_titles'], ['Test Media'])

class MediaListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.movie1 = MediaItem.objects.create(title='Movie 1', type=MediaType.MOVIE)
        self.movie2 = MediaItem.objects.create(title='Movie 2', type=MediaType.MOVIE)
        self.book1 = MediaItem.objects.create(title='Book 1', type=MediaType.BOOK)

        UserMedia.objects.create(user=self.user, item=self.movie1)

    def test_media_list_filters_by_type(self):
        url = reverse('tracker:media-list', kwargs={'type': MediaType.MOVIE})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertContains(response, 'Movie 1')
        self.assertContains(response, 'Movie 2')
        self.assertNotContains(response, 'Book 1')

    def test_media_list_context_data_anonymous(self):
        url = reverse('tracker:media-list', kwargs={'type': MediaType.MOVIE})
        response = self.client.get(url)

        self.assertEqual(response.context['media_type'], MediaType.MOVIE)
        self.assertNotIn('user_media_ids', response.context)

    def test_media_list_context_data_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('tracker:media-list', kwargs={'type': MediaType.MOVIE})
        response = self.client.get(url)

        self.assertEqual(response.context['media_type'], MediaType.MOVIE)
        self.assertIn('user_media_ids', response.context)
        self.assertIn(self.movie1.id, response.context['user_media_ids'])
        self.assertNotIn(self.movie2.id, response.context['user_media_ids'])


class MediaDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.media = MediaItem.objects.create(title='Test Media', type=MediaType.MOVIE)
        self.user_media = UserMedia.objects.create(user=self.user, item=self.media)

        self.note1 = Note.objects.create(
            user_media=self.user_media,
            title='First title',
            text='First note'
        )
        self.note2 = Note.objects.create(
            user_media=self.user_media,
            title='Second title',
            text='Second note'
        )

    def test_media_detail_anonymous_user(self):
        url = reverse('tracker:media-detail', kwargs={
            'type': self.media.type,
            'pk': self.media.pk
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('user_media', response.context)
        self.assertNotIn('notes', response.context)

    def test_media_detail_authenticated_user_without_media(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.login(username='otheruser', password='testpass')

        url = reverse('tracker:media-detail', kwargs={
            'type': self.media.type,
            'pk': self.media.pk
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['user_media'])
        self.assertNotIn('notes', response.context)

    def test_media_detail_authenticated_user_with_media(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('tracker:media-detail', kwargs={
            'type': self.media.type,
            'pk': self.media.pk
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_media'], self.user_media)
        self.assertIn('notes', response.context)
        self.assertEqual(len(response.context['notes']), 2)

    def test_media_detail_notes_order(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('tracker:media-detail', kwargs={
            'type': self.media.type,
            'pk': self.media.pk
        })
        response = self.client.get(url)

        notes = response.context['notes']
        self.assertTrue(notes[0].created_at >= notes[1].created_at)


class AddMediaToLibraryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.media = MediaItem.objects.create(title='Test Media', type=MediaType.MOVIE)
        self.url = reverse(
            'tracker:media-add',
            kwargs={
                'type': self.media.type,
                'pk': self.media.pk
            }
        )

    def test_add_media_success(self):
        self.client.login(username='testuser', password='testpass')

        self.assertFalse(
            UserMedia.objects.filter(user=self.user, item=self.media).exists()
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserMedia.objects.filter(user=self.user, item=self.media).exists()
        )

    def test_add_media_redirect(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(self.url)
        expected_url = reverse('tracker:media-detail', kwargs={
            'type': self.media.type,
            'pk': self.media.pk
        })

        self.assertRedirects(response, expected_url)

    def test_add_nonexistent_media(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('tracker:media-add', kwargs={'type': 'movie', 'pk': 999})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

