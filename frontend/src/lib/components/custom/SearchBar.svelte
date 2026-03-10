<script lang="ts">
	import { clickOutside } from "$lib/domain/click-outside.svelte";
	import { courseToScoredCourse } from "$lib/domain/query-scoring";
	import { matchWords } from "$lib/domain/sim-calcs";
	import { ArrowUpLeft } from "@lucide/svelte";
	import ScrollArea from "../ui/scroll-area/scroll-area.svelte";
	import type { CourseData } from "$lib/interfaces/course-data";
	import { getLoadedDataContext } from "$lib/domain/contexts";
    import "./search-bar.css";
	import { MIN_CHARS_TO_SEARCH } from "$lib/config";

    interface SearchProps {
        query: string
        guessCourse: (e: MouseEvent) => void
    }

    // search bar states
    let { query=$bindable(), guessCourse }: SearchProps = $props();
    const { courseTitles } = getLoadedDataContext();
    let isSearchBarFocused = $state(false);
    let isSearchFocused = $state(false);
    //let query = $state("");
    let searchResults = $derived(
        query.length <= MIN_CHARS_TO_SEARCH ? [] :
        courseTitles.map(iden => courseToScoredCourse(iden, query))
                    .filter(scoredTitle => scoredTitle.score > 0)
                    .sort((a, b) => b.score - a.score) // sort descending on score
    );

    // small functions
    const guessCourseAndBlur = (e: MouseEvent) => {
        guessCourse(e);
        isSearchBarFocused = false;
        isSearchFocused = false;
    }
    const fillInSearch = (title: string) => {
        return (e: MouseEvent) => {
            e.stopPropagation();
            query = title;
        }
    }
    const setFocusTrue = () => {
        isSearchBarFocused = true;
        isSearchFocused = true;
    }

</script>

<!-- course search field -->
<div class="outer-container-sizing relative text-frame-style" role="button" use:clickOutside onclick_outside={() => isSearchFocused = false}>
    <input type="text" placeholder="Enter a guess..." bind:value={query} class="search-frame-sizing"
    onfocus={setFocusTrue} oninput={setFocusTrue} onblur={() => isSearchBarFocused = false}/>

    <div class="absolute dropdown-container" hidden={!(isSearchFocused || isSearchBarFocused)}>
        <ScrollArea class="w-full rounded-sm dropdown-scrollarea-border">
            <ol class="max-h-[40vh]">
            
                {#if query.length <= MIN_CHARS_TO_SEARCH}
                    <li class="search-result">Enter some more letters! ({MIN_CHARS_TO_SEARCH + 1}+)</li>
                {:else if (!searchResults.length)}
                    <li class="search-result">No results found</li>
                {:else}
                    {#each searchResults as searchResult}
                        <li class="relative" id={searchResult.courseId}>
                            <button onclick={guessCourseAndBlur} class="search-result search-result-hover transition-colors">
                                <p>{searchResult.title}</p>

                                <!-- dummy box to take up space to leave room for real arrow-->
                                <div class="opacity-0">
                                    <ArrowUpLeft />
                                </div>
                            </button>
                            <button onclick={fillInSearch(searchResult.title)} class="absolute top-1 right-1 rounded-full hover:bg-primary/20 text-foreground/80">
                                <ArrowUpLeft />
                            </button>
                        </li>
                    {/each}
                {/if}
            </ol>
        </ScrollArea>
    </div>
</div>