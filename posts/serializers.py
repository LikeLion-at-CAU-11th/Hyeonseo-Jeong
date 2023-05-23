from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        # 어떤 field를 serialize 할 것인가?
        # "__all__"은 모든 field를 직렬화하겠다!
        fields = "__all__" 

        # 만약 특정 field만 직렬화하고 싶다면..
        # fields = ['writer', 'content']

        # 제외할 field를 지정할 수도 있다.
        # exclude = ['id']

        # create, update, delete는 안 되고,
        # read만 되는 field를 선언할 수도 있다. (이름이 바뀌면 안 되는 경우)
        # read_only_fields = ['writer']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
