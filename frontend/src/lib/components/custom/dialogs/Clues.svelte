<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { Lightbulb } from '@lucide/svelte';
	import ScrollArea from "../../ui/scroll-area/scroll-area.svelte";
	import { getLoadedDataContext } from "$lib/domain/contexts";
    import "./clues.css";

    const { dailyCourse } = getLoadedDataContext();
    const words = dailyCourse.title.match(/\w+/g) || [];
    const [longest, secondLongest] = words.reduce<[string, string]>((longests, currentWord) => {
        if (currentWord.length > longests[0].length) { return [currentWord, longests[0]]; }
        if (currentWord.length > longests[1].length) { return [longests[0], currentWord]; }
        return longests;
    }, ["", ""]);
    const titleShape = dailyCourse.title.replaceAll(/\w/g, "_");

    let showSubj = $state(false);
    let showLongest = $state(false);
    let showSecondLongest = $state(false);
    let showShape = $state(false);

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
                <h2 class="text-xl">Subject area(s)</h2>
                <button class="show-hide-container max-w-full" 
                onclick={() => showSubj = !showSubj}>
                    {showSubj ? dailyCourse.subjectNames.join(" / ") : "Show clue"}
                </button>

                <h2 class="text-xl">Title shape</h2>
                <p>(Title but letters and numbers are replaced by underscores)</p>
                <button class="show-hide-container max-w-full" 
                onclick={() => showShape = !showShape}>
                    <h6>{showShape ? titleShape : "Show clue"}</h6>
                </button>
                
                <h2 class="text-xl">Longest word</h2>
                <button class="show-hide-container max-w-full" 
                onclick={() => showLongest = !showLongest}>
                    {showLongest ? longest : "Show clue"}
                </button>

                <h2 class="text-xl">Second longest word</h2>
                <button class="show-hide-container max-w-full" 
                onclick={() => showSecondLongest = !showSecondLongest}>
                    {showSecondLongest ? secondLongest : "Show clue"}
                </button>
            </div>
        </ScrollArea>
        
    </Dialog.Content>
</Dialog.Root>