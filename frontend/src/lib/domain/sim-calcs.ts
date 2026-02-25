// calculates the dot product cosine similarity between two vectors of the same dimensions
export function cosineSim(a: number[], b: number[]) {
    if (a.length != b.length) {
        throw Error("different length vectors");
    } else {
        return a.reduce((prev, curr, i) => prev += (curr * b[i]), 0);
    }
}

// takes a cosine similarity value between -1 and 1 and scales it to be valuable for the player
export function scaleCosineSim(cosineSim: number) {
    return 0.35 * Math.atan(14 * ((cosineSim + 1) / 2 - 0.6)) + 0.512;
}

// checks what words are shared/matched between guessed title and daily title
export function matchWords(guessTitle: string, dailyTitle: string) {
    const SEPARATORS = /[ ,()–—!:.'-]/;
    const guessWords = guessTitle.split(SEPARATORS).filter(w => !!w);
    const dailyWords = dailyTitle.split(SEPARATORS).filter(w => !!w);
    //console.log(guessWords, dailyWords);
    const dailyWordsCounter = new Map<string, number>(dailyWords.map(w => [w.toLowerCase(), 0]));

    // loop 1: count matching words
    let dailyWordCount: number | undefined = undefined;
    for (const word of dailyWords) {
        dailyWordCount = dailyWordsCounter.get(word.toLowerCase());
        if (dailyWordCount != undefined) {
            dailyWordsCounter.set(word.toLowerCase(), dailyWordCount + 1);
        }
    }

    // loop 2: combining into a list of strings: matched strings start with "/m/"
    let guessTitleIndex = 0;
    let separatorsBetween = "";
    let returnList: string[] = [];
    for (const word of guessWords) {
        dailyWordCount = dailyWordsCounter.get(word.toLowerCase());
        if (dailyWordCount) {
            // neither 0 nor undefined
            //console.log(word, dailyWordCount);
            returnList.push("/m/" + word);
            dailyWordsCounter.set(word.toLowerCase(), dailyWordCount - 1);
        } else {
            returnList.push(word);
        }

        guessTitleIndex += word.length;
        separatorsBetween = getSeparators(guessTitle, guessTitleIndex, SEPARATORS);
        if (separatorsBetween) { returnList.push(separatorsBetween) };
        guessTitleIndex += separatorsBetween.length;
    }

    //console.log(returnList);
    return returnList;
}

// gets the separators between two tokens on a string, given the index of the first separator
function getSeparators(s: string, sepStartIndex: number, separators: RegExp) {
    let separatorStr = "";
    while (sepStartIndex < s.length && separators.test(s.charAt(sepStartIndex))) {
        separatorStr += s.charAt(sepStartIndex);
        sepStartIndex++;
    }
    return separatorStr;
}