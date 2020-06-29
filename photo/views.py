from django.shortcuts import render,redirect,redirect,HttpResponseRedirect
from django.http import HttpResponseForbidden,HttpResponse
from urllib.parse import urlparse

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.contrib import messages

from .models import Photo

class PhotoList(ListView):
    model = Photo
    template_name_suffix='_list'
    
    
class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url ='/'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields =['text','image']
    template_name_suffix='_update'
    success_url='/'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request,"%s님 수정권한 없습니다" % request.user.username)
            return redirect('/')
        else:
            return super(PhotoUpdate,self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    fields =['text','image']
    template_name_suffix='_delete'
    success_url='/'

    def dispatch(self, request, *args, **kwargs):
        object=self.get_object()
        if object.author != request.user: #object.author > User모델로 넘어감 request.user > User모델로 넘어감
            messages.warning(request,"삭제권한 없습니다")
            return redirect('/')
        else:
                
            return super(PhotoDelete,self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix ='_detail'
    
    

class PhotoLike(View):
    
    def get(self, request, *args, **kwargs): #kwargs ['photo_id':3]
       
        if not request.user.is_authenticated:
            # return HttpResponseForbidden()
            return HttpResponse('로그인 해주세요')
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            
            
            #바로 직전 화면으로 보내는 테크닉
            referer_url = request.META.get('HTTP_REFERER') # referer_url =http://127.0.0.1:8000/ or http://127.0.0.1:8000/detail/3/                                                  
            path = urlparse(referer_url).path # path='/' or /detail/3/
            print(referer_url, path)
            return HttpResponseRedirect(path)
            
            
class PhotoFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo =Photo.objects.get(pk=photo_id)
                user = request.user
                
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                    
                else:
                    photo.favorite.add(user)
            return HttpResponseRedirect('/')

class PhotoLikeList(ListView):
    model =Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList,self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.like_post.all()
        return queryset
    
    
class PhotoFavoriteList(ListView):
    model =Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList,self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset