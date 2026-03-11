<script lang="ts">
	import type { GuessedCourse } from "$lib/interfaces/course-data";
	import { onDestroy, onMount } from "svelte";
	import GuessTitleText from "./GuessTitleText.svelte";
    import "./guesses.css";
	import { getLoadedDataContext } from "$lib/domain/contexts";

    interface GuessBlockProps {
        guess: GuessedCourse
        guessesLength: number
    }
    let { guess, guessesLength }: GuessBlockProps = $props();
    let countPercent = $state(0);
    let { dailyCourse } = getLoadedDataContext();

    onMount(() => {
        const startTime = performance.now();
        const duration = 1000;
        const ease = (x: number) => {
            return Math.pow(x - 1, 5) + 1;
        }

        function frameStep(currTime: number) {
            countPercent = ease(Math.min((currTime - startTime) / duration, 1));
            if(countPercent < 1) {
                requestAnimationFrame(frameStep);
            }
        }

        requestAnimationFrame(frameStep);
    });

</script>

<ul class={`guess-block ${ guess.courseId === dailyCourse.courseId ? "bg-word-match/20" 
                            : (guess.guessNum === guessesLength ? "bg-zinc-700" : "bg-zinc-900") }`}>
    <p class="w-fit">{guess.guessNum}</p>
    <p class="course-title">
        <GuessTitleText titleFrags={guess.titleFrags} courseId={guess.courseId} />
    </p>
    <p class="sim-score">{(guess.simScore * countPercent * 100).toFixed(1)}%</p>
</ul>