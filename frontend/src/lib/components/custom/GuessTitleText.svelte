<script lang="ts">
    import "./guesses.css";
    let { titleFrags, courseId }: { titleFrags: string[], courseId: string } = $props();
</script>

<span>{`${courseId}: `}</span>
{#each titleFrags as frag}
    <span class={frag.startsWith("/m/") ? "matched-animate-in" : ""}>{frag.replace("/m/", "")}</span>
{/each}