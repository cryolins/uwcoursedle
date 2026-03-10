<script lang="ts">
	import { setLoadedDataContext } from '$lib/domain/contexts';
	import { cosineSim, matchWords, scaleCosineSim } from '$lib/domain/sim-calcs';
	import { type GuessedCourse } from '$lib/interfaces/course-data';
    import SearchBar from '$lib/components/custom/SearchBar.svelte'
	import GuessBlock from '$lib/components/custom/GuessBlock.svelte';
	import { STATS_KEY } from '$lib/domain/storage';
	import { onMount, untrack } from 'svelte';
	import Navbar from '$lib/components/custom/Navbar.svelte';
	import DailyCourse from '$lib/components/custom/DailyCourse.svelte';
	import { type PlayerStats } from '$lib/interfaces/stats';
	import { MAX_DAILY_GUESSES } from '$lib/config';
	import { toast } from 'svelte-sonner';
	import type { PageData, PageProps } from './$types';
	import type { GuessResponse } from '$lib/interfaces/guess-server';

    // load in json data
    let { data }: PageProps = $props();
    const { courseTitles, dailyCourse, dayGuessKey, yesterdayGuessKey } = data;

    // search bar and guesses states
    let query = $state<string>("");
    let guesses = $state<GuessedCourse[]>([]);
    let hasWon = $derived(guesses.some(course => course.simScore === 1));
    let hasLost = $derived(guesses.length >= MAX_DAILY_GUESSES && !hasWon);
    let canEnd = $state<boolean>(false); // state to prevent triggering counting player stats on mount

    // stats
    let stats = $state<PlayerStats>({
        wins: 0, plays: 0, streak: 0, guessStats: { scoreSum: 0, amt: 0 }
    });
    let openStats = $state(false);

    // context 
    setLoadedDataContext({ 
        courseTitles, dailyCourse, dayGuessKey,
        guesses: () => guesses, stats: () => stats,
        hasWon: () => hasWon, hasLost: () => hasLost
    });

    // small functions
    const guessCourse = async (e: MouseEvent) => {
        e.stopPropagation();
        if (hasWon || hasLost) { return; } // do nothing if no guesses left

        const clickedBtn = e.currentTarget as HTMLElement;
        const guessId = clickedBtn.parentElement?.id;
        if (guessId) {
            const res = await fetch("/guess", {
                method: "POST",
                body: JSON.stringify({ guessId, dailyId: dailyCourse.courseId }),
                headers: { "Content-Type": "application/json" }
            });
            if (!res.ok) {
                toast.error(`Error processing guess. Please try again (${res.status})`);
                return;
            }

            const guessRes: GuessResponse = await res.json();
            guesses.push({...guessRes, courseId: guessId, guessNum: guesses.length + 1})
            canEnd = true; // tie being able to end to solely making guesses
        }
    }    
    const guessComparator = (a: GuessedCourse, b: GuessedCourse) => {
        return b.simScore - a.simScore;
    }

    // onMounts and effects
    onMount(() => {
        // fetch guesses and stats from localStorage
        const savedGuesses = localStorage.getItem(dayGuessKey);
        guesses = savedGuesses ? JSON.parse(savedGuesses) : [];
        const savedStats = localStorage.getItem(STATS_KEY);
        stats = savedStats ? JSON.parse(savedStats) : stats;

        // fetch yesterday data to decide if streak exists
        const yesterdayGuessesStr = localStorage.getItem(yesterdayGuessKey);
        const yesterdayGuesses: GuessedCourse[] = yesterdayGuessesStr ? JSON.parse(yesterdayGuessesStr) :  []
        const wonYesterday = yesterdayGuesses && yesterdayGuesses.some(course => course.simScore === 1);
        if (!wonYesterday) { 
            stats.streak = hasWon ? 1 : 0; 
            localStorage.setItem(STATS_KEY, JSON.stringify(stats));
        }

        // setup tab sync event for guesses
        const storageHandler = (e: StorageEvent) => {
            if (e.key === dayGuessKey && e.newValue) {
                // match current render's dayGuessKey
                guesses = JSON.parse(e.newValue);
            } else if (e.key === STATS_KEY && e.newValue) {
                stats = JSON.parse(e.newValue);
            }
        }
        window.addEventListener("storage", storageHandler);

        return () => {
            window.removeEventListener("storage", storageHandler);
        }
    });

    // localStorage syncing
    $effect(() => {
        if (guesses) {
            // use loaded guess key on render so players can still play across midnight
            localStorage.setItem(dayGuessKey, JSON.stringify(guesses));
        }
    });
    $effect(() => {
        if (stats) { localStorage.setItem(STATS_KEY, JSON.stringify(stats)); }
    });

    // win/lose effects
    $effect(() => {
        if (hasWon) { // hasWon is sole dependency
            untrack(() => {
                if (canEnd) {                    
                    // update stats
                    stats.plays += 1;
                    stats.wins += 1;
                    stats.streak += 1;
                    stats.guessStats.amt += guesses.length;
                    stats.guessStats.scoreSum += guesses.reduce(
                        (scoreAcc: number, currGuess: GuessedCourse) => scoreAcc + currGuess.simScore, 0);
                    
                    localStorage.setItem(STATS_KEY, JSON.stringify(stats));

                    // send a toast
                    toast.success("You won!");
                }
                openStats = true;
            });
        }
    });
    $effect(() => {
        if (hasLost) { // hasWon is sole dependency
            untrack(() => {
                if (canEnd) {
                    // update stats
                    stats.plays += 1;
                    stats.streak = 0;
                    stats.guessStats.amt += guesses.length;
                    stats.guessStats.scoreSum += guesses.reduce(
                        (scoreAcc: number, currGuess: GuessedCourse) => scoreAcc + currGuess.simScore, 0);
                    
                    localStorage.setItem(STATS_KEY, JSON.stringify(stats));

                    // send a toast
                    toast.error("Game over :(");
                }
                openStats = true;
            });
        }
    });

    // const resetGuesses = () => { guesses = []; }
    
</script>

<div class="outer-main-container">
    <!-- central game container -->
    <div class="central-main-container fg-scrollbar">

        <!-- top navbar -->
        <Navbar bind:openStats={openStats}/>

        <!-- daily course display -->
        <DailyCourse />

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