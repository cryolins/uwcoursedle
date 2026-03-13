<script lang="ts">
	import { MAX_DAILY_GUESSES } from "$lib/config";
	import { getLoadedDataContext } from "$lib/domain/contexts";
    import "./daily.css";
    let { dailyCourse, hasLost } = getLoadedDataContext();

    let showAns = $state(false);
</script>

<div class="daily-display">
    <h4 class="text-xl">Today's course:</h4>
    <h2 class="daily-course-text wrap-anywhere">{dailyCourse.courseId}</h2>

    {#if hasLost()}
        <button class="show-hide-container show-ans-container" 
        onclick={() => showAns = !showAns}>
            {showAns ? dailyCourse.title : "Show answer"}
        </button>
    {/if}

    <h6>Guess the course title in {MAX_DAILY_GUESSES} tries. <wbr>Enter a guess below!</h6>
</div>