export interface GuessRequest {
    guessId: string
    dailyId: string
}

export interface GuessResponse {
    titleFrags: string[]
    simScore: number
}