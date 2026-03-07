<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/uwc-favicon.svg';
	import { ModeWatcher } from 'mode-watcher';
	import GameSonner from '$lib/components/custom/GameSonner.svelte';

	let { children } = $props();
</script>

<svelte:head>
  	<title>UWCoursedle</title>
	<meta name="description" content="Guess the daily UW course!" >
	<meta property="og:title" content="UWCoursedle">
	<meta property="og:description" content="Guess the daily UW course!" >
	<link rel="icon" href={favicon} />
</svelte:head>
<ModeWatcher />
<GameSonner />

{@render children()}
