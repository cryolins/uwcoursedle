<script lang="ts">
	import HowToPlay from '$lib/components/HowToPlay.svelte';
	import { loadCoursesMap } from '$lib/domain/data-loaders';
    import { ChartColumn } from '@lucide/svelte';

    const coursesMap = loadCoursesMap();
    
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
        <input type="text" placeholder="Enter a guess..."
        class="p-2 w-5/6 border-3 border-primary2 rounded-lg bg-white text-black"/>

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