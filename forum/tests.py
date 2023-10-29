import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment 

class CrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='Test Content')
        self.comment = Comment.objects.create(user=self.user, post=self.post, text='Test Comment') 

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.text, 'Test Content')
        self.assertEqual(self.post.user, self.user)

    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Test Comment')
        self.assertEqual(comment.text, 'Test Comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

    def test_post_edit(self):
        self.post.title = 'Updated Post'
        self.post.save()
        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.title, 'Updated Post')

    def test_comment_edit(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Test Comment')
        comment.text = 'Updated Comment'
        comment.save()
        updated_comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(updated_comment.text, 'Updated Comment')

    def test_post_deletion(self):
        post_id = self.post.id
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post_id)

    def test_comment_deletion(self):
        comment_id = self.comment.pk
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment_id)

    def test_post_user_relation(self):
        self.assertEqual(self.post.user, self.user)

    def test_comment_user_relation(self):
        self.assertEqual(self.comment.user, self.user)

    def test_comment_post_relation(self):
        self.assertEqual(self.comment.post, self.post)

if __name__ == '__main__':
    unittest.main()
