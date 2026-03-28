import { SEPARATORS } from "$lib/config";
import type { CourseIdentifiers, ScoredCourse } from "$lib/interfaces/course-data";

// scores courses based on:
/*
- highest if exact match
- then if title starts with query
- then if any words in the title start with query
- and finally if query at any point contains the query as a substring
*/

export function scoreCourse(title: string, query: string): number {
    title = title.toLowerCase();
    query = query.toLowerCase();
    const titleWords = title.split(SEPARATORS)
    const queryWords = query.split(SEPARATORS);

    if (title === query) return 5;
    if (title.startsWith(query)) return 4;
    if (titleWords.some(tw => tw.startsWith(query))) return 3;
    if (queryWords.every(qw => titleWords.some(tw => tw.startsWith(qw)))) return 2;
    if (title.includes(query)) return 1;
    return 0;
}

// function to help package a course title into ScoredCourse
export function courseToScoredCourse(course: CourseIdentifiers, query: string): ScoredCourse {
    return { courseId: course.courseId, title: course.title , score: scoreCourse(course.title, query)};
}