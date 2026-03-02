export interface CourseData {
    courseId: string
    subjectCode: string
    title: string
    vector: number[]
}

export interface ScoredCourse {
    title: string
    score: number
}

export interface GuessedCourse {
    titleFrags: string[]
    simScore: number
    guessNum: number
}