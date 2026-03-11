function getDayNum(dayOffset = 0): string {
    const now = new Date();
    const day = new Date(now.getTime() - (dayOffset * 24 * 60 * 60 * 1000));
    const dayStr = day.toLocaleDateString("en-CA", {
        year: "numeric", month: "2-digit", day:"2-digit", timeZone: "America/Toronto"
    }).replaceAll("-", "");
    return dayStr;
}
export function getTodayGuessKey(): string {
    return "guess-" + getDayNum();
}
export function getYesterdayGuessKey(): string {
    return "guess-" + getDayNum(-1);
}

export const STATS_KEY = "uwc-stats";