<script lang="ts">
	import HowToPlay from '$lib/components/HowToPlay.svelte';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';
	import { clickOutside } from '$lib/domain/click-outside.svelte';
	import { setLoadedDataContext } from '$lib/domain/contexts';
	import { getDailyCourse, loadCoursesMap } from '$lib/domain/data-loaders';
	import { titleToScoredCourse } from '$lib/domain/query-scoring';
	import { matchWords } from '$lib/domain/sim-calcs';
	import type { ScoredCourse } from '$lib/interfaces/course-data';
    import { ArrowUpLeft, ChartColumn } from '@lucide/svelte';
    import SearchBar from '$lib/components/SearchBar.svelte'

    // load in json data
    const coursesMap = loadCoursesMap();
    const courseTitles = [...coursesMap.keys()];
    const dailyCourse = getDailyCourse();
    setLoadedDataContext({ coursesMap, courseTitles, dailyCourse });

    // search bar states
    let query = $state<string>("");

    // small functions
    const guessCourse = (e: MouseEvent) => {
        e.stopPropagation();
        const clickedBtn = e.currentTarget as HTMLElement;
        const guessedTitle = clickedBtn.parentElement?.id;
        console.log(guessedTitle);
        if (guessedTitle) {
            console.log(matchWords(guessedTitle, dailyCourse.title));
            console.log("guessed"); // TODO
        }
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

        <!-- daily course display -->
        <div class="flex flex-col w-full h-fit items-center text-center">
            <h4 class="text-xl">Today's course:</h4>
            <h2 class="daily-course-text wrap-anywhere">{dailyCourse.courseId}</h2>
            <h6>Guess the course title in 10 tries. <wbr>Enter a guess below!</h6>
        </div>

        <!-- course search bar -->
        <SearchBar bind:query={query} guessCourse={guessCourse}/>

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