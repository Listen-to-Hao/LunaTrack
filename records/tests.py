from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenstrualRecord
from .forms import MenstrualRecordForm

class MenstrualRecordViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_record_list_view(self):
        url = reverse('record_list')  # Use the appropriate name for your view
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/record_list.html')
        self.assertIn('records', response.context)
        self.assertIn('symptom_choices', response.context)

    def test_add_record_view(self):
        url = reverse('add_record')  # Use the appropriate name for your view
        data = {
            'start_date': '2025-03-01',
            'end_date': '2025-03-05',
            'blood_volume': 5,
            'clotting': 'None',
            'mood_swings': 'Yes',
            'stress_level': 3,
            'symptom_description': 'Mild pain',
            'pre_menstrual_symptoms': 'Yes',
            'menstrual_symptoms': 'Yes',
            'post_menstrual_symptoms': 'No',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content), {'success': True, 'message': 'Record added successfully'})

    def test_edit_record_view(self):
        record = MenstrualRecord.objects.create(
            user=self.user,
            start_date='2025-03-01',
            end_date='2025-03-05',
            blood_volume=5,
            clotting='None',
            mood_swings='Yes',
            stress_level=3,
            symptom_description='Mild pain',
            pre_menstrual_symptoms='Yes',
            menstrual_symptoms='Yes',
            post_menstrual_symptoms='No'
        )
        url = reverse('edit_record', args=[record.pk])  # Use the appropriate name for your view
        data = {
            'start_date': '2025-03-01',
            'end_date': '2025-03-05',
            'blood_volume': 5,
            'clotting': 'None',
            'mood_swings': 'Yes',
            'stress_level': 3,
            'symptom_description': 'Updated description',
            'pre_menstrual_symptoms': 'Yes',
            'menstrual_symptoms': 'Yes',
            'post_menstrual_symptoms': 'No',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content), {'success': True, 'message': 'Record updated successfully'})

    def test_delete_record_view(self):
        record = MenstrualRecord.objects.create(
            user=self.user,
            start_date='2025-03-01',
            end_date='2025-03-05',
            blood_volume=5,
            clotting='None',
            mood_swings='Yes',
            stress_level=3,
            symptom_description='Mild pain',
            pre_menstrual_symptoms='Yes',
            menstrual_symptoms='Yes',
            post_menstrual_symptoms='No'
        )
        url = reverse('delete_record', args=[record.pk])  # Use the appropriate name for your view
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content), {'success': True, 'message': 'Record deleted successfully'})
        self.assertEqual(MenstrualRecord.objects.count(), 0)

