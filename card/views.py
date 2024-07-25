from datetime import datetime
import re
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cartao, LoteCartoes
from .serializers import (CartaoSerializer, CartaoCreateSerializer,
                          UploadCartaoFileSerializer, LoteCartoesSerializer,
                          CartaoSearchSerializer)
from logs.models import LogRequest
import logging

logger = logging.getLogger(__name__)


def log_request(user, endpoint, method, request_body='', response_body=''):
    log = LogRequest(
        user=user,
        endpoint=endpoint,
        method=method,
        request_body=request_body,
        response_body=response_body,
    )
    log.save()


@extend_schema_view(
    post=extend_schema(tags=['Cartão']),
    get=extend_schema(tags=['Cartão'])
)
class UploadCartaoFileView(APIView):
    parser_classes = [MultiPartParser]
    serializer_class = UploadCartaoFileSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            log_request(request.user, request.path, request.method, str(
                request.data), '{"error": "Nenhum arquivo fornecido"}')
            return Response(
                {'error': 'Nenhum arquivo fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lote = None
        cartoes_validos = set()

        try:
            for i, line in enumerate(file):
                decoded_line = line.decode('utf-8').rstrip()
                if i == 0:
                    nome = decoded_line[0:29].strip()
                    data = decoded_line[29:37].strip()
                    data_formatada = datetime.strptime(
                        data, '%Y%m%d').strftime('%d-%m-%Y')
                    lote = decoded_line[41:45].strip()
                else:
                    numero_cartao = decoded_line[7:27].strip()
                    if re.match(r'^\d{16}$', numero_cartao):
                        cartoes_validos.add(numero_cartao)

            if not lote:
                log_request(request.user, request.path, request.method, str(
                    request.data), '{"error": "Lote não encontrado no arquivo"}')
                return Response({
                                'error': 'Lote não encontrado no arquivo'},
                                status=status.HTTP_400_BAD_REQUEST
                                )

            cartoes_existentes = set(Cartao.objects.filter(
                numero__in=cartoes_validos).values_list('numero', flat=True))
            cartoes_a_inserir = cartoes_validos - cartoes_existentes

            if not cartoes_a_inserir:
                log_request(request.user, request.path, request.method, str(
                    request.data), '{"error": "Todos os cartões no arquivo já estão cadastrados ou são inválidos."}')
                return Response(
                    {'error': 'Todos os cartões no arquivo já estão cadastrados ou são inválidos.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for numero_cartao in cartoes_a_inserir:
                Cartao.objects.create(numero=numero_cartao, lote=lote)

            lote_cartoes = LoteCartoes.objects.create(
                usuario=request.user,
                quantidade=len(cartoes_a_inserir),
                nome=nome,
                data=data_formatada,
                numero=lote
            )

            serializer = LoteCartoesSerializer(lote_cartoes)
            log_request(request.user, request.path, request.method,
                        str(request.data), serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            log_request(request.user, request.path, request.method,
                        str(request.data), f'{{"error": "{str(e)}"}}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    post=extend_schema(tags=['Cartão']),
    get=extend_schema(tags=['Cartão'])
)
class CartaoCreateView(generics.CreateAPIView):
    queryset = Cartao.objects.all()
    serializer_class = CartaoCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        log_request(request.user, request.path, request.method,
                    str(request.data), response.data)
        return response


@extend_schema_view(
    post=extend_schema(tags=['Cartão']),
    get=extend_schema(tags=['Cartão'])
)
class CartaoListView(generics.ListAPIView):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        log_request(request.user, request.path,
                    request.method, '', response.data)
        return response


@extend_schema_view(
    post=extend_schema(tags=['Cartão']),
    get=extend_schema(tags=['Cartão'])
)
class CartaoSearchView(APIView):
    serializer_class = CartaoSearchSerializer

    def get(self, request, *args, **kwargs):
        numero = kwargs.get('numero')
        if not numero:
            log_request(request.user, request.path, request.method, str(
                request.data), '{"error": "Número do cartão não fornecido"}')
            return Response(
                {'error': 'Número do cartão não fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cartao = Cartao.objects.get(numero=numero)
            log_request(request.user, request.path, request.method,
                        str(request.data), f'{{"id": "{cartao.id}"}}')
            return Response({'id': cartao.id}, status=status.HTTP_200_OK)
        except Cartao.DoesNotExist:
            log_request(request.user, request.path, request.method, str(
                request.data), '{"error": "Cartão não encontrado"}')
            return Response(
                {'error': 'Cartão não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
