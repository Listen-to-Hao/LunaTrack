from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import MenstrualRecord
from .forms import MenstrualRecordForm

SYMPTOM_CHOICES = [
    ('breast_tenderness', 'Breast Tenderness'),
    ('mood_swings', 'Mood Swings'),
    ('headache', 'Headache'),
    ('bloating', 'Bloating'),
    ('fatigue', 'Fatigue'),
    ('nausea', 'Nausea'),
    ('other', 'Other')
]

def record_list(request):
    records = MenstrualRecord.objects.filter(user=request.user).order_by("-start_date")
    form = MenstrualRecordForm()
    return render(request, "records/record_list.html", {"records": records, "symptom_choices": SYMPTOM_CHOICES})

def add_record(request):
    if request.method == "POST":
        form = MenstrualRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return JsonResponse({"success": True, "message": "Record added successfully"})
    return JsonResponse({"success": False, "message": "Invalid data"}, status=400)

def edit_record(request, pk):
    record = get_object_or_404(MenstrualRecord, pk=pk, user=request.user)

    if request.method == "POST":
        form = MenstrualRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Record updated successfully"})
    
    return JsonResponse({
        "success": True,
        "start_date": record.start_date.strftime('%Y-%m-%d'),
        "end_date": record.end_date.strftime('%Y-%m-%d'),
        "blood_volume": record.blood_volume,
        "clotting": record.clotting,
        "mood_swings": record.mood_swings,
        "stress_level": record.stress_level,
        "symptom_description": record.symptom_description,
        "pre_menstrual_symptoms": record.pre_menstrual_symptoms,
        "menstrual_symptoms": record.menstrual_symptoms,
        "post_menstrual_symptoms": record.post_menstrual_symptoms
    })

def delete_record(request, pk):
    try:
        record = get_object_or_404(MenstrualRecord, pk=pk, user=request.user)
        record.delete()
        return JsonResponse({"success": True, "message": "Record deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
