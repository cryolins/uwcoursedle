// splitmix32 prng from https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript
function splitmix32(seed: number) {
    return function() {
        seed |= 0; // seed re-updated every time the function is called
        seed = seed + 0x9e3779b9 | 0; // ^^^
        let t = seed ^ seed >>> 16; // generate a random number based off current seed
        t = Math.imul(t, 0x21f0aaad); // a bunch of mixing functions
        t = t ^ t >>> 15;
        t = Math.imul(t, 0x735a2d97);
        return ((t = t ^ t >>> 15) >>> 0) / 4294967296;
    }
}

export function getDailyIndex(jsonLength: number) {
    const today = new Date();
    const todayStr = today.toLocaleDateString("en-CA", {
        year: "numeric", month: "2-digit", day:"2-digit", timeZone: "America/Toronto"
    }).replaceAll("-", "");
    const dailySeed = Number(todayStr);
    const dailyPRNG = splitmix32(dailySeed);
    const prngRes = dailyPRNG();
    return Math.min(Math.floor(prngRes * jsonLength), jsonLength - 1);
}