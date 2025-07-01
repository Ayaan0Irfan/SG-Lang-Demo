"""
Parallel Processing Module
Async and concurrent execution for LLM operations
"""

import asyncio
import time
from typing import Any, Callable, Coroutine, List

class ParallelProcessor:
    """Handle parallel and async LLM operations"""

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_parallel(self, tasks: List[Coroutine]) -> List[Any]:
        """Execute multiple async tasks in parallel with concurrency control"""
        async def bounded_task(task):
            async with self.semaphore:
                return await task
        bounded_tasks = [bounded_task(task) for task in tasks]
        return await asyncio.gather(*bounded_tasks)

    async def execute_with_timeout(self, task: Coroutine, timeout: float = 30.0) -> Any:
        """Execute task with timeout"""
        try:
            return await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Task timed out after {timeout} seconds")

    async def execute_batch(self, tasks: List[Coroutine], batch_size: int = None) -> List[Any]:
        """Execute tasks in batches to manage memory and API limits"""
        if batch_size is None:
            batch_size = self.max_concurrent
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i : i + batch_size]
            batch_results = await self.execute_parallel(batch)
            results.extend(batch_results)
            if i + batch_size < len(tasks):
                await asyncio.sleep(0.1)
        return results
