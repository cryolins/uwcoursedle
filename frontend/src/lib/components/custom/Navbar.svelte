<script lang="ts">
	import HowToPlay from "./HowToPlay.svelte";
    import "./navbar.css";
	import Stats from "./Stats.svelte";

    let { openStats=$bindable() } : { openStats?: boolean } = $props();

</script>

<div class="navbar-style">
    <h1 class="text-4xl overflow-hidden">
        <span class="text-primary2">UW</span>Coursedle
    </h1>

    <!-- dialog-opening icons TODO dialog components -->
    <div class="icons-container gap-2 sm:gap-4">
        <HowToPlay />
        <Stats bind:openStats={openStats} />
    </div>
</div>