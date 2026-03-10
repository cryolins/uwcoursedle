export interface CourseData {
    courseId: string
    subjectCodes: string[]
    subjectNames: string[]
    title: string
    vector: number[]
}

export interface CourseIdentifiers {
    courseId: string
    title: string
}

export interface ScoredCourse {
    courseId: string
    title: string
    score: number
}

export interface GuessedCourse {
    titleFrags: string[]
    courseId: string
    simScore: number
    guessNum: number
}