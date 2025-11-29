from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scoring import score_tasks
import json

@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart_balance")

    # Compute scores
    scored = score_tasks(tasks)

    # Sort highest → lowest
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)

    return Response({"tasks": scored})


@api_view(["GET"])
def suggest_tasks(request):
    tasks_json = request.GET.get("tasks", "[]")
    strategy = request.GET.get("strategy", "smart_balance")

    try:
        tasks = json.loads(tasks_json)
    except:
        return Response({"error": "Invalid tasks JSON"}, status=400)

    scored = score_tasks(tasks)
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)

    top3 = scored[:3]
    suggestions = [
        {"task": t, "why": t["explanation"]}
        for t in top3
    ]

    return Response({"suggestions": suggestions})
