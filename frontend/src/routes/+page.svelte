<script lang="ts">
	import HowToPlay from '$lib/components/HowToPlay.svelte';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';
	import { clickOutside } from '$lib/domain/click-outside.svelte';
	import { setLoadedDataContext } from '$lib/domain/contexts';
	import { getDailyCourse, loadCoursesMap } from '$lib/domain/data-loaders';
	import { titleToScoredCourse } from '$lib/domain/query-scoring';
	import { cosineSim, matchWords, scaleCosineSim } from '$lib/domain/sim-calcs';
	import { type GuessedCourse, type ScoredCourse } from '$lib/interfaces/course-data';
    import { ArrowUpLeft, ChartColumn } from '@lucide/svelte';
    import SearchBar from '$lib/components/SearchBar.svelte'
    import GuessTitleText from '$lib/components/GuessTitleText.svelte'
	import GuessBlock from '$lib/components/GuessBlock.svelte';
	import { getTodayGuessKey, getTodayKey } from '$lib/domain/storage';
	import { onMount } from 'svelte';

    // constants
    const MAX_DAILY_GUESSES = 10;

    // load in json data
    const coursesMap = loadCoursesMap();
    const courseTitles = [...coursesMap.keys()];
    const dailyCourse = getDailyCourse();
    const dayGuessKey = getTodayGuessKey();
    setLoadedDataContext({ coursesMap, courseTitles, dailyCourse });

    // search bar and guesses states
    let query = $state<string>("");
    let guesses = $state<GuessedCourse[]>([]);
    let hasWon = $state(false);

    // small functions
    const guessCourse = (e: MouseEvent) => {
        e.stopPropagation();
        if (hasWon || guesses.length >= MAX_DAILY_GUESSES) { return; } // do nothing if no guesses left
        //^^^ possible TODO: make a toast notification for it

        const clickedBtn = e.currentTarget as HTMLElement;
        const guessedTitle = clickedBtn.parentElement?.id;
        const guessedCourse = guessedTitle ? coursesMap.get(guessedTitle) : undefined;
        if (guessedTitle && guessedCourse) {
            if (guessedTitle === dailyCourse.title) { hasWon = true; }

            const titleFrags = matchWords(guessedTitle, dailyCourse.title);
            const simScore = scaleCosineSim(cosineSim(guessedCourse.vector, dailyCourse.vector))
            guesses.push({ titleFrags, simScore, guessNum: guesses.length + 1 });
        }
    }    
    const guessComparator = (a: GuessedCourse, b: GuessedCourse) => {
        return b.simScore - a.simScore;
    }

    // onMounts and effects
    onMount(() => {
        // fetch guesses from localStorage
        const savedGuesses = localStorage.getItem(dayGuessKey);
        guesses = savedGuesses ? JSON.parse(savedGuesses) : [];

        // setup tab sync event for guesses
        const storageHandler = (e: StorageEvent) => {
            if (e.key === dayGuessKey && e.newValue) {
                // match current render's dayGuessKey
                guesses = JSON.parse(e.newValue);
            }
        }
        window.addEventListener("storage", storageHandler);

        return () => {
            window.removeEventListener("storage", storageHandler);
        }
    });
    $effect(() => {
        if (guesses) {
            // use loaded guess key on render so players can still play across midnight
            localStorage.setItem(dayGuessKey, JSON.stringify(guesses));
        }
    });

    // const resetGuesses = () => { guesses = []; hasWon = false; }
    
</script>

<div class="flex w-full h-screen bg-zinc-800 justify-center items-center text-white">
    <!-- central game container -->
    <div class="flex flex-col size-full max-w-xl items-center gap-6 overflow-y-auto overflow-x-hidden fg-scrollbar">

        <!-- top navbar -->
        <div class="flex flex-row w-full h-fit justify-between px-2 py-3 border-b-8 border-primary2">
            <h1 class="text-4xl overflow-hidden">
                <span class="text-primary2">UW</span>Coursedle
            </h1>

            <!-- dialog-opening icons TODO dialog components -->
            <div class="flex flex-row w-fit h-full gap-2 sm:gap-4">
                <HowToPlay />
                <ChartColumn class="size-10"/>
            </div>
        </div>

        <!-- daily course display -->
        <div class="flex flex-col w-full h-fit items-center text-center">
            <!-- <button class="bg-white text-zinc-900" onclick={resetGuesses}>reset {dayGuessKey}</button> -->
            <h4 class="text-xl">Today's course:</h4>
            <h2 class="daily-course-text wrap-anywhere">{dailyCourse.courseId}</h2>
            <h6>Guess the course title in 10 tries. <wbr>Enter a guess below!</h6>
        </div>

        <!-- course search bar -->
        <SearchBar bind:query={query} guessCourse={guessCourse}/>

        <!-- guesses container -->
        <div class="main-guess-scroll-area overflow-auto fg-scrollbar">
            <!-- guess fields labels -->
            <div class="flex flex-row w-4/5 h-fit justify-between gap-2">
                <p>Guess #</p>
                <p>Course title</p>
                <p>Similarity</p>
            </div>

            {#each guesses.toSorted(guessComparator) as guess (guess.guessNum)}
                <GuessBlock guess={guess} />
            {/each}
            
        </div>

    </div>
</div>