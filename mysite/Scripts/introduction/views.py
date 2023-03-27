from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

def persons_inform(request):
    if request.method == "GET":
        return JsonResponse({
            'status': 200,
            'success': True,
            'message': '메시지 전달 성공!',
            'data': [{
            'name': '정현서',
            'age': 26,
            'major': 'Computer Science and Engineering',
        },

        {
            'name': '양희철',
            'age': 24,
            'major': 'Industrial Security',        
        }]
        })