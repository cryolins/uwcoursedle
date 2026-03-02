export function getTodayKey(): string {
    const today = new Date();
    const dayNum = (today.getFullYear() * 10000) + ((today.getMonth() + 1) * 100) + (today.getDate());
    return dayNum.toString();
}
export function getTodayGuessKey(): string {
    return "guess-" + getTodayKey();
}