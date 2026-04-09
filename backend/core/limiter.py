from datetime import datetime, timezone

# Simple in-memory storage for the demo
user_last_job_time = {}

def check_rate_limit(user_id: int, seconds: int = 60):
    now = datetime.now(timezone.utc)
    if user_id in user_last_job_time:
        elapsed = (now - user_last_job_time[user_id]).total_seconds()
        if elapsed < seconds:
            return False, int(seconds - elapsed)
    
    user_last_job_time[user_id] = now
    return True, 0