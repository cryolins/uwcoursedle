import coursesJson from "$lib/courses.json";
import type { CourseData } from "$lib/interfaces/course-data";
import { getDailyIndex } from "./prng";

// loads a map of the courses where key = title, value = course data
export function loadCoursesMap() {
    const coursesMap = new Map<string, CourseData>();
    for (const course of coursesJson) {
        coursesMap.set(course.title, course);
    }
    return coursesMap;
}

// gets daily course using seeded prng in the form of a CourseData object
export function getDailyCourse(): CourseData {
    const dailyIndex = getDailyIndex(coursesJson.length);
    return coursesJson[dailyIndex];
}