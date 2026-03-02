<script lang="ts">
	import { clickOutside } from "$lib/domain/click-outside.svelte";
	import { titleToScoredCourse } from "$lib/domain/query-scoring";
	import { matchWords } from "$lib/domain/sim-calcs";
	import { ArrowUpLeft } from "@lucide/svelte";
	import ScrollArea from "./ui/scroll-area/scroll-area.svelte";
	import type { CourseData } from "$lib/interfaces/course-data";
	import { getLoadedDataContext } from "$lib/domain/contexts";

    interface SearchProps {
        query: string
        guessCourse: (e: MouseEvent) => void
    }

    // search bar states
    let { query=$bindable(), guessCourse }: SearchProps = $props();
    const { courseTitles, dailyCourse } = getLoadedDataContext();
    let isSearchBarFocused = $state(false);
    let isSearchFocused = $state(false);
    //let query = $state("");
    let searchResults = $derived(
        courseTitles.map(title => titleToScoredCourse(title, query))
                    .filter(scoredTitle => scoredTitle.score > 0)
                    .sort((a, b) => b.score - a.score) // sort descending on score
    );

    // small functions
    const guessCourseAndBlur = (e: MouseEvent) => {
        guessCourse(e);
        isSearchBarFocused = false;
        isSearchFocused = false;
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

<!-- course search field -->
<div class="w-5/6 h-fit relative search-frame-style" role="button" use:clickOutside onclick_outside={() => isSearchFocused = false}>
    <input type="text" placeholder="Enter a guess..." bind:value={query} class="search-frame-sizing"
    onfocus={setFocusTrue} oninput={setFocusTrue} onblur={() => isSearchBarFocused = false}/>

    <div class="w-full h-fit absolute z-10 top-full mt-1.5" hidden={!(isSearchFocused || isSearchBarFocused)}>
        <ScrollArea class="w-full rounded-sm border-2 border-primary2 border-solid">
            <ol class="max-h-[40vh]">
                {#each searchResults as searchResult}
                    <li class="relative" id={searchResult.title}>
                        <button onclick={guessCourseAndBlur} class="search-result search-result-hover transition-colors">
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