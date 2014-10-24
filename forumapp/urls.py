from django.conf.urls import patterns, url
from forumapp import views


urlpatterns = patterns('',

    # ex: /polls/

    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    # ex: /polls/5/


    url(r'^general_thread_list/view_myposts/(?P<thread_id>\d+)/$', views.detail, name='detail'),

    url(r'^general_thread_list/trashbin/(?P<thread_id>\d+)/$', views.detail, name='detail'),

    url(r'^general_thread_list/(?P<thread_id>\d+)/$', views.detail, name='detail'),
   

    url(r'^register/$',views.register,name = 'register'),
    url(r'^creation/$',views.creation,name = 'creation'),

    url(r'^general_thread_list/$',views.thread_list,name = 'thread_list'),
    url(r'^general_thread_list/view_myposts/$',views.view_myposts,name = 'view_myposts'),
    url(r'^general_thread_list/view_myposts/$',views.move_to_trash,name = 'move_to_trash'),

    url(r'^general_thread_list/trashbin/$',views.show_trash,name = 'move_to_trash'),

    url(r'^login/$',views.alogin,name = 'alogin'),
    url(r'^logout/$',views.alogout,name = 'alogouwt'),
    url(r'^create_post/$',views.creation,name = 'alogout'),
    url(r'^register_test/$',views.register,name = 'alogout'),
    url(r'^search/$', views.search_thread, name='search'),

	url(r'^general_review_list/$',views.review_list,name = 'review_list'),
	
	
    url(r'^whiteboard/$',views.whiteboard,name = 'whiteboard'),
    url(r'^white/$',views.white,name = 'white'),

    url(r'^profile/(.+)/$', views.profile,name="profile"),

    url(r'^course/(?P<subject_id>\d+)/$',views.course_review,name='review'),
    url(r'^search_review/$', views.search_review, name='search_review'),
    url(r'^create_review/$',views.create_review,name = 'create_review'),
)

