<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { ChartColumn } from '@lucide/svelte';
	import ScrollArea from "../ui/scroll-area/scroll-area.svelte";
    import { STATS_KEY } from "$lib/domain/storage";
	import { onMount } from "svelte";
    import flameImg from "$lib/assets/flame.png";
    import greyFlameImg from "$lib/assets/greyflame.png";
    import "./stats.css";
	import { getLoadedDataContext } from "$lib/domain/contexts";
	import type { GuessedCourse } from "$lib/interfaces/course-data";
	import { SITE_URL } from "$lib/config";

    let { openStats=$bindable() } : { openStats?: boolean } = $props();
    let { stats, dayGuessKey, hasWon, hasLost, guesses } = getLoadedDataContext();
    let copyInput = $state<HTMLInputElement>();
    let hasPlayed = $derived(hasWon() || hasLost());

    function getEmojiString(guessesArr: GuessedCourse[]) {
        function mapToEmoji(guess: GuessedCourse) {
            const emojis = ["🟥", "🟧", "🟨", "🟩", "✅"];
            return emojis[Math.floor(guess.simScore * 4)];
        }
        return guessesArr.map(g => mapToEmoji(g)).join("");
    }

    function getDateString() {
        const dateStr = dayGuessKey.split("-").at(1);
        return dateStr?.slice(0, 4) + "/" + dateStr?.slice(4, 6) + "/" + dateStr?.slice(6);
    }

    const copyToClipboard = () => {
        navigator.clipboard.writeText(copyInput?.value ?? "");
    }

    onMount(() => {
        const savedStats = localStorage.getItem(STATS_KEY);
    });

</script>
 
<Dialog.Root bind:open={openStats} onOpenChange={(val) => (openStats = val)}>
    <Dialog.Trigger >
        <ChartColumn class="size-10"/>
    </Dialog.Trigger>

    <Dialog.Content class="w-xl max-w-9/10">
        <Dialog.Header>
            <Dialog.Title><h1>Your Stats</h1></Dialog.Title>
        </Dialog.Header>

        <ScrollArea type="always" class="dialog-inner-scroll-size overflow-y-hidden">
            <div class="main-stats-container">
                <!-- all-time stats -->
                 <h3 class="text-xl">All-time Games Stats</h3>
                <div class="all-time-container">
                    <img src={stats().streak ? flameImg : greyFlameImg} alt="streak flame" class="streak-img"/>
                    <div>Win <br/>Streak:<br/><h6 class="text-3xl">{stats().streak}</h6></div>
                    <div class="all-time-grid">
                        <div>
                            <p>Completed</p>
                            <h6>{stats().plays}</h6>
                        </div>
                        <div>
                            <p>Won</p>
                            <h6>{stats().wins}</h6>
                        </div>
                        <div>
                            <p>% Won</p>
                            <h6>{stats().plays ? (100 * stats().wins / stats().plays).toFixed(1) + "%" : "N/A"}</h6>
                        </div>
                        <div>
                            <p>Avg. <wbr/>Guesses</p>
                            <h6>{stats().wins ? (stats().guessStats.amt / stats().plays).toFixed(1): "N/A"}</h6>
                        </div>
                    </div>                        
                </div>
                <h3 class="text-xl">Share Today's Results:</h3>
                <div class="share-container">
                    <input class="text-frame-style share-input-sizing"
                     type="text" readonly bind:this={copyInput}
                     value={`UWCoursedle (${getDateString()}): ${(hasPlayed ? getEmojiString(guesses()) : "Play now! |")} ${SITE_URL}`}/>
                    <button onclick={copyToClipboard} class="rounded-sm copy-button transition-colors">
                        Copy
                    </button>
                </div>
            </div>
        </ScrollArea>
        
    </Dialog.Content>
</Dialog.Root>