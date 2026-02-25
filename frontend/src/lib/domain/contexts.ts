import type { CourseData } from "$lib/interfaces/course-data";
import { createContext } from "svelte";

interface LoadedDataContext {
    coursesMap: Map<string, CourseData>
    courseTitles: string[]
    dailyCourse: CourseData     
}

export const [getLoadedDataContext, setLoadedDataContext] = createContext<LoadedDataContext>();