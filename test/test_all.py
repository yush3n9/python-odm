import unittest

from pymodm import connect
from pymodm.connection import _get_db

from src.entity import User, Post, Comment


class TestAll(unittest.TestCase):

    def setUp(self):
        connect("mongodb://localhost:27017/unittest")
        self.u1 = User('Tommy')
        self.u2 = User('Jack')

        self.p1 = Post(self.u1)
        # p2 has no comments, so save now!
        self.p2 = Post(self.u1).save()
        self.p3 = Post(self.u2)

        self.c1 = Comment(self.p1).save()
        self.c2 = Comment(self.p1).save()
        self.c3 = Comment(self.p1).save()
        self.c4 = Comment(self.p3).save()

    def test_func(self):
        self.assertEqual(len(self.u1.get_posts()), 2)
        self.assertEqual(len(self.u2.get_posts()), 1)
        self.assertEqual(len(self.p1.get_comments()), 3)
        self.assertEqual(len(self.p2.get_comments()), 0)
        self.assertEqual(len(self.p3.get_comments()), 1)

    def test_cascade(self):
        self.assertEqual(self.p1.ref_user._id, self.u1._id)
        self.assertEqual(self.p1.ref_user.username, 'Tommy')
        self.assertEqual(self.p2.ref_user.username, 'Tommy')
        self.assertEqual(self.p3.ref_user.username, 'Jack')
        self.assertEqual(self.p2.ref_user._id, self.u1._id)
        self.assertEqual(self.p3.ref_user._id, self.u2._id)
        self.assertEqual(self.c1.ref_post._id, self.p1._id)
        self.assertEqual(self.c2.ref_post._id, self.p1._id)
        self.assertEqual(self.c3.ref_post._id, self.p1._id)
        self.assertEqual(self.c4.ref_post._id, self.p3._id)

    def tearDown(self):
        _get_db().client.drop_database('unittest')


if __name__ == '__main__':
    unittest.main()
