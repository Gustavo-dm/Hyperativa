from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Cartao, LoteCartoes, CustomUser


class UploadCartaoFileViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('cartao_upload')

    def test_upload_file_success(self):
        file_content = (
            "DESAFIO-HYPERATIVA           20180524LOTE0001000010\n"
            "C2     4456897999999999\n"
            "C1     4456897922969999\n"
            "LOTE0001000010"
        )
        file = SimpleUploadedFile(
            "test_file.txt", file_content.encode(), content_type="text/plain")

        response = self.client.post(
            self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cartao.objects.count(), 2)
        self.assertEqual(LoteCartoes.objects.count(), 1)

    def test_upload_file_without_file(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CartaoCreateViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpassword',
            username='testuser'
            )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('cartao_create')

    def test_create_cartao_success(self):
        data = {
            'numero': '4456897999999999',
            'lote': '0001000010'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cartao.objects.count(), 1)

    def test_create_cartao_invalid(self):
        data = {
            'numero': '4456897',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CartaoListViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpassword',
            username='testuser'
            )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('cartao_list')
        Cartao.objects.create(numero='4456897999999999', lote='0001000010')

    def test_list_cartao(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CartaoSearchViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpassword',
            username='testuser'
            )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('search_cartao', kwargs={
                           'numero': '4456897999999999'})
        self.cartao = Cartao.objects.create(
            numero='4456897999999999', lote='0001000010')

    def test_search_cartao_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': self.cartao.id})

    def test_search_cartao_not_found(self):
        url = reverse('search_cartao', kwargs={'numero': '0000000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Cartão não encontrado'})
