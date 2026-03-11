<script lang="ts">
    import "./guesses.css";
    let { titleFrags, courseId }: { titleFrags: string[], courseId: string } = $props();

    function getClass(frag: string) {
        if (frag.startsWith("/m/")) {
            return "matched-animate-in";
        } else if (frag.startsWith("/l/")) {
            return "lemma-animate-in";
        } else {
            return "";
        }
    }

</script>

<span>{`${courseId}: `}</span>
{#each titleFrags as frag}
    <span class={getClass(frag)}>
        {frag.replace(/\/[lm]\//, "")}
    </span>
{/each}