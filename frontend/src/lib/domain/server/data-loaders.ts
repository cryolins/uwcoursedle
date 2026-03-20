import coursesJsonSource from "./courses.json"
import playablesSource from "./playable-list.json"
import type { CourseData, CourseIdentifiers } from "$lib/interfaces/course-data";
import { getDailyIndex } from "../prng";

const coursesJson = coursesJsonSource as CourseData[];
const playables = playablesSource as string[];

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
export function getDailyCourse(): CourseIdentifiers & { subjectNames: string[] } {
    const dailyIndex = getDailyIndex(playables.length);
    const playableCourseId = playables[dailyIndex];
    const { courseId, title, subjectNames } = coursesMap.get(playableCourseId)!;
    return { courseId, title, subjectNames };
}