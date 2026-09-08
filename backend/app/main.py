from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .models import AuditEvent, Priority, Status, WorkItem, WorkItemCreate, WorkItemPatch
from .store import Store

app = FastAPI(title="Operations Workflow Hub", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
store = Store()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/work-items", response_model=list[WorkItem])
def list_items(status: Status | None = None, priority: Priority | None = None, search: str = Query("", max_length=80)) -> list[WorkItem]:
    needle = search.casefold()
    return [item for item in store.items if (status is None or item.status == status) and (priority is None or item.priority == priority) and (not needle or needle in item.title.casefold() or needle in item.owner.casefold())]


@app.post("/api/work-items", response_model=WorkItem, status_code=201)
def create_item(data: WorkItemCreate, x_user: str = Header("demo-user")) -> WorkItem:
    return store.create(data, x_user)


@app.patch("/api/work-items/{item_id}", response_model=WorkItem)
def update_item(item_id: int, data: WorkItemPatch, x_user: str = Header("demo-user")) -> WorkItem:
    item = store.update(item_id, data, x_user)
    if item is None:
        raise HTTPException(status_code=404, detail="Work item not found")
    return item


@app.get("/api/metrics")
def metrics() -> dict[str, int]:
    return {"total": len(store.items), "open": sum(x.status != Status.COMPLETE for x in store.items), "blocked": sum(x.status == Status.BLOCKED for x in store.items), "urgent": sum(x.priority == Priority.URGENT for x in store.items)}


@app.get("/api/audit-events", response_model=list[AuditEvent])
def audit_events() -> list[AuditEvent]:
    return list(reversed(store.events))
