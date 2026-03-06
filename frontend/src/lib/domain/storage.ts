function getDayNum(dayOffset = 0): string {
    const day = new Date();
    day.setDate(day.getDate() + dayOffset);
    const dayNum = (day.getFullYear() * 10000) + ((day.getMonth() + 1) * 100) + (day.getDate());
    return dayNum.toString();
}
export function getTodayGuessKey(): string {
    return "guess-" + getDayNum();
}
export function getYesterdayGuessKey(): string {
    return "guess-" + getDayNum(-1);
}

export const STATS_KEY = "uwc-stats";