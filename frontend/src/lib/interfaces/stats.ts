export interface PlayerStats {
    wins: number
    plays: number
    streak: number
    guessStats: { scoreSum: number, amt: number } 
    // guess stats are only recorded on game completion (sum of scores, # of guesses) to take avg
}