<script lang="ts">
    import "./guesses.css";
    let { titleFrags }: { titleFrags: string[] } = $props();
</script>

{#each titleFrags as frag}
    <span class={frag.startsWith("/m/") ? "matched-animate-in" : ""}>{frag.replace("/m/", "")}</span>
{/each}