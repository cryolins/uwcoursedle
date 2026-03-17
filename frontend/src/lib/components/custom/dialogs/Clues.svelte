<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { Lightbulb } from '@lucide/svelte';
	import ScrollArea from "../../ui/scroll-area/scroll-area.svelte";
	import { getLoadedDataContext } from "$lib/domain/contexts";
    import "./clues.css";
	import { CLUE_HEADERS, CLUE_NOTES } from "./clues-data";
	import { CLUE_COUNT } from "$lib/config";

    // get consts of interest
    const { dailyCourse, clueIndices, guessedCourseIds } = getLoadedDataContext();
    const words = dailyCourse.title.match(/\w+/g) || [];
    const [longest, secondLongest] = words.reduce<[string, string]>((longests, currentWord) => {
        if (currentWord.length > longests[0].length) { return [currentWord, longests[0]]; }
        if (currentWord.length > longests[1].length) { return [longests[0], currentWord]; }
        return longests;
    }, ["", ""]);
    const titleShape = dailyCourse.title.replaceAll(/\w/g, "_");

    // put into a list to iterate through
    const clueVals = [dailyCourse.subjectNames.join(" / "), titleShape, longest, secondLongest];
    let showClues = $derived(clueIndices().map(i => i >= 0));

</script>
 
<Dialog.Root>
    <Dialog.Trigger >
        <div class="clues-trigger transition-colors">
            <Lightbulb /> Clues
        </div>
    </Dialog.Trigger>

    <Dialog.Content class="dialog-sizing">
        <Dialog.Header>
            <Dialog.Title><h1>Clues</h1></Dialog.Title>
        </Dialog.Header>

        <ScrollArea type="always" class="dialog-inner-scroll-size">
            <div class="flex flex-col w-full gap-2">
                {#each Array(CLUE_COUNT) as _, i}
                     <!-- content here -->
                    <h2 class="text-xl">{CLUE_HEADERS[i]}</h2>
                    {#if CLUE_NOTES[i]}
                        <p>{CLUE_NOTES[i]}</p>
                    {/if}
                    <button class="show-hide-container max-w-full" 
                    onclick={() => clueIndices()[i] = guessedCourseIds().length}>
                        {showClues[i] ? clueVals[i] : "Show clue"}
                    </button>
                {/each}
            </div>
        </ScrollArea>
        
    </Dialog.Content>
</Dialog.Root>