from django.urls import path
from .views import PhotoCreate,PhotoDelete,PhotoUpdate,PhotoList,PhotoDetail

from django.http import HttpResponse

def test(request):
    return HttpResponse('test.hi')

app_name = "photo"

urlpatterns=[
    
    path("create/", PhotoCreate.as_view(), name='create'),
    path("delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path("detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path('', PhotoList.as_view(), name='index'),
    
]



from django.conf import settings
from django.conf.urls.static import static 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)