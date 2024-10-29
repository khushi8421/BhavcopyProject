# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import EquityRecord

# class EquityRecordTests(APITestCase):

#     def setUp(self):
#         self.equity_record = EquityRecord.objects.create(
#             name="Test Equity",
#             symbol="TEQ",
#             price=100.50,
#             volume=1000
#         )

#     def test_list_equity_records(self):
#         response = self.client.get(reverse('equity-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

