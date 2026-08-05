from typing import List, Dict, Any
from models import Issue
from config_loader import AppConfig

class IssueEvaluator:
    """Dynamic Scoring Engine weighted against the user's custom tech stack."""

    def evaluate_issues(self, raw_issues: List[Dict[str, Any]], config: AppConfig) -> List[Issue]:
        evaluated_issues = []
        user_stack = [s.lower() for s in config.tech_stack]

        for item in raw_issues:
            text_content = f"{item.get('title', '')} {item.get('description', '')}".lower()
            
            # 1. Dynamic Tech Stack Match (Max 40 pts)
            matched_tech = []
            for tech in user_stack:
                if tech in text_content:
                    matched_tech.append(tech.capitalize())
            
            stack_score = min(40, len(matched_tech) * 15 + 10) if matched_tech else 10

            # 2. Issue Clarity (Max 30 pts)
            clarity_score = 10
            if len(item.get("description", "")) > 300:
                clarity_score += 10
            if len(item.get("description", "")) > 600:
                clarity_score += 5
            
            clarity_keywords = ["steps to reproduce", "expected behavior", "acceptance criteria", "code", "###", "```"]
            if any(kw in text_content for kw in clarity_keywords):
                clarity_score += 5

            # 3. Setup Difficulty & Beginner Labels (Max 20 pts)
            setup_score = 5
            labels = [l.lower() for l in item.get("labels", [])]
            beginner_labels = ["good first issue", "easy", "beginner", "help wanted"]
            if any(lbl in labels for lbl in beginner_labels):
                setup_score += 10
            
            setup_keywords = ["contributing", "setup", "docker", "environment", "simple"]
            if any(kw in text_content for kw in setup_keywords):
                setup_score += 5

            # 4. Activity (Max 10 pts)
            comments = item.get("comments_count", 0)
            activity_score = 10 if 0 < comments <= 5 else 5

            total_score = min(100, stack_score + clarity_score + setup_score + activity_score)

            issue_obj = Issue(
                id=str(item.get("id")),
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("description", ""),
                repository=item.get("repository", ""),
                labels=item.get("labels", []),
                tech_stack=matched_tech if matched_tech else ["General Tech"],
                score=total_score,
                created_at=item.get("created_at", ""),
                comments_count=comments
            )
            
            if total_score >= config.min_score_threshold:
                evaluated_issues.append(issue_obj)

        # Rerank by score descending
        evaluated_issues.sort(key=lambda x: x.score, reverse=True)
        return evaluated_issues
