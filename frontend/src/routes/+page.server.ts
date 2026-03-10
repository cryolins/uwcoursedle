import { coursesMap, getDailyCourse } from "$lib/domain/server/data-loaders";
import { getTodayGuessKey, getYesterdayGuessKey } from "$lib/domain/storage";
import type { CourseData, CourseIdentifiers } from "$lib/interfaces/course-data";
import type { Actions, PageServerLoad } from "./$types";

function courseDataToIdentifiers(courseData: CourseData): CourseIdentifiers{
    return { courseId: courseData.courseId, title: courseData.title}
}

export const load: PageServerLoad = () => {
    const courseTitles: CourseIdentifiers[] = [...coursesMap.values().map(
        c => courseDataToIdentifiers(c)
    )];

    const dailyCourse = getDailyCourse();
    const dayGuessKey = getTodayGuessKey();
    const yesterdayGuessKey = getYesterdayGuessKey();

    return {
        courseTitles,
        dailyCourse,
        dayGuessKey,
        yesterdayGuessKey
    };
};