from django.urls import path
from .views import PhotoCreate,PhotoDelete,PhotoUpdate,PhotoList,PhotoDetail
from .views import *
from django.http import HttpResponse





def test(request):
    return HttpResponse('test.hi')

app_name = "photo"

urlpatterns=[
    
    path("create/", PhotoCreate.as_view(), name='create'),
    
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('favorite/<int:photo_id>/', PhotoFavorite.as_view(), name='favorite'),
    
    path("like/", PhotoLikeList.as_view(), name='like_list'),
    path('favorite/', PhotoFavoriteList.as_view(), name='favorite_list'),
    
    path("delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path("detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path('', PhotoList.as_view(), name='index'),
    
]



from django.conf import settings
from django.conf.urls.static import static 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)