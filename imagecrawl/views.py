from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from imagecrawl.models import *
from imagecrawl import serializers
import utils
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.utils import timezone

#Template views

def home(request):
	response = render(request,'imagecrawl/home.html')
	return response

# rest views.
class CrawlViewSet(viewsets.ModelViewSet):
    http_method_names = ['post',"get","patch","delete"]
    queryset = Crawl.objects.all()
    serializer_class = serializers.CrawlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    	m = utils.Crawler(request.data['url'])
    	crawl_obj = Crawl.objects.create(url = request.data['url'],uid = m.id,started_time = timezone.now())
    	final_list = m.crawl(depth = 5)
        objects = [Image(crawl = crawl_obj,image_url = item[1]) for item in final_list]
        Image.objects.bulk_create(objects)
        crawl_obj.finished_time = timezone.now()
        crawl_obj.save()
        serialized_crawl = serializers.CrawlSerializer(crawl_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serialized_crawl.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Crawl.objects.all().order_by('-id')
        return queryset


class ImageViewSet(viewsets.ModelViewSet):
    http_method_names = ["get","delete"]
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Image.objects.all()
        crawl = self.request.query_params.get('crawl', None)
        if crawl is not None:
            queryset = queryset.filter(crawl_id=crawl)
        return queryset
