#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView

from wenhu.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['moments_num'] = user.publisher.filter(reply=False).count()  # 'publisher'为News表中的related_name
        context['article_num'] = user.author.filter(status='P').count()  # 只算已发表的文章
        context['comment_num'] = user.publisher.filter(reply=True).count() + user.comment_comments.all().count()  # 动态+文章的评论数
        context['question_num'] = user.q_author.all().count()
        context['answer_num'] = user.a_author.all().count()

        # 互动数 = 动态点赞数+问答点赞数+评论数+私信用户数(双方都有发送和接收私信)
        tmp = set()
        # 我发送私信给了多少不同的用户
        sent_num = user.sent_messages.all()
        for s in sent_num:
            tmp.add(s.recipient.username)
        # 我接收的所有私信来自多少不同的用户
        received_num = user.received_messages.all()
        for r in received_num:
            tmp.add(r.sender.username)

        context['interaction_num'] = user.liked_news.all().count() + user.qa_vote.all().count() + \
                                     context['comment_num'] + len(tmp)

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """用户只能更新自己的信息"""

    model = User
    fields = ['nickname', 'email', 'picture', 'introduction', 'job_title', 'location',
              'personal_url', 'weibo', 'zhihu', 'github', 'linkedin']

    template_name = 'users/user_form.html'

    def get_success_url(self):
        """更新成功后跳转到用户自己的页面"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
