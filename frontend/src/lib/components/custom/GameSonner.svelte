<script lang="ts">
	import { CircleX, CopyCheck, Trophy } from "@lucide/svelte";
	import { Toaster } from "../ui/sonner";
</script>

{#snippet winIcon()}
    <Trophy class="size-4" />
{/snippet}
{#snippet copyIcon()}
    <CopyCheck class="size-4" />
{/snippet}
{#snippet loseIcon()}
    <CircleX class="size-4" />
{/snippet}

<Toaster position="bottom-left" 
        richColors
        expand
        toastOptions={{
            style: "width: fit-content;"
        }}
        duration={2500}
        successIcon={winIcon}
        infoIcon={copyIcon}
        errorIcon={loseIcon}
 />