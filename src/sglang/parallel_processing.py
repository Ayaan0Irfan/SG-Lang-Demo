"""
Parallel Processing Module
Async and concurrent execution for LLM operations
"""

import asyncio
import time
from typing import List, Dict, Any, Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor


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
            batch = tasks[i:i + batch_size]
            batch_results = await self.execute_parallel(batch)
            results.extend(batch_results)
            
            # Small delay between batches to respect rate limits
            if i + batch_size < len(tasks):
                await asyncio.sleep(0.1)
        
        return results
    
    def measure_execution_time(self, func: Callable) -> Callable:
        """Decorator to measure execution time"""
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if hasattr(result, '__dict__'):
                result.execution_time = execution_time
            elif isinstance(result, dict):
                result['execution_time'] = execution_time
            
            return result
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if hasattr(result, '__dict__'):
                result.execution_time = execution_time
            elif isinstance(result, dict):
                result['execution_time'] = execution_time
            
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    async def retry_with_backoff(self, task: Coroutine, max_retries: int = 3, base_delay: float = 1.0) -> Any:
        """Retry failed tasks with exponential backoff"""
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return await task
            except Exception as e:
                last_exception = e
                if attempt == max_retries:
                    break
                
                delay = base_delay * (2 ** attempt)
                print(f"[!] Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                await asyncio.sleep(delay)
        
        raise last_exception
    
    async def execute_with_fallback(self, primary_task: Coroutine, fallback_task: Coroutine) -> Any:
        """Execute primary task with fallback if it fails"""
        try:
            return await primary_task
        except Exception as e:
            print(f"[!] Primary task failed: {e}. Trying fallback...")
            return await fallback_task
    
    def create_task_pool(self, task_generator: Callable, inputs: List[Any]) -> List[Coroutine]:
        """Create a pool of tasks from inputs"""
        return [task_generator(input_item) for input_item in inputs]
    
    async def progress_tracker(self, tasks: List[Coroutine], description: str = "Processing") -> List[Any]:
        """Execute tasks with progress tracking"""
        total_tasks = len(tasks)
        completed = 0
        
        async def track_task(task, task_id):
            nonlocal completed
            result = await task
            completed += 1
            progress = (completed / total_tasks) * 100
            print(f"\r[*] {description}: {progress:.1f}% ({completed}/{total_tasks})", end="")
            return result
        
        tracked_tasks = [track_task(task, i) for i, task in enumerate(tasks)]
        results = await asyncio.gather(*tracked_tasks)
        print()  # New line after progress
        return results
