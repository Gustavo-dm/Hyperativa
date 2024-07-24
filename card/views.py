from datetime import datetime
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cartao,LoteCartoes
from .serializers import CartaoSerializer, CartaoCreateSerializer,UploadCartaoFileSerializer,LoteCartoesSerializer
from logs.models import LogRequest
import logging

logger = logging.getLogger(__name__)

class UploadCartaoFileView(APIView):
    parser_classes = [MultiPartParser]
    serializer_class = UploadCartaoFileSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Nenhum arquivo fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        num_cartoes = []
        lote = None

        try:
            for i, line in enumerate(file):
                decoded_line = line.decode('utf-8').rstrip()
                if i == 0:
                    nome = decoded_line[0:29].strip()
                    data = decoded_line[29:37].strip()
                    data_formatada = datetime.strptime(data, '%Y%m%d').strftime('%d-%m-%Y')
                    lote = decoded_line[41:45].strip()
                else:
                    numero_cartao = decoded_line[7:27].strip()
                    if len(numero_cartao) > 10:
                        num_cartoes.append(numero_cartao)

            if not lote:
                return Response({'error': 'Lote não encontrado no arquivo'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Cartao objects
            for numero_cartao in num_cartoes:
                Cartao.objects.create(numero=numero_cartao, lote=lote)

            # Create LoteCartoes object
            lote_cartoes = LoteCartoes.objects.create(
                usuario=request.user,
                quantidade=len(num_cartoes),
                nome=nome,
                data=data_formatada,
                numero=lote
            )

            serializer = LoteCartoesSerializer(lote_cartoes)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CartaoCreateView(generics.CreateAPIView):
    queryset = Cartao.objects.all()
    serializer_class = CartaoCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        # Log request
        log = LogRequest(
            user=request.user,
            endpoint=request.path,
            method=request.method,
            request_body=str(request.data),
            response_body='',
        )
        log.save()
        return super().post(request, *args, **kwargs)

class CartaoListView(generics.ListAPIView):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        # Log request
        log = LogRequest(
            user=request.user,
            endpoint=request.path,
            method=request.method,
            request_body='',
            response_body=str(self.get_queryset().values()),
        )
        log.save()
        return super().get(request, *args, **kwargs)
    
    
class CartaoSearchView(APIView):
    def get(self, request, *args, **kwargs):
        numero = kwargs.get('numero')
        if not numero:
            return Response({'error': 'Número do cartão não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cartao = Cartao.objects.get(numero=numero)
            return Response({'id': cartao.id}, status=status.HTTP_200_OK)
        except Cartao.DoesNotExist:
            return Response({'error': 'Cartão não encontrado'}, status=status.HTTP_404_NOT_FOUND)