from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Project(BaseModel):
    id: int
    title: str
    description: str
    tech: list[str]
    github_url: str | None = None
    live_url: str | None = None
    featured: bool = False


class ContactMessage(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    message: str = Field(min_length=5, max_length=500)


# in-memory "database" (resets every time the server restarts)
projects = [
    Project(
        id=1,
        title="FlightWatch",
        description="Real-time dashboard that spots unusual flight activity.",
        tech=["TypeScript", "React"],
        github_url="https://github.com/your-username/flightwatch",
        featured=True,
    ),
    Project(
        id=2,
        title="UMD Course Planner",
        description="Web app that helps UMD students plan their classes.",
        tech=["TypeScript", "React", "Python"],
        github_url="https://github.com/your-username/umd-course-planner",
        live_url="https://your-planner-link.com",
        featured=True,
    ),
    Project(
        id=3,
        title="Fynn",
        description="AI financial agent built at Bitcamp 2026.",
        tech=["Python"],
        github_url="https://github.com/your-username/fynn",
        featured=False,
    ),
]

contact_messages = [
    ContactMessage(name="Test Recruiter", email="test@example.com", message="Loved your portfolio!"),
]


# 1. GET all projects, optionally filter by tech or featured
@app.get("/projects")
def get_projects(tech: str | None = None, featured: bool | None = None):
    results = projects
    if tech is not None:
        results = [p for p in results if tech.lower() in [t.lower() for t in p.tech]]
    if featured is not None:
        results = [p for p in results if p.featured == featured]
    return results


# 2. GET one project by id
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for p in projects:
        if p.id == project_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")


# 3. POST a message from the contact form
@app.post("/contact", status_code=201)
def submit_contact(msg: ContactMessage):
    contact_messages.append(msg)
    return {"message": f"Thanks {msg.name}, I'll get back to you soon!", "total_messages": len(contact_messages)}
