from rest_framework import serializers
from .models import Post, Comment
import boto3
from config import settings
from botocore.exceptions import ClientError

def is_image(image):
    file_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = image.name.split('.')[-1].lower()
    
    if file_extension not in file_extensions:
        return False
    return True

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

    # 이미지 유효성 검사 함수
    def is_image(image):
        # 이미지 유효성 검사 로직
        return True

    # 이미지 업로드 함수
    def save_image(image):
        try:
            # s3 client 생성
            s3 = boto3.client('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_REGION)

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_path = image.name
            s3.upload_fileobj(image, bucket_name, file_path)
            
            s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
            return s3_url
        except:
            print("s3 upload error")
            return None     

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        
        fields = "__all__"