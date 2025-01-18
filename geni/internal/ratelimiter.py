from collections import deque
import logging
import time

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, limit=1, window=10):
        self.limit = limit
        self.window = window      
        self.remaining = -1  
        self.queue = deque()

    def wait(self):
        """
        Sleep until we are allowed to make another request.
        """
        # If we were told we have remaining calls, don't wait
        while self.remaining <= 0 and len(self.queue) >= self.limit:
            current_time = time.time()
            # Clear expired timestamps
            while self.queue and self.queue[0] <= current_time:
                self.queue.popleft()

            # Sleep if still rate-limited
            if len(self.queue) >= self.limit:
                dt = self.queue[0] - current_time
                logger.info(f"Rate limit reached. Pausing for {dt:.2f} seconds...")
                time.sleep(dt)

    def update(self, headers):
        """
        Update the rate limit settings based on the instructions from reply headers.
        """
        self.limit = headers.get("X-API-Rate-Limit", self.limit)
        self.remaining = headers.get("X-API-Rate-Remaining", 0)
        rate_window = headers.get("X-API-Rate-Window", self.window)

        self.queue.append(time.time() + rate_window)
