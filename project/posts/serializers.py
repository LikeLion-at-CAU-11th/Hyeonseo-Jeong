from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post        # 어떤 모델을 시리얼라이즈 할 것인가?

        fields = "__all__"  # 모델에서 어떤 필드를 가져올 것인가?

    # 추가적으로,
        # 가져올 필드를 지정할 수 있다.
        # fields = ['writer', 'content']

        # 제외할 필드를 지정할 수 있다.
        # exclude = ['id']

        # read만 가능한 필드를 지정할 수 있다. (변경되지 않아야 하는 필드)
        # read_only_fields = ['writer']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        
        fields = "__all__"