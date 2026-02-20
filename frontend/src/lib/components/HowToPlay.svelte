<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { CircleQuestionMark } from '@lucide/svelte';
	import ScrollArea from "./ui/scroll-area/scroll-area.svelte";
</script>
 
<Dialog.Root>
    <Dialog.Trigger >
        <CircleQuestionMark class="size-10"/>
    </Dialog.Trigger>

    <Dialog.Content class="w-xl max-w-full">
        <Dialog.Header>
            <Dialog.Title><h1>How to Play</h1></Dialog.Title>
        </Dialog.Header>

        <ScrollArea type="always" class="w-full max-h-[calc(80vh-102px)]">
            <div class="flex flex-col w-full gap-4">
                <p>
                    Welcome to <span class="text-primary2">UW</span>Coursedle! Your goal is to guess the correct course title based off the course code in <span class="font-bold underline">10</span> tries.
                </p>
                <p>
                    These courses are based off those listed on the University of Waterloo’s <a href="https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/home" class="underline">undergraduate calendar</a>.
                    <br/><span class="italic">Last updated: Feb 2026 (2025-2026 academic year)</span>.
                </p>
                <p>
                    Browse through course titles to search for a course to make your guess!
                    The <span class="text-word-match">green</span> text in your guess show the words with an exact match between your guess and the actual course name. 
                    The similarity score represents how semantically close the topic of the course is to your guess.
                </p>
                <p>
                    Have fun! - Pei Lin He   (<a href="https://github.com/cryolins/uwcoursedle" class="underline">view UWCoursedle on GitHub</a>)
                </p>
            </div>
        </ScrollArea>
        
    </Dialog.Content>
</Dialog.Root>