from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from records.models import MenstrualRecord
from analyse.views import analyze_cycle_regularity, analyze_blood_volume, analyze_symptoms, analyze_weight_trend, analyze_mood_stress
import json

User = get_user_model()

class MenstrualAnalysisTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creating a test user and two menstrual records for the test case
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.record1 = MenstrualRecord.objects.create(user=cls.user, start_date=now().date() - timedelta(days=30), blood_volume='medium', weight=50, stress_level='low', pre_menstrual_symptoms=['fatigue'], menstrual_symptoms=['cramps'], post_menstrual_symptoms=[])
        cls.record2 = MenstrualRecord.objects.create(user=cls.user, start_date=now().date() - timedelta(days=60), blood_volume='heavy', weight=52, stress_level='medium', pre_menstrual_symptoms=[], menstrual_symptoms=['headache'], post_menstrual_symptoms=['mood_swings'])

    def test_analyze_cycle_regularity(self):
        # Test to check cycle regularity analysis
        result = analyze_cycle_regularity(self.user)
        self.assertIn('avg_cycle', result)  # Ensure the result includes the average cycle
        self.assertIn('std_cycle', result)  # Ensure the result includes the standard deviation of the cycle
        self.assertIn('suggestions', result)  # Ensure the result includes analysis suggestions

    def test_analyze_blood_volume(self):
        # Test to check blood volume analysis
        result = analyze_blood_volume(self.user)
        self.assertIn('blood_values', result)  # Ensure the result includes blood volume values
        self.assertIn('suggestions', result)  # Ensure the result includes suggestions based on the blood volume

    def test_analyze_symptoms(self):
        # Test to check symptom trends analysis
        result = analyze_symptoms(self.user)
        self.assertIn('symptom_trends', result)  # Ensure the result includes symptom trends
        self.assertIn('suggestions', result)  # Ensure the result includes suggestions based on symptoms

    def test_analyze_weight_trend(self):
        # Test to check weight trend analysis
        result = analyze_weight_trend(self.user)
        self.assertIn('weight_data', result)  # Ensure the result includes weight data
        self.assertIn('suggestions', result)  # Ensure the result includes suggestions based on the weight trend

    def test_analyze_mood_stress(self):
        # Test to check mood and stress level analysis
        result = analyze_mood_stress(self.user)
        self.assertIn('stress_levels', result)  # Ensure the result includes stress level data
        self.assertIn('suggestions', result)  # Ensure the result includes suggestions based on mood and stress levels

    def test_analyse_view(self):
        # Test to check the analysis view response
        client = Client()  # Create a test client instance
        client.login(username='testuser', password='testpassword')  # Log in as the test user
        response = client.get('/analyse/')  # Send GET request to the analysis view
        self.assertEqual(response.status_code, 200)  # Ensure the response status is 200 (OK)
        self.assertIn('analysis_data', response.context)  # Ensure the context contains analysis data
        self.assertIn('symptom_recommendations', response.context)  # Ensure the context contains symptom recommendations
        self.assertIsInstance(response.context['analysis_data'], dict)  # Ensure 'analysis_data' is a dictionary
