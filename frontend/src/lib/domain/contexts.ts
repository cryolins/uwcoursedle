import type { CourseData, CourseIdentifiers, GuessedCourse } from "$lib/interfaces/course-data";
import type { PlayerStats } from "$lib/interfaces/stats";
import { createContext } from "svelte";

interface LoadedDataContext {
    courseTitles: CourseIdentifiers[]
    dailyCourse: CourseIdentifiers & { subjectNames: string[] }
    dayGuessKey: string
    guesses: () => GuessedCourse[]
    stats: () => PlayerStats
    hasWon: () => boolean
    hasLost: () => boolean
}

export const [getLoadedDataContext, setLoadedDataContext] = createContext<LoadedDataContext>();