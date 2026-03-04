<script lang="ts">
	import HowToPlay from '$lib/components/custom/HowToPlay.svelte';
	import { setLoadedDataContext } from '$lib/domain/contexts';
	import { getDailyCourse, loadCoursesMap } from '$lib/domain/data-loaders';
	import { cosineSim, matchWords, scaleCosineSim } from '$lib/domain/sim-calcs';
	import { type GuessedCourse } from '$lib/interfaces/course-data';
    import { ChartColumn } from '@lucide/svelte';
    import SearchBar from '$lib/components/custom/SearchBar.svelte'
	import GuessBlock from '$lib/components/custom/GuessBlock.svelte';
	import { getTodayGuessKey } from '$lib/domain/storage';
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/custom/Navbar.svelte';
	import DailyCourse from '$lib/components/custom/DailyCourse.svelte';

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
    let hasWon = $derived(guesses.some(course => course.simScore === 1));

    // small functions
    const guessCourse = (e: MouseEvent) => {
        e.stopPropagation();
        if (hasWon || guesses.length >= MAX_DAILY_GUESSES) { return; } // do nothing if no guesses left
        //^^^ possible TODO: make a toast notification for it

        const clickedBtn = e.currentTarget as HTMLElement;
        const guessedTitle = clickedBtn.parentElement?.id;
        const guessedCourse = guessedTitle ? coursesMap.get(guessedTitle) : undefined;
        if (guessedTitle && guessedCourse) {
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

    // const resetGuesses = () => { guesses = []; }
    
</script>

<div class="outer-main-container">
    <!-- central game container -->
    <div class="central-main-container fg-scrollbar">

        <!-- top navbar -->
        <Navbar />

        <!-- daily course display -->
        <DailyCourse dailyCourseId={dailyCourse.courseId} />

        <!-- course search bar -->
        <SearchBar bind:query={query} guessCourse={guessCourse}/>

        <!-- guesses container -->
        <div class="main-guess-scroll-area overflow-auto fg-scrollbar">
            <!-- guess fields labels -->
            <div class="guess-col-headers">
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