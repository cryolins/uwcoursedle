import type { CourseData, GuessedCourse } from "$lib/interfaces/course-data";
import type { PlayerStats } from "$lib/interfaces/stats";
import { createContext } from "svelte";

interface LoadedDataContext {
    coursesMap: Map<string, CourseData>
    courseTitles: string[]
    dailyCourse: CourseData
    dayGuessKey: string
    guesses: () => GuessedCourse[]
    stats: () => PlayerStats
    hasWon: () => boolean
    hasLost: () => boolean
}

export const [getLoadedDataContext, setLoadedDataContext] = createContext<LoadedDataContext>();