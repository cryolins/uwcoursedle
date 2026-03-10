<script lang="ts">
	import Hints from "./Hints.svelte";
	import HowToPlay from "./HowToPlay.svelte";
    import "./navbar.css";
	import Stats from "./Stats.svelte";

    let { openStats=$bindable() } : { openStats?: boolean } = $props();

</script>

<div class="navbar-style">
    <h1 class="text-4xl overflow-hidden">
        <span class="text-primary2">UW</span>Coursedle
    </h1>

    <!-- dialog-opening icons -->
    <div class="icons-container gap-2 sm:gap-4">
        <HowToPlay />
        <Hints />
        <Stats bind:openStats={openStats} />
    </div>
</div>