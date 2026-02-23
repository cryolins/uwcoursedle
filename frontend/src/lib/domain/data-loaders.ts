import coursesJson from "$lib/courses.json";
import type { CourseData } from "$lib/interfaces/course-data";

// loads a map of the courses where key = title, value = course data
export function loadCoursesMap() {
    const coursesMap = new Map<string, CourseData>();
    for (const course of coursesJson) {
        coursesMap.set(course.title, course);
    }
    return coursesMap;
}