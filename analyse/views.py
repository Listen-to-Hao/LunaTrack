from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
import numpy as np
from records.models import MenstrualRecord
import json
from googleapiclient.discovery import build

def search_symptoms(keyword):
    """调用Google Search API获取健康建议"""
    api_key = "AIzaSyBATyhquphIGMpRAlJtYUZZfzI9IDDdQUs"  # 替换为你的API Key
    search_engine_id = "f5688f439efbf455f"  # 替换为你的Search Engine ID

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(
            q=keyword,
            cx=search_engine_id,
            num=3,  # 限制每次请求返回3条结果
        ).execute()
        print(f"API Response for '{keyword}':", res)  # 打印 API 响应
        return res.get("items", [])
    except Exception as e:
        print(f"❌ API Error for '{keyword}':", e)  # 打印错误信息
        return []

# 🔹 计算月经周期规律性
def analyze_cycle_regularity(user):
    """分析用户的月经周期规律性，并提供建议"""
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    if len(records) < 2:
        return {"error": "Not enough data to analyze cycle regularity. Please log more cycles."}

    cycle_lengths = [(records[i].start_date - records[i - 1].start_date).days for i in range(1, len(records))]
    avg_cycle = np.mean(cycle_lengths)
    std_cycle = np.std(cycle_lengths)
    next_period_estimate = records.last().start_date + timedelta(days=int(avg_cycle))

    # **异常情况检测 & 建议**
    suggestions = []
    if std_cycle > 5:
        suggestions.append("Your cycle length varies significantly. Consider tracking stress, diet, and sleep patterns.")
    if avg_cycle < 21:
        suggestions.append("Your cycles are short (<21 days). This might indicate hormonal imbalances.")
    if avg_cycle > 40:
        suggestions.append("Your cycles are long (>40 days). If persistent, consult a doctor.")

    return {
        "cycle_lengths": cycle_lengths,
        "avg_cycle": avg_cycle,
        "std_cycle": std_cycle,
        "next_period_estimate": next_period_estimate.strftime("%Y-%m-%d"),
        "suggestions": suggestions
    }


# 🔹 计算经血量分析
def analyze_blood_volume(user):
    """分析用户的血量变化趋势，并提供建议"""
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    if not records:
        return {"error": "No blood flow data available. Please log your menstrual health information."}

    dates = [record.start_date.strftime("%Y-%m-%d") for record in records]
    blood_values = [1 if record.blood_volume == "light" else (2 if record.blood_volume == "medium" else 3) for record in records]

    # **异常情况检测 & 建议**
    suggestions = []
    if blood_values.count(3) > len(blood_values) * 0.5:
        suggestions.append("Frequent heavy bleeding may indicate uterine fibroids or hormonal imbalances.")
    if blood_values.count(1) > len(blood_values) * 0.5:
        suggestions.append("Consistently light bleeding may indicate low estrogen levels or nutritional deficiencies.")

    return {
        "dates": dates,
        "blood_values": blood_values,
        "suggestions": suggestions
    }


# 🔹 计算症状分析
def analyze_symptoms(user):
    """分析用户的症状变化趋势，并提供建议"""
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    if not records:
        return {"error": "No symptom data available. Please enter your symptoms."}

    symptom_trends = {}
    for record in records:
        for symptom in record.pre_menstrual_symptoms + record.menstrual_symptoms + record.post_menstrual_symptoms:
            if symptom not in symptom_trends:
                symptom_trends[symptom] = 0
            symptom_trends[symptom] += 1

    # **异常情况检测 & 建议**
    suggestions = []
    if symptom_trends.get("fatigue", 0) > 3:
        suggestions.append("Frequent fatigue may be related to anemia or low iron levels.")
    if symptom_trends.get("mood_swings", 0) > 3:
        suggestions.append("Frequent mood swings may indicate hormonal fluctuations or high stress.")
    if symptom_trends.get("headache", 0) > 3:
        suggestions.append("Persistent headaches may be linked to dehydration or hormonal changes.")

    return {
        "symptom_trends": symptom_trends,
        "suggestions": suggestions
    }

# 🔹 计算体重变化趋势
def analyze_weight_trend(user):
    """分析用户的体重变化趋势，并提供建议"""
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    if len(records) < 2:
        return {"error": "Not enough data to analyze weight trends. Please track your weight regularly."}

    dates = [record.start_date.strftime("%Y-%m-%d") for record in records]
    weight_data = [record.weight for record in records]

    # **异常情况检测 & 建议**
    suggestions = []
    if max(weight_data) - min(weight_data) > 5:
        suggestions.append("Significant weight changes may impact menstrual regularity. Consider tracking your diet.")
    if weight_data[-1] < 45:
        suggestions.append("Your weight is quite low. This may impact hormonal balance and menstruation.")

    return {
        "dates": dates,
        "weight_data": weight_data,
        "suggestions": suggestions
    }


# 🔹 计算情绪波动与压力
def analyze_mood_stress(user):
    """分析用户的情绪波动和压力趋势，并提供建议"""
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    if not records:
        return {"error": "No mood data available. Please record your emotional state."}

    dates = [record.start_date.strftime("%Y-%m-%d") for record in records]
    stress_levels = [1 if record.stress_level == "low" else (2 if record.stress_level == "medium" else 3) for record in records]

    # **异常情况检测 & 建议**
    suggestions = []
    if stress_levels.count(3) > len(stress_levels) * 0.5:
        suggestions.append("Frequent high stress levels may impact your cycle. Consider relaxation techniques.")

    return {
        "dates": dates,
        "stress_levels": stress_levels,
        "suggestions": suggestions
    }




def analyse_view(request):
    """渲染分析页面，并提供健康建议"""
    user = request.user
    analysis_data = {
        "cycle_analysis": analyze_cycle_regularity(user),
        "blood_analysis": analyze_blood_volume(user),
        "symptom_analysis": analyze_symptoms(user),
        "weight_analysis": analyze_weight_trend(user),
        "mood_analysis": analyze_mood_stress(user),
    }

    # ✅ 确保每个分析结果都有 `suggestions` 键
    for key, value in analysis_data.items():
        if "suggestions" not in value:
            value["suggestions"] = []  # 确保 suggestions 存在

        # ✅ 预先转换为 JSON 以避免前端解析问题
        if not value.get("error"):
            value["json_data"] = json.dumps(value)
        
    
    # 提取症状数据
    twelve_months_ago = now().date() - timedelta(days=365)
    records = MenstrualRecord.objects.filter(user=user, start_date__gte=twelve_months_ago).order_by("start_date")

    symptom_keywords = set()
    for record in records:
        # 过滤掉 "other"
        symptoms = [
            symptom for symptom in record.pre_menstrual_symptoms + record.menstrual_symptoms + record.post_menstrual_symptoms
            if symptom != "other"
        ]
        symptom_keywords.update(symptoms)
        if record.symptom_description and record.symptom_description.lower() != "other":
            symptom_keywords.add(record.symptom_description)

    # 扩展关键词
    extended_keywords = set()
    for keyword in symptom_keywords:
        extended_keywords.add(keyword)
        if keyword == "headache":
            extended_keywords.add("menstrual headache relief")
        elif keyword == "bloating":
            extended_keywords.add("how to reduce bloating during period")
        elif keyword == "fatigue":
            extended_keywords.add("causes of fatigue during menstruation")
        elif keyword == "nausea":
            extended_keywords.add("nausea during period causes")
        elif keyword == "mood_swings":
            extended_keywords.add("how to manage mood swings during period")

    # 调用 API 获取健康建议
    search_results = []
    for keyword in extended_keywords:
        results = search_symptoms(keyword)
        search_results.extend(results)

    # 去重和过滤
    unique_results = {result["link"]: result for result in search_results}.values()
    filtered_results = [
        result for result in unique_results
        if "menstrual" in result["title"].lower() or "period" in result["title"].lower()
    ]

    return render(request, "analyse/analyse.html", {
        "analysis_data": analysis_data,
        "symptom_recommendations": list(filtered_results)[:5]  # 只返回前5条结果
    })