import coursesJsonSource from "./courses.json"
import type { CourseData } from "$lib/interfaces/course-data";
import { getDailyIndex } from "../prng";

const coursesJson = coursesJsonSource as CourseData[]

// loads a map of the courses where key = title, value = course data
function loadCoursesMap() {
    const coursesMap = new Map<string, CourseData>();
    for (const course of coursesJson) {
        coursesMap.set(course.courseId, course);
    }
    return coursesMap;
}

export const coursesMap = loadCoursesMap();

// gets daily course using seeded prng in the form of a CourseData object
export function getDailyCourseId(): string {
    const dailyIndex = getDailyIndex(coursesJson.length);
    return coursesJson[dailyIndex].courseId;
}