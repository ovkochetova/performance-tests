from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

courses_route = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses"]
)


class CourseIn(BaseModel):
    title: str
    description: str


class CourseOut(BaseModel):
    id: int
    title: str


class CoursesStore(BaseModel):
    root: list[CourseOut]

    def find(self, course_id: int) -> CourseOut | None:
        return next(filter(lambda course: course.id == course_id, self.root), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        course = CourseOut(id=len(self.root) + 1, **course_in.model_dump())
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut | None:
        index = next((i for i, course in enumerate(self.root) if course.id == course_id), None)
        if index is None:
            return None
        course = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = course
        return course

    def delete(self, course_id: int) -> None:
        self.root = [course for course in self.root if course.id != course_id]


store = CoursesStore(root=[])


@courses_route.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int):
    if not (course := store.find(course_id)):
        raise HTTPException(
            detail="Course not found",
            status_code=404
        )
    return course


@courses_route.get("", response_model=list[CourseOut])
async def get_courses():
    return store.root

@courses_route.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseIn):
    return store.create(course)


@courses_route.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn):
    if not store.find(course_id):
        raise HTTPException(
            detail="Course not found",
            status_code=404
        )
    return store.update(course_id, course)


@courses_route.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int):
    if not store.find(course_id):
        raise HTTPException(
            detail="Course not found",
            status_code=404
        )
    store.delete(course_id)


app.include_router(courses_route)
