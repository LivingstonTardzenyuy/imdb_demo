from rest_framework import serializers 
from watchlist_app.models import WatchList, StreamPlatForm, Reviews


class ReviewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reviews 
        fields = "__all__"


class WatchListSerializers(serializers.ModelSerializer):

    length_name = serializers.SerializerMethodField()           #allows me to define a field 
    # platform = serializers.CharField(source='platform.name', read_only = True)
    class Meta:
        model = WatchList 
        fields = "__all__"

    def get_length_name(self, object):
        length = len(object.title)
        return length

    
    def validate(self, data):
        if data['title'] == data['description']:
            return serializers.ValidationError("the title and description should be different")
        else:
            return data 


class StreamPlatFormSerializers(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializers(many = True, read_only = True)
    
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only = True, view_name='watchlist-details')
    class Meta:
        model = StreamPlatForm
        fields = "__all__"