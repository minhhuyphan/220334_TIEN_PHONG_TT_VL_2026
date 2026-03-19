import asyncio
import json
import uuid
from typing import Dict, List, Optional
from app.models.banner_db import TasksManager, UserManager, BannerHistoryManager, ConfigManager
from app.config import settings

class TaskManagerRAM:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManagerRAM, cls).__new__(cls)
            cls._instance.queue = asyncio.Queue()
            cls._instance.active_tasks: Dict[str, dict] = {}
            cls._instance.worker_task = None
        return cls._instance

    async def add_task(self, task_id: str, user_id: int, request_data: dict, process_func):
        task_info = {
            "id": task_id,
            "user_id": user_id,
            "request_data": request_data,
            "process_func": process_func,
            "status": "pending"
        }
        self.active_tasks[task_id] = task_info
        await self.queue.put(task_id)
        return task_id

    async def start_worker(self):
        if self.worker_task is None:
            self.worker_task = asyncio.create_task(self._worker_loop())
            print("🚀 RAM Task Worker started.")

    async def _worker_loop(self):
        while True:
            task_id = await self.queue.get()
            try:
                task_info = self.active_tasks.get(task_id)
                if not task_info:
                    continue
                
                task_info["status"] = "processing"
                # Call the processing function
                await task_info["process_func"](task_id, task_info["user_id"], task_info["request_data"])
                
            except Exception as e:
                print(f"❌ Error in RAM worker for task {task_id}: {e}")
            finally:
                if task_id in self.active_tasks:
                    # Keep for a while or remove? 
                    # User said "lưu vào ram", maybe they want to query recent tasks from RAM?
                    # For now, let's keep it until it's finished and then maybe remove after some time.
                    del self.active_tasks[task_id]
                self.queue.task_done()

    async def get_active_tasks(self):
        return self.active_tasks

# Singleton instance
ram_task_manager = TaskManagerRAM()
