<script lang="ts">
	import HowToPlay from '$lib/components/HowToPlay.svelte';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';
	import { clickOutside } from '$lib/domain/click-outside.svelte';
	import { loadCoursesMap } from '$lib/domain/data-loaders';
	import { titleToScoredCourse } from '$lib/domain/query-scoring';
	import type { ScoredCourse } from '$lib/interfaces/course-data';
    import { ArrowUpLeft, ChartColumn } from '@lucide/svelte';

    const coursesMap = loadCoursesMap();
    const courseTitles = [...coursesMap.keys()];

    // search bar states
    let isSearchBarFocused = $state(false);
    let isSearchFocused = $state(false);
    let query = $state("");
    let searchResults = $derived(
        courseTitles.map(title => titleToScoredCourse(title, query))
                    .filter(scoredTitle => scoredTitle.score > 0)
                    .sort((a, b) => b.score - a.score) // sort descending on score
    );

    // small functions
    const guessCourse = (e: MouseEvent) => {
        e.stopPropagation();
        const clickedBtn = e.currentTarget as HTMLElement;
        const guessedTitle = clickedBtn.parentElement?.id;
        console.log(guessedTitle);
        if (guessedTitle) {
            console.log("guessed"); // TODO
        }
    }
    const fillInSearch = (e: MouseEvent) => {
        e.stopPropagation();
        const clickedBtn = e.currentTarget as HTMLElement;
        const clickedTitle = clickedBtn.parentElement?.id;
        query = !!clickedTitle ? clickedTitle : query;
    }
    const setFocusTrue = () => {
        isSearchBarFocused = true;
        isSearchFocused = true;
    }
    
    
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

        <!-- daily course display TODO fetch daily course -->
        <div class="flex flex-col w-full h-fit items-center text-center">
            <h4 class="text-xl">Today's course:</h4>
            <h2 class="daily-course-text wrap-anywhere">WWWWW308E</h2>
            <h6>Guess the course title in 10 tries. <wbr>Enter a guess below!</h6>
        </div>

        <!-- course search field TODO make the filtering -->
        <div class="w-5/6 h-fit relative search-frame-style" role="button" use:clickOutside onclick_outside={() => isSearchFocused = false}>
            <input type="text" placeholder="Enter a guess..." bind:value={query} class="search-frame-sizing"
            onfocus={setFocusTrue} oninput={setFocusTrue} onblur={() => isSearchBarFocused = false}/>

            <div class="w-full h-fit absolute top-full mt-1.5" hidden={!(isSearchFocused || isSearchBarFocused)}>
                <ScrollArea class="w-full rounded-sm border-2 border-primary2 border-solid">
                    <ol class="max-h-[40vh]">
                        {#each searchResults as searchResult}
                            <li class="relative" id={searchResult.title}>
                                <button onclick={guessCourse} class="search-result search-result-hover transition-colors">
                                    <p>{searchResult.title}</p>

                                    <!-- dummy box to take up space to leave room for real arrow-->
                                    <div class="opacity-0">
                                        <ArrowUpLeft />
                                    </div>
                                </button>
                                <button onclick={fillInSearch} class="absolute top-1 right-1 rounded-full hover:bg-primary/20 text-foreground/80">
                                    <ArrowUpLeft />
                                </button>
                            </li>
                        {/each}
                        {#if (!searchResults.length)}
                            <li class="search-result">No results found</li>
                        {/if}
                    </ol>
                </ScrollArea>
            </div>
        </div>

        <!-- guesses container -->
        <div class="flex flex-col w-full min-h-32 grow items-center gap-6 overflow-auto fg-scrollbar">
            <!-- guess fields labels -->
            <div class="flex flex-row w-4/5 h-fit justify-between gap-2">
                <p>Guess #</p>
                <p>Course title</p>
                <p>Similarity</p>
            </div>

            <ul class="flex flex-row w-full h-fit justify-around gap-4 items-center px-6 py-3 bg-zinc-900">
                <p class="w-fit">9</p>
                <p class="w-auto grow wrap-break-word text-center">Urbanization today: Introduction to cities and regions.</p>
                <p class="w-fit">100%</p>
            </ul>
            <ul class="flex flex-row w-full h-fit justify-around gap-4 items-center px-6 py-3 bg-zinc-900">
                <p class="w-fit">9</p>
                <p class="w-auto grow wrap-break-word text-center">Urbanization today: Introduction to cities and regions.</p>
                <p class="w-fit">100%</p>
            </ul>
            <ul class="flex flex-row w-full h-fit justify-around gap-4 items-center px-6 py-3 bg-zinc-900">
                <p class="w-fit">9</p>
                <p class="w-auto grow wrap-break-word text-center">Urbanization today: Introduction to cities and regions.</p>
                <p class="w-fit">100%</p>
            </ul>
            <ul class="flex flex-row w-full h-fit justify-around gap-4 items-center px-6 py-3 bg-zinc-900">
                <p class="w-fit">9</p>
                <p class="w-auto grow wrap-break-word text-center">Urbanization today: Introduction to cities and regions.</p>
                <p class="w-fit">100%</p>
            </ul>
            <ul class="flex flex-row w-full h-fit justify-around gap-4 items-center px-6 py-3 bg-zinc-900">
                <p class="w-fit">9</p>
                <p class="w-auto grow wrap-break-word text-center">Urbanization today: Introduction to cities and regions.</p>
                <p class="w-fit">100%</p>
            </ul>
        </div>

    </div>
</div>