from django.test import TestCase
from .scoring import score_tasks

class ScoringAlgorithmTests(TestCase):

    def test_overdue_task_has_high_urgency(self):
        """Overdue tasks must receive maximum urgency and proper explanation."""
        tasks = [{
            "id": "t1",
            "title": "Past Due Task",
            "due_date": "2020-01-01",   # long overdue
            "importance": 5,
            "estimated_hours": 2,
            "dependencies": []
        }]
        scored = score_tasks(tasks)

        # Explanation should mention overdue OR past due
        explanation = scored[0]["explanation"].lower()
        self.assertTrue(
            "past" in explanation or "overdue" in explanation,
            msg=f"Expected 'past' or 'overdue' in explanation, got: {explanation}"
        )

    def test_high_importance_scores_higher(self):
        """Important tasks (importance=10) should outrank lower ones."""
        tasks = [
            {
                "id": "t1",
                "title": "Low Importance Task",
                "due_date": None,
                "importance": 3,
                "estimated_hours": 2,
                "dependencies": []
            },
            {
                "id": "t2",
                "title": "High Importance Task",
                "due_date": None,
                "importance": 10,
                "estimated_hours": 2,
                "dependencies": []
            }
        ]
        scored = score_tasks(tasks)
        scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)

        # Expect high-importance task first
        self.assertEqual(scored_sorted[0]["id"], "t2")

    def test_low_effort_gets_quick_win_bonus(self):
        """Low-effort tasks should be prioritized over high-effort ones."""
        tasks = [
            {
                "id": "t1",
                "title": "Large Task",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 12,
                "dependencies": []
            },
            {
                "id": "t2",
                "title": "Quick Task",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 1,
                "dependencies": []
            }
        ]

        scored = score_tasks(tasks)
        scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)

        self.assertEqual(scored_sorted[0]["id"], "t2")  # quick task wins

    def test_dependency_increases_priority(self):
        """Tasks with more dependencies should rank higher."""
        tasks = [
            {
                "id": "t1",
                "title": "Simple Task",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": []
            },
            {
                "id": "t2",
                "title": "Blocking Task",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": ["t1", "t3", "t4"]  # more dependencies
            }
        ]

        scored = score_tasks(tasks)
        scored_sorted = sorted(scored, key=lambda x: x["score"], reverse=True)

        self.assertEqual(scored_sorted[0]["id"], "t2")

    def test_circular_dependency_detected(self):
        """Cycle detection must assign score=0 and include explanation."""
        tasks = [
            {
                "id": "a",
                "title": "Task A",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": ["b"]
            },
            {
                "id": "b",
                "title": "Task B",
                "due_date": None,
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": ["a"]  # creates cycle
            }
        ]

        scored = score_tasks(tasks)
        zero_scores = [t for t in scored if t["score"] == 0]

        self.assertEqual(len(zero_scores), 2)  # both are part of the cycle
        self.assertIn("circular", zero_scores[0]["explanation"].lower())
