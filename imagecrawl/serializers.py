from rest_framework import serializers
from imagecrawl.models import *
from collections import OrderedDict


class ChoicesField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        """init."""
        self._choices = OrderedDict(choices)
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        """Used while retrieving value for the field."""
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in self._choices:
            if self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))

class CrawlSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    status = ChoicesField(Crawl.STATUS_CHOICES)
    
    def get_status(self,obj):
        return obj.get_status_display()
    
    class Meta:
        model = Crawl
        fields = ('id','uid','created_time','started_time','error','url','description','status','finished_time')
        read_only_fields = ('id','uid','created_time','started_time','error')


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()
    
    def get_status(self,obj):
        return obj.get_status_display()
    
    class Meta:
        model = Image
        fields = ('image_url','created_time','crawl')
        read_only_fields = ('image_url','created_time','crawl')
