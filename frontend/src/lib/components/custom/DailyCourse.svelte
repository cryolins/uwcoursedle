<script lang="ts">
	import { MAX_DAILY_GUESSES } from "$lib/config";
    import "./daily.css";
    let { dailyCourseId }: { dailyCourseId: string } = $props();
</script>

<div class="daily-display">
    <!-- <button class="bg-white text-zinc-900" onclick={resetGuesses}>reset {dayGuessKey}</button> -->
    <h4 class="text-xl">Today's course:</h4>
    <h2 class="daily-course-text wrap-anywhere">{dailyCourseId}</h2>
    <h6>Guess the course title in {MAX_DAILY_GUESSES} tries. <wbr>Enter a guess below!</h6>
</div>