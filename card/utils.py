from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

secret_key = b'your-secret-key-32' 
iv = b'initialvector123'  

class DecryptDataView(APIView):
    def post(self, request, *args, **kwargs):
        encrypted_data = request.data.get('data')

        if not encrypted_data:
            return JsonResponse({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cipher = AES.new(secret_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(b64decode(encrypted_data)), AES.block_size)
            return JsonResponse({'data': decrypted_data.decode('utf-8')}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
